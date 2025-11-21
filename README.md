# AskQL - Natural Language to SQL Converter

A full-stack application that converts natural language questions into executable SQL queries on user-provided databases (SQLite or MySQL).

![AskQL Banner](https://img.shields.io/badge/AskQL-v1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🚀 Features

- **Natural Language Processing**: Convert plain English questions to SQL queries
- **Multi-Database Support**: Works with SQLite (upload) and MySQL (connection)
- **Schema Awareness**: Automatically extracts and uses your database schema
- **Ambiguity Detection**: Asks clarifying questions when needed
- **Safe Execution**: Only allows SELECT queries, blocks destructive operations
- **Interactive Chat**: Conversational interface with context awareness
- **Data Visualization**: Automatic chart generation (bar, line, pie charts)
- **Query History**: Track all your queries and results
- **Real-time Validation**: SQL syntax and schema validation

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│          React Frontend                  │
│   (Tailwind CSS + Recharts)             │
└─────────────────────────────────────────┘
                  │
                  │ REST API
                  ▼
┌─────────────────────────────────────────┐
│        FastAPI Backend                   │
│  • NL→SQL Generator (Ollama/OpenAI)     │
│  • SQL Validator & Safety Layer         │
│  • Database Manager (SQLAlchemy)        │
│  • Query Executor                        │
│  • Visualization Engine                  │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      SQLite / MySQL Database            │
└─────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Ollama** (running locally) OR **OpenAI API Key**
- **MySQL Server** (optional, for MySQL connections)

## 🔧 Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and run Ollama** (if using local LLM):
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull a model, e.g., llama2
   ollama pull llama2
   
   # Start Ollama (usually runs automatically on port 11434)
   ollama serve
   ```

5. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   
   **For Ollama (Local LLM):**
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```
   
   **For OpenAI:**
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   LLM_MODEL=gpt-4
   ```

6. **Run the backend**:
   ```bash
   cd app
   python main.py
   ```
   
   Backend will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```
   
   Frontend will start at `http://localhost:3000`

## 🎯 Usage

### 1. Connect to Database

**Option A: SQLite**
- Click "SQLite Upload" tab
- Upload your `.db` file (max 50MB)
- Click "Connect to Database"

**Option B: MySQL**
- Click "MySQL Connection" tab
- Enter connection details:
  - Host (e.g., `localhost`)
  - Port (default: `3306`)
  - Database name
  - Username
  - Password
- Click "Connect to MySQL"

### 2. Ask Questions

Once connected, use the chat interface to ask questions in natural language:

#### Example Questions

**Simple Queries:**
```
- "Show me all users"
- "List all products"
- "Display the first 10 orders"
```

**Filtered Queries:**
```
- "Find users from California"
- "Show products with price greater than 100"
- "Get orders from the last 30 days"
```

**Aggregations:**
```
- "What's the total revenue by category?"
- "Count the number of users by country"
- "Show average order value by month"
```

**Joins:**
```
- "Show customer names with their order totals"
- "List products with their category names"
- "Find users who have never placed an order"
```

**Sorting & Limiting:**
```
- "Top 10 customers by revenue"
- "Most expensive products"
- "Latest 20 orders"
```

### 3. View Results

Results are displayed in multiple formats:
- **Table View**: Structured data table
- **Chart View**: Automatic visualization (bar, line, or pie charts)
- **SQL View**: Generated SQL query
- **Explanation**: Natural language explanation of the query

### 4. Query History

All queries are tracked in the history panel on the right sidebar, showing:
- Original question
- Generated SQL
- Number of rows returned
- Timestamp

## 🛡️ Security Features

### SQL Safety Layer
- ✅ Only SELECT queries allowed
- ❌ Blocks INSERT, UPDATE, DELETE, DROP, ALTER
- ✅ Automatic row limit (max 1000 rows)
- ✅ Query timeout (30 seconds)
- ✅ SQL injection prevention via parameterized queries
- ✅ Schema validation

### File Upload Safety
- File size limit: 50MB
- File type validation: `.db` only
- Isolated storage per session
- Automatic cleanup on disconnect

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   └── config.py          # Configuration
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── services/
│   │   │   ├── database_manager.py    # DB connections
│   │   │   ├── sql_generator.py       # NL→SQL
│   │   │   ├── sql_validator.py       # SQL validation
│   │   │   ├── query_executor.py      # Query execution
│   │   │   └── visualization.py       # Chart generation
│   │   └── main.py                # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SchemaPanel.jsx
│   │   │   ├── ResultsPanel.jsx
│   │   │   └── QueryHistory.jsx
│   │   ├── pages/
│   │   │   ├── DatabaseConnect.jsx
│   │   │   └── QueryInterface.jsx
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── ARCHITECTURE.md
└── README.md
```

## 🔌 API Endpoints

### Database Connection
- `POST /api/connect/sqlite` - Upload SQLite database
- `POST /api/connect/mysql` - Connect to MySQL
- `GET /api/schema/{session_id}` - Get database schema

### Query Operations
- `POST /api/ask` - Convert natural language to SQL
- `POST /api/execute` - Execute SQL query
- `POST /api/visualize` - Generate chart configuration
- `GET /api/history/{session_id}` - Get query history

### Session Management
- `DELETE /api/session/{session_id}` - Close session and cleanup
- `GET /api/health` - Health check

## 🧪 Example Workflow

1. **Connect**: Upload `chinook.db` (SQLite sample database)
2. **Ask**: "Show me the top 5 artists by number of albums"
3. **AskQL Generates**:
   ```sql
   SELECT artists.Name, COUNT(albums.AlbumId) as album_count
   FROM artists
   JOIN albums ON artists.ArtistId = albums.ArtistId
   GROUP BY artists.ArtistId, artists.Name
   ORDER BY album_count DESC
   LIMIT 5
   ```
4. **Results**: Table with artist names and album counts
5. **Visualization**: Bar chart showing the distribution

## 🎨 UI Features

- **Responsive Design**: Works on desktop and tablet
- **Dark Code Blocks**: SQL queries displayed in syntax-highlighted blocks
- **Real-time Feedback**: Loading states and error messages
- **Collapsible Schema**: Expandable table/column viewer
- **Chat History**: Conversation-style interface
- **Multi-view Results**: Switch between table and chart views

## ⚙️ Configuration

### Environment Variables

**Backend (`.env`)**:

**Option 1: Using Ollama (Local)**
```env
LLM_PROVIDER=ollama                 # Use local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2                 # or mistral, codellama, etc.
LLM_TEMPERATURE=0.1                 # Lower = more deterministic
MAX_FILE_SIZE=52428800              # 50MB
MAX_QUERY_ROWS=1000                 # Result limit
QUERY_TIMEOUT=30                    # Seconds
CORS_ORIGINS=http://localhost:3000
```

**Option 2: Using OpenAI**
```env
LLM_PROVIDER=openai                 # Use OpenAI API
OPENAI_API_KEY=sk-...               # Required for OpenAI
LLM_MODEL=gpt-4                     # or gpt-3.5-turbo
LLM_TEMPERATURE=0.1                 # Lower = more deterministic
MAX_FILE_SIZE=52428800              # 50MB
MAX_QUERY_ROWS=1000                 # Result limit
QUERY_TIMEOUT=30                    # Seconds
CORS_ORIGINS=http://localhost:3000
```

### Customization

**Change LLM Provider**: Set `LLM_PROVIDER` to `ollama` or `openai` in `.env`
**Change Ollama Model**: Edit `OLLAMA_MODEL` in `.env` (llama2, mistral, codellama, etc.)
**Change OpenAI Model**: Edit `LLM_MODEL` in `.env` (gpt-4, gpt-3.5-turbo)
**Adjust Row Limit**: Edit `MAX_QUERY_ROWS` in `.env`
**Modify UI Theme**: Edit Tailwind classes in component files

### Ollama Model Recommendations

For best results with SQL generation, consider these models:
- **llama2** (7B/13B) - Good balance of speed and accuracy
- **codellama** - Optimized for code generation, excellent for SQL
- **mistral** - Fast and accurate
- **mixtral** - Best performance but requires more resources

Pull a model:
```bash
ollama pull codellama
```

## 🐛 Troubleshooting

### Backend Issues

**"Cannot connect to Ollama"**
- Ensure Ollama is installed and running: `ollama serve`
- Check Ollama is accessible at `http://localhost:11434`
- Pull a model: `ollama pull llama2`

**"OpenAI API Key not found"**
- Ensure `.env` file exists with valid `OPENAI_API_KEY`
- Or switch to Ollama by setting `LLM_PROVIDER=ollama`

**"Failed to connect to MySQL"**
- Verify MySQL server is running
- Check credentials and database name
- Ensure MySQL port (3306) is accessible

**"Module not found"**
- Run `pip install -r requirements.txt` again
- Activate virtual environment

### Frontend Issues

**"Cannot connect to backend"**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend `.env`

**"npm install fails"**
- Use Node.js 18 or higher
- Delete `node_modules` and `package-lock.json`, then retry

## 📚 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **OpenAI API** - GPT-4 for NL→SQL generation
- **SQLParse** - SQL parsing and validation
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **Recharts** - Chart library
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Support for PostgreSQL, Oracle, SQL Server
- Query optimization suggestions
- Natural language result summarization
- Export results to CSV/Excel
- User authentication and saved queries
- Multi-language support

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the ARCHITECTURE.md file
3. Open an issue on GitHub

---

**Built with ❤️ using FastAPI, React, and OpenAI GPT-4**
