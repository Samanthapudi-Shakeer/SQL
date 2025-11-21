# AskQL Quick Start Guide

Get up and running with AskQL in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed  
- [ ] OpenAI API key (get from https://platform.openai.com/api-keys)
- [ ] A SQLite database file OR MySQL database access

## Step-by-Step Setup

### 1. Clone/Download the Repository

```bash
cd /path/to/SQL
```

### 2. Backend Setup (2 minutes)

```bash
# Go to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Frontend Setup (2 minutes)

Open a NEW terminal window:

```bash
# Go to frontend directory
cd frontend

# Install dependencies
npm install
```

### 4. Start the Application (1 minute)

**Terminal 1 (Backend):**
```bash
cd backend/app
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE ready in XXX ms
  ➜  Local:   http://localhost:3000/
```

### 5. Open Your Browser

Visit: http://localhost:3000

## First Query Example

1. **Connect Database**:
   - If you have a SQLite .db file: Click "SQLite Upload" → Choose file → Connect
   - If you have MySQL: Click "MySQL Connection" → Enter credentials → Connect

2. **Ask a Question**:
   ```
   "Show me the first 10 rows from any table"
   ```

3. **View Results**:
   - See the generated SQL
   - View data in table format
   - Switch to chart view if applicable

## Testing Without a Database

Don't have a database handy? Create a simple one:

```bash
# Create test database
cd backend/data/uploads

# Start Python
python

# Create sample database
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
)
''')

cursor.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@example.com', 30)")
cursor.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@example.com', 25)")
cursor.execute("INSERT INTO users VALUES (3, 'Charlie', 'charlie@example.com', 35)")

conn.commit()
conn.close()
exit()
```

Now upload `test.db` in the UI!

## Example Questions to Try

```
1. "Show me all users"
2. "Find users older than 30"
3. "Count how many users we have"
4. "What's the average age?"
5. "Show users sorted by name"
```

## Common Issues & Solutions

### Backend won't start

**Error**: `No module named 'fastapi'`
- **Solution**: Make sure virtual environment is activated and dependencies installed
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Error**: `OpenAI API key not found`
- **Solution**: Check your `.env` file has `OPENAI_API_KEY=sk-...`

### Frontend won't start

**Error**: `Cannot find module`
- **Solution**: Delete `node_modules` and reinstall
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

### Can't connect to backend

**Error**: `Network Error` or `ERR_CONNECTION_REFUSED`
- **Solution**: 
  1. Check backend is running on port 8000
  2. Check CORS settings in backend `.env`
  3. Try `http://localhost:8000/api/health` in browser

### MySQL connection fails

**Error**: `Failed to connect to MySQL`
- **Solution**:
  1. Verify MySQL server is running
  2. Check credentials are correct
  3. Ensure database exists
  4. Check MySQL port (usually 3306)

## Architecture Overview

```
Browser (http://localhost:3000)
    ↓
Frontend (React + Vite)
    ↓ HTTP/REST
Backend (FastAPI on http://localhost:8000)
    ↓
OpenAI API (GPT-4)
    ↓
Database (SQLite/MySQL)
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [EXAMPLE_QUERIES.md](EXAMPLE_QUERIES.md) for query ideas
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

## Production Deployment Tips

### Backend
```bash
# Install gunicorn for production
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
# Build for production
npm run build

# Preview build
npm run preview

# Deploy dist/ folder to your hosting service
```

### Environment Variables

For production, set these in your hosting platform:
- `OPENAI_API_KEY` - Your OpenAI API key
- `CORS_ORIGINS` - Your frontend domain
- `DEBUG=False` - Disable debug mode

## Support

Having trouble? Check:
1. All terminals are running (backend + frontend)
2. Virtual environment is activated
3. .env file has valid OpenAI API key
4. No other services using ports 3000 or 8000

---

**You're all set! Start asking questions in natural language!** 🎉
