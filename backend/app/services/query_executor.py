"""SQL query execution service."""
from typing import List, Dict, Any, Tuple
from sqlalchemy import text
from app.core.config import settings
import signal
import contextlib


class TimeoutException(Exception):
    """Query timeout exception."""
    pass


@contextlib.contextmanager
def timeout(seconds):
    """Context manager for timeout."""
    def signal_handler(signum, frame):
        raise TimeoutException("Query execution timeout")
    
    # Set the signal handler
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class QueryExecutor:
    """Executes SQL queries safely."""
    
    def execute(self, engine, sql: str) -> Tuple[bool, List[Dict[str, Any]], List[str], str]:
        """
        Execute SQL query.
        
        Returns:
            success: bool
            data: List of rows as dictionaries
            columns: List of column names
            message: Error or success message
        """
        try:
            with engine.connect() as connection:
                # Use timeout for query execution
                try:
                    with timeout(settings.QUERY_TIMEOUT):
                        result = connection.execute(text(sql))
                        
                        # Fetch results
                        rows = result.fetchall()
                        
                        if not rows:
                            return True, [], [], "Query executed successfully but returned no results"
                        
                        # Get column names
                        columns = list(result.keys())
                        
                        # Convert to list of dictionaries
                        data = []
                        for row in rows:
                            row_dict = {}
                            for i, col in enumerate(columns):
                                value = row[i]
                                # Convert to JSON-serializable types
                                if value is not None:
                                    row_dict[col] = self._serialize_value(value)
                                else:
                                    row_dict[col] = None
                            data.append(row_dict)
                        
                        return True, data, columns, f"Successfully retrieved {len(data)} rows"
                        
                except TimeoutException:
                    return False, [], [], f"Query execution timeout after {settings.QUERY_TIMEOUT} seconds"
                
        except Exception as e:
            error_msg = str(e)
            return False, [], [], f"Query execution error: {error_msg}"
    
    def _serialize_value(self, value: Any) -> Any:
        """Convert value to JSON-serializable type."""
        # Handle common types
        if isinstance(value, (int, float, str, bool, type(None))):
            return value
        
        # Handle dates/datetime
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        
        # Handle bytes
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8')
            except:
                return str(value)
        
        # Default: convert to string
        return str(value)
    
    def validate_results(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validate query results."""
        if not data:
            return False, "Query returned no results. Try refining your question."
        
        if len(data) > settings.MAX_QUERY_ROWS:
            return False, f"Query returned too many results ({len(data)}). Please add more filters."
        
        return True, "Results are valid"


# Global query executor instance
query_executor = QueryExecutor()
