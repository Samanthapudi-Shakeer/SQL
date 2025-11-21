"""Database connection and management service."""
import os
import uuid
import aiosqlite
from typing import Dict, Optional, Any
from sqlalchemy import create_engine, inspect, text, MetaData
from sqlalchemy.pool import NullPool
from app.models.schemas import DatabaseSchema, TableSchema, ColumnSchema, MySQLConnectionRequest
from app.core.config import settings


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self):
        self.connections: Dict[str, Any] = {}
        self.schemas: Dict[str, DatabaseSchema] = {}
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def connect_sqlite(self, file_content: bytes, filename: str) -> tuple[str, DatabaseSchema]:
        """Connect to SQLite database from uploaded file."""
        session_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{session_id}_{filename}")
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Create connection
        connection_string = f"sqlite:///{file_path}"
        engine = create_engine(connection_string, poolclass=NullPool)
        
        # Extract schema
        schema = await self._extract_schema(engine, "sqlite")
        
        self.connections[session_id] = {
            "engine": engine,
            "type": "sqlite",
            "file_path": file_path
        }
        self.schemas[session_id] = schema
        
        return session_id, schema
    
    def connect_mysql(self, conn_params: MySQLConnectionRequest) -> tuple[str, DatabaseSchema]:
        """Connect to MySQL database."""
        session_id = str(uuid.uuid4())
        
        connection_string = (
            f"mysql+pymysql://{conn_params.username}:{conn_params.password}"
            f"@{conn_params.host}:{conn_params.port}/{conn_params.database}"
        )
        
        engine = create_engine(connection_string, poolclass=NullPool)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Extract schema
        schema = self._extract_schema_sync(engine, "mysql")
        
        self.connections[session_id] = {
            "engine": engine,
            "type": "mysql"
        }
        self.schemas[session_id] = schema
        
        return session_id, schema
    
    async def _extract_schema(self, engine, db_type: str) -> DatabaseSchema:
        """Extract database schema asynchronously."""
        return self._extract_schema_sync(engine, db_type)
    
    def _extract_schema_sync(self, engine, db_type: str) -> DatabaseSchema:
        """Extract database schema synchronously."""
        inspector = inspect(engine)
        tables = []
        
        for table_name in inspector.get_table_names():
            columns = []
            pk_constraint = inspector.get_pk_constraint(table_name)
            pk_columns = pk_constraint.get("constrained_columns", []) if pk_constraint else []
            
            for column in inspector.get_columns(table_name):
                col_schema = ColumnSchema(
                    name=column["name"],
                    type=str(column["type"]),
                    primary_key=column["name"] in pk_columns,
                    nullable=column.get("nullable", True)
                )
                
                # Check for foreign keys
                for fk in inspector.get_foreign_keys(table_name):
                    if column["name"] in fk.get("constrained_columns", []):
                        ref_table = fk.get("referred_table")
                        ref_cols = fk.get("referred_columns", [])
                        if ref_cols:
                            col_schema.foreign_key = f"{ref_table}.{ref_cols[0]}"
                
                columns.append(col_schema)
            
            tables.append(TableSchema(name=table_name, columns=columns))
        
        return DatabaseSchema(tables=tables, database_type=db_type)
    
    def get_engine(self, session_id: str):
        """Get database engine for session."""
        if session_id not in self.connections:
            raise ValueError(f"No connection found for session {session_id}")
        return self.connections[session_id]["engine"]
    
    def get_schema(self, session_id: str) -> DatabaseSchema:
        """Get database schema for session."""
        if session_id not in self.schemas:
            raise ValueError(f"No schema found for session {session_id}")
        return self.schemas[session_id]
    
    def close_connection(self, session_id: str):
        """Close database connection and cleanup."""
        if session_id in self.connections:
            conn_info = self.connections[session_id]
            conn_info["engine"].dispose()
            
            # Remove SQLite file if exists
            if conn_info["type"] == "sqlite" and "file_path" in conn_info:
                try:
                    os.remove(conn_info["file_path"])
                except:
                    pass
            
            del self.connections[session_id]
            if session_id in self.schemas:
                del self.schemas[session_id]


# Global database manager instance
db_manager = DatabaseManager()
