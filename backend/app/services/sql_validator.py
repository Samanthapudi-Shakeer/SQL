"""SQL validation and safety service."""
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Token
from sqlparse.tokens import Keyword, DML
from typing import List, Tuple
from app.models.schemas import DatabaseSchema


class SQLValidator:
    """Validates SQL queries for safety and correctness."""
    
    ALLOWED_KEYWORDS = {
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER',
        'ON', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN', 'IS', 'NULL',
        'GROUP', 'BY', 'HAVING', 'ORDER', 'ASC', 'DESC', 'LIMIT', 'OFFSET',
        'AS', 'DISTINCT', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'CASE', 'WHEN',
        'THEN', 'ELSE', 'END', 'CAST', 'UNION', 'ALL', 'EXISTS'
    }
    
    FORBIDDEN_KEYWORDS = {
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE',
        'REPLACE', 'MERGE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE', 'CALL',
        'DECLARE', 'SET', 'BEGIN', 'COMMIT', 'ROLLBACK', 'SAVEPOINT'
    }
    
    def validate(self, sql: str, schema: DatabaseSchema) -> Tuple[bool, str]:
        """Validate SQL query for safety and correctness."""
        
        # Parse SQL
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                return False, "Invalid SQL syntax"
        except Exception as e:
            return False, f"SQL parsing error: {str(e)}"
        
        # Check for forbidden operations
        sql_upper = sql.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in sql_upper:
                return False, f"Forbidden operation: {keyword} is not allowed. Only SELECT queries are permitted."
        
        # Check for multiple statements
        if len(parsed) > 1:
            return False, "Multiple SQL statements are not allowed"
        
        statement = parsed[0]
        
        # Ensure it's a SELECT statement
        if not self._is_select_statement(statement):
            return False, "Only SELECT statements are allowed"
        
        # Extract and validate table names
        tables = self._extract_table_names(statement)
        valid_tables = {table.name.lower() for table in schema.tables}
        
        for table in tables:
            if table.lower() not in valid_tables:
                return False, f"Table '{table}' does not exist in schema"
        
        # Validate columns (basic check)
        # Note: This is a simplified check. Full validation would require parsing all column references
        all_columns = set()
        for table in schema.tables:
            for col in table.columns:
                all_columns.add(col.name.lower())
        
        return True, "Valid SQL query"
    
    def _is_select_statement(self, statement) -> bool:
        """Check if statement is a SELECT statement."""
        for token in statement.tokens:
            if token.ttype is DML and token.value.upper() == 'SELECT':
                return True
        return False
    
    def _extract_table_names(self, statement) -> List[str]:
        """Extract table names from SQL statement."""
        tables = []
        from_seen = False
        
        for token in statement.tokens:
            if from_seen:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.append(self._get_real_name(identifier))
                elif isinstance(token, Identifier):
                    tables.append(self._get_real_name(token))
                from_seen = False
            
            if token.ttype is Keyword and token.value.upper() == 'FROM':
                from_seen = True
            
            # Handle JOIN clauses
            if token.ttype is Keyword and 'JOIN' in token.value.upper():
                from_seen = True
        
        return tables
    
    def _get_real_name(self, identifier) -> str:
        """Get the real table name from an identifier."""
        if isinstance(identifier, Identifier):
            # Handle aliases
            return identifier.get_real_name()
        return str(identifier)
    
    def add_row_limit(self, sql: str, max_rows: int = 1000) -> str:
        """Add LIMIT clause to SQL if not present."""
        sql_upper = sql.upper()
        
        if 'LIMIT' not in sql_upper:
            # Add LIMIT clause
            sql = sql.rstrip(';').strip()
            sql += f" LIMIT {max_rows}"
        
        return sql
    
    def sanitize_sql(self, sql: str) -> str:
        """Sanitize SQL query."""
        # Remove comments
        sql = sqlparse.format(sql, strip_comments=True)
        
        # Remove trailing semicolons
        sql = sql.rstrip(';').strip()
        
        return sql


# Global SQL validator instance
sql_validator = SQLValidator()
