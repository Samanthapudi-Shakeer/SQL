"""NL to SQL generation service using LLM."""
import json
from typing import List, Dict, Optional
from openai import OpenAI
from app.models.schemas import DatabaseSchema, SQLResponse
from app.core.config import settings


class SQLGenerator:
    """Generates SQL from natural language using LLM."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_sql(
        self,
        question: str,
        schema: DatabaseSchema,
        context: List[Dict[str, str]] = None
    ) -> SQLResponse:
        """Generate SQL from natural language question."""
        
        # Build schema description
        schema_desc = self._build_schema_description(schema)
        
        # Build conversation context
        context_str = ""
        if context:
            context_str = "\n\nPrevious conversation:\n"
            for item in context[-3:]:  # Last 3 exchanges
                context_str += f"Q: {item.get('question', '')}\nA: {item.get('answer', '')}\n"
        
        # Create prompt
        system_prompt = f"""You are an expert SQL query generator. Your task is to convert natural language questions into correct SQL queries.

Database Schema:
{schema_desc}

Rules:
1. Generate ONLY SELECT queries (no INSERT, UPDATE, DELETE, DROP, ALTER, etc.)
2. Use correct table and column names from the schema
3. If the question is ambiguous or missing information, set needs_clarification=true and ask a clarifying question
4. Be case-insensitive when matching user-mentioned table/column names to schema
5. Add appropriate WHERE, JOIN, GROUP BY, ORDER BY clauses as needed
6. Limit results to {settings.MAX_QUERY_ROWS} rows if no limit specified
7. Return valid JSON only

Response format:
{{
  "sql": "SELECT ...",
  "explanation": "This query retrieves...",
  "needs_clarification": false,
  "clarification_question": null,
  "confidence": 0.95
}}

If ambiguous, respond:
{{
  "sql": null,
  "explanation": "Need more information",
  "needs_clarification": true,
  "clarification_question": "Which table are you referring to: users or customers?",
  "confidence": 0.3
}}"""

        user_prompt = f"{context_str}\n\nQuestion: {question}\n\nGenerate the SQL query:"
        
        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            return SQLResponse(
                sql=result.get("sql"),
                explanation=result.get("explanation", ""),
                needs_clarification=result.get("needs_clarification", False),
                clarification_question=result.get("clarification_question"),
                confidence=result.get("confidence", 1.0)
            )
            
        except json.JSONDecodeError as e:
            # Fallback: try to extract SQL from response
            return SQLResponse(
                sql=None,
                explanation=f"Failed to parse LLM response: {str(e)}",
                needs_clarification=True,
                clarification_question="Could you rephrase your question?",
                confidence=0.0
            )
        except Exception as e:
            return SQLResponse(
                sql=None,
                explanation=f"Error generating SQL: {str(e)}",
                needs_clarification=True,
                clarification_question="I encountered an error. Could you try asking differently?",
                confidence=0.0
            )
    
    def _build_schema_description(self, schema: DatabaseSchema) -> str:
        """Build a text description of the database schema."""
        desc = f"Database type: {schema.database_type}\n\nTables:\n"
        
        for table in schema.tables:
            desc += f"\n{table.name}:\n"
            for col in table.columns:
                pk_marker = " [PRIMARY KEY]" if col.primary_key else ""
                fk_marker = f" [FK -> {col.foreign_key}]" if col.foreign_key else ""
                null_marker = "" if col.nullable else " [NOT NULL]"
                desc += f"  - {col.name}: {col.type}{pk_marker}{fk_marker}{null_marker}\n"
        
        return desc
    
    def detect_ambiguity(self, question: str, schema: DatabaseSchema) -> tuple[bool, Optional[str]]:
        """Detect if a question is ambiguous."""
        # Simple heuristic-based ambiguity detection
        question_lower = question.lower()
        
        # Check for vague references
        vague_terms = ["it", "that", "those", "them", "this", "these"]
        if any(term in question_lower.split() for term in vague_terms):
            return True, "Could you be more specific about what you're referring to?"
        
        # Check for multiple possible table matches
        mentioned_tables = [
            table.name for table in schema.tables
            if table.name.lower() in question_lower
        ]
        
        if len(mentioned_tables) == 0:
            # No tables mentioned - might be ambiguous
            if len(schema.tables) > 3:
                table_names = ", ".join([t.name for t in schema.tables[:5]])
                return True, f"Which table are you interested in? Available tables: {table_names}"
        
        return False, None


# Global SQL generator instance
sql_generator = SQLGenerator()
