"""API routes for AskQL."""
import uuid
from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import (
    MySQLConnectionRequest, ConnectionResponse, QuestionRequest,
    SQLResponse, ExecuteRequest, ExecuteResponse, VisualizationRequest,
    ChartConfig, QueryHistoryResponse, QueryHistoryItem, ErrorResponse
)
from app.services.database_manager import db_manager
from app.services.sql_generator import sql_generator
from app.services.sql_validator import sql_validator
from app.services.query_executor import query_executor
from app.services.visualization import visualization_service
from app.core.config import settings

router = APIRouter()

# In-memory query history (in production, use a database)
query_history: Dict[str, List[QueryHistoryItem]] = {}


@router.post("/connect/sqlite", response_model=ConnectionResponse)
async def connect_sqlite(file: UploadFile = File(...)):
    """Upload and connect to SQLite database."""
    try:
        # Validate file
        if not file.filename.endswith('.db'):
            raise HTTPException(status_code=400, detail="Only .db files are allowed")
        
        # Read file content
        content = await file.read()
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Connect to database
        session_id, schema = await db_manager.connect_sqlite(content, file.filename)
        
        # Initialize query history for session
        query_history[session_id] = []
        
        return ConnectionResponse(
            success=True,
            message="Successfully connected to SQLite database",
            session_id=session_id,
            schema=schema
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/connect/mysql", response_model=ConnectionResponse)
async def connect_mysql(request: MySQLConnectionRequest):
    """Connect to MySQL database."""
    try:
        session_id, schema = db_manager.connect_mysql(request)
        
        # Initialize query history for session
        query_history[session_id] = []
        
        return ConnectionResponse(
            success=True,
            message="Successfully connected to MySQL database",
            session_id=session_id,
            schema=schema
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect: {str(e)}")


@router.get("/schema/{session_id}")
async def get_schema(session_id: str):
    """Get database schema for session."""
    try:
        schema = db_manager.get_schema(session_id)
        return schema
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/ask", response_model=SQLResponse)
async def ask_question(request: QuestionRequest):
    """Convert natural language question to SQL."""
    try:
        # Get schema
        schema = db_manager.get_schema(request.session_id)
        
        # Check for ambiguity first (heuristic-based)
        is_ambiguous, clarification = sql_generator.detect_ambiguity(request.question, schema)
        
        if is_ambiguous and not request.context:
            return SQLResponse(
                sql=None,
                explanation="Question needs clarification",
                needs_clarification=True,
                clarification_question=clarification,
                confidence=0.3
            )
        
        # Generate SQL
        response = sql_generator.generate_sql(request.question, schema, request.context)
        
        # If SQL generated, validate it
        if response.sql and not response.needs_clarification:
            is_valid, validation_msg = sql_validator.validate(response.sql, schema)
            
            if not is_valid:
                return SQLResponse(
                    sql=None,
                    explanation=validation_msg,
                    needs_clarification=True,
                    clarification_question="Could you rephrase your question?",
                    confidence=0.2
                )
            
            # Add row limit
            response.sql = sql_validator.add_row_limit(response.sql, settings.MAX_QUERY_ROWS)
            response.sql = sql_validator.sanitize_sql(response.sql)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute", response_model=ExecuteResponse)
async def execute_query(request: ExecuteRequest):
    """Execute SQL query."""
    try:
        # Get engine
        engine = db_manager.get_engine(request.session_id)
        
        # Get schema for validation
        schema = db_manager.get_schema(request.session_id)
        
        # Validate SQL
        is_valid, validation_msg = sql_validator.validate(request.sql, schema)
        if not is_valid:
            raise HTTPException(status_code=400, detail=validation_msg)
        
        # Sanitize and add limit
        sql = sql_validator.sanitize_sql(request.sql)
        sql = sql_validator.add_row_limit(sql, settings.MAX_QUERY_ROWS)
        
        # Execute query
        success, data, columns, message = query_executor.execute(engine, sql)
        
        if not success:
            raise HTTPException(status_code=500, detail=message)
        
        # Validate results
        is_valid, validation_msg = query_executor.validate_results(data)
        
        # Add to history
        if request.session_id in query_history:
            history_item = QueryHistoryItem(
                id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                question="",  # Not available in execute endpoint
                sql=sql,
                success=success,
                row_count=len(data)
            )
            query_history[request.session_id].append(history_item)
        
        return ExecuteResponse(
            success=True,
            data=data,
            columns=columns,
            row_count=len(data),
            message=message if is_valid else validation_msg
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visualize", response_model=ChartConfig)
async def visualize_data(request: VisualizationRequest):
    """Generate visualization configuration for data."""
    try:
        chart_config = visualization_service.suggest_chart(
            request.data,
            request.columns,
            request.preferred_chart
        )
        return chart_config
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=QueryHistoryResponse)
async def get_query_history(session_id: str):
    """Get query history for session."""
    if session_id not in query_history:
        return QueryHistoryResponse(items=[], total=0)
    
    items = query_history[session_id]
    return QueryHistoryResponse(items=items, total=len(items))


@router.delete("/session/{session_id}")
async def close_session(session_id: str):
    """Close database session and cleanup."""
    try:
        db_manager.close_connection(session_id)
        if session_id in query_history:
            del query_history[session_id]
        return {"success": True, "message": "Session closed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AskQL"}
