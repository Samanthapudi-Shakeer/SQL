# AskQL Architecture

## Overview
AskQL is a full-stack application that converts natural language questions into executable SQL queries on user-provided databases (SQLite or MySQL).

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Connect   │  │  Query Chat  │  │  Results Panel   │   │
│  │  Database   │  │   Interface  │  │  + Visualization │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│                    React + Tailwind CSS                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   API Endpoints                       │   │
│  │  /connect/sqlite  /connect/mysql  /schema            │   │
│  │  /ask  /execute  /visualize  /history                │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────┐   │
│  │  Database    │  │   NL→SQL        │  │     SQL      │   │
│  │  Connection  │  │   Generator     │  │  Validator   │   │
│  │  Manager     │  │   (LLM-based)   │  │  & Safety    │   │
│  └──────────────┘  └─────────────────┘  └──────────────┘   │
│                                                               │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────┐   │
│  │   Schema     │  │    Query        │  │ Visualization│   │
│  │ Introspector │  │   Executor      │  │   Engine     │   │
│  └──────────────┘  └─────────────────┘  └──────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │  SQLite / MySQL Database     │
              └──────────────────────────────┘
```

## Core Components

### Frontend (React + Tailwind)
1. **Database Connection Page**
   - SQLite file upload
   - MySQL connection form
   - Schema display

2. **Query Chat Interface**
   - Natural language input
   - Conversation history
   - Clarification prompts

3. **Results Panel**
   - Generated SQL display
   - Natural language explanation
   - Data table
   - Chart visualization
   - Query history sidebar

### Backend (FastAPI)

#### 1. Database Connection Manager
- SQLite file handling
- MySQL connection pooling
- Connection validation
- Schema caching

#### 2. Schema Introspector
- Extract table names
- Extract column names and types
- Extract relationships (foreign keys)
- Generate schema JSON representation

#### 3. NL→SQL Generator
- LLM-based query generation (OpenAI GPT-4 or similar)
- Schema-aware prompting
- Context management
- Query refinement

#### 4. Ambiguity Detector
- Analyze natural language for ambiguity
- Identify missing context
- Generate clarifying questions
- Multi-turn conversation support

#### 5. SQL Validator & Safety Layer
- Parse SQL syntax
- Validate table/column existence
- Block destructive operations (DROP, DELETE, UPDATE, INSERT)
- Allow only SELECT queries
- Row limit enforcement

#### 6. Query Executor
- Safe SQL execution
- Result validation (non-empty check)
- Error handling
- Timeout management

#### 7. Visualization Engine
- Analyze result data types
- Suggest appropriate chart types
- Generate chart configurations
- Support bar, line, and pie charts

## API Endpoints

### POST /connect/sqlite
Upload SQLite database file
```json
{
  "file": "<base64_encoded_db>"
}
```

### POST /connect/mysql
Connect to MySQL database
```json
{
  "host": "localhost",
  "port": 3306,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}
```

### GET /schema
Get current database schema
```json
{
  "tables": [
    {
      "name": "users",
      "columns": [
        {"name": "id", "type": "INTEGER", "primary_key": true},
        {"name": "name", "type": "VARCHAR(100)"}
      ]
    }
  ]
}
```

### POST /ask
Convert natural language to SQL
```json
{
  "question": "Show me all users from California",
  "conversation_id": "uuid",
  "context": []
}
```

Response:
```json
{
  "sql": "SELECT * FROM users WHERE state = 'California'",
  "explanation": "This query retrieves all user records...",
  "needs_clarification": false,
  "clarification_question": null
}
```

### POST /execute
Execute SQL query
```json
{
  "sql": "SELECT * FROM users LIMIT 10"
}
```

### POST /visualize
Generate chart configuration
```json
{
  "data": [...],
  "chart_type": "bar"
}
```

### GET /history
Get query history

## Data Flow

1. **Database Connection**
   ```
   User → Upload/Connect → Backend validates → Extract schema → Return schema JSON
   ```

2. **Query Processing**
   ```
   User question → Ambiguity detection → 
   [If ambiguous] → Ask clarification → Get user response →
   Generate SQL (with schema context) → Validate SQL → 
   Execute safely → Validate results → 
   Generate explanation → Suggest visualization → Return response
   ```

3. **Visualization**
   ```
   Query results → Analyze data types → 
   Determine best chart type → Generate chart config → 
   Frontend renders chart
   ```

## Security Measures

1. **SQL Injection Prevention**
   - Parameterized queries
   - SQL parsing and validation
   - Whitelist of allowed operations

2. **Database Safety**
   - Read-only queries (SELECT only)
   - Row limit enforcement (max 1000 rows)
   - Query timeout (30 seconds)
   - No DDL operations

3. **File Upload Safety**
   - File size limits (max 50MB)
   - File type validation
   - Isolated storage

4. **API Security**
   - CORS configuration
   - Rate limiting
   - Error message sanitization

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy (ORM + Core)
- **LLM**: OpenAI API (GPT-4)
- **Validation**: sqlparse, sqlglot
- **File handling**: aiofiles

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **State Management**: React Context + Hooks

### Development
- **Package Manager**: npm (frontend), pip (backend)
- **Testing**: pytest (backend), Jest (frontend)
- **Linting**: ESLint, Black

## Deployment Considerations

1. **Environment Variables**
   - OPENAI_API_KEY
   - DATABASE_URL (optional default)
   - CORS_ORIGINS
   - MAX_FILE_SIZE

2. **Database Storage**
   - Uploaded SQLite files in `/data/uploads`
   - Temporary files cleanup

3. **Scaling**
   - Stateless backend design
   - Connection pooling
   - LLM response caching

## Error Handling

1. **Database Errors**
   - Connection failures
   - Invalid queries
   - Timeout errors

2. **LLM Errors**
   - API failures
   - Invalid SQL generation
   - Retry logic

3. **User Errors**
   - Invalid file uploads
   - Malformed questions
   - Empty results

All errors return structured JSON with user-friendly messages.
