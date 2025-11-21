"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum


class ChartType(str, Enum):
    """Supported chart types."""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    TABLE = "table"


class ColumnSchema(BaseModel):
    """Database column schema."""
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = True
    foreign_key: Optional[str] = None


class TableSchema(BaseModel):
    """Database table schema."""
    name: str
    columns: List[ColumnSchema]


class DatabaseSchema(BaseModel):
    """Complete database schema."""
    tables: List[TableSchema]
    database_type: str  # sqlite or mysql


class MySQLConnectionRequest(BaseModel):
    """MySQL connection parameters."""
    host: str = Field(..., description="MySQL host")
    port: int = Field(3306, description="MySQL port")
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class ConnectionResponse(BaseModel):
    """Database connection response."""
    success: bool
    message: str
    session_id: str
    schema: Optional[DatabaseSchema] = None


class QuestionRequest(BaseModel):
    """Natural language question request."""
    question: str = Field(..., description="Natural language question")
    session_id: str = Field(..., description="Database session ID")
    conversation_id: Optional[str] = None
    context: List[Dict[str, str]] = Field(default_factory=list, description="Conversation context")


class SQLResponse(BaseModel):
    """SQL generation response."""
    sql: Optional[str] = None
    explanation: str
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    confidence: float = 1.0


class ExecuteRequest(BaseModel):
    """SQL execution request."""
    sql: str = Field(..., description="SQL query to execute")
    session_id: str = Field(..., description="Database session ID")


class ExecuteResponse(BaseModel):
    """SQL execution response."""
    success: bool
    data: List[Dict[str, Any]]
    columns: List[str]
    row_count: int
    message: Optional[str] = None


class VisualizationRequest(BaseModel):
    """Visualization request."""
    data: List[Dict[str, Any]]
    columns: List[str]
    preferred_chart: Optional[ChartType] = None


class ChartConfig(BaseModel):
    """Chart configuration."""
    chart_type: ChartType
    x_axis: Optional[str] = None
    y_axis: Optional[List[str]] = None
    labels: Optional[List[str]] = None
    values: Optional[List[float]] = None
    title: str = ""
    description: str = ""


class QueryHistoryItem(BaseModel):
    """Query history item."""
    id: str
    timestamp: str
    question: str
    sql: str
    success: bool
    row_count: int


class QueryHistoryResponse(BaseModel):
    """Query history response."""
    items: List[QueryHistoryItem]
    total: int


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    error_type: str = "general"
