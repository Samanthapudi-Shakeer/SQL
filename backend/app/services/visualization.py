"""Data visualization service."""
from typing import List, Dict, Any, Optional
from app.models.schemas import ChartType, ChartConfig


class VisualizationService:
    """Generates chart configurations from query results."""
    
    def suggest_chart(
        self,
        data: List[Dict[str, Any]],
        columns: List[str],
        preferred_chart: Optional[ChartType] = None
    ) -> ChartConfig:
        """Suggest appropriate chart type and configuration."""
        
        if not data or not columns:
            return ChartConfig(
                chart_type=ChartType.TABLE,
                title="No Data",
                description="No data available for visualization"
            )
        
        # If preferred chart specified, try to use it
        if preferred_chart:
            return self._generate_chart_config(data, columns, preferred_chart)
        
        # Analyze data to suggest best chart type
        chart_type = self._analyze_data_for_chart_type(data, columns)
        return self._generate_chart_config(data, columns, chart_type)
    
    def _analyze_data_for_chart_type(self, data: List[Dict[str, Any]], columns: List[str]) -> ChartType:
        """Analyze data to determine best chart type."""
        
        if len(columns) == 1:
            return ChartType.TABLE
        
        # Check if we have numeric columns
        numeric_cols = []
        categorical_cols = []
        
        for col in columns:
            sample_values = [row[col] for row in data[:10] if row.get(col) is not None]
            if not sample_values:
                continue
            
            if all(isinstance(v, (int, float)) for v in sample_values):
                numeric_cols.append(col)
            else:
                categorical_cols.append(col)
        
        # Decision logic
        if len(categorical_cols) == 1 and len(numeric_cols) >= 1:
            # One category + numeric values -> Bar chart
            unique_categories = len(set(row[categorical_cols[0]] for row in data if row.get(categorical_cols[0])))
            if unique_categories <= 10:
                return ChartType.BAR
            elif unique_categories <= 5:
                return ChartType.PIE
        
        if len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
            # Category + multiple numeric -> Bar chart
            return ChartType.BAR
        
        # Check if data looks like time series
        first_col = columns[0]
        if any(keyword in first_col.lower() for keyword in ['date', 'time', 'year', 'month', 'day']):
            return ChartType.LINE
        
        # Default to table
        return ChartType.TABLE
    
    def _generate_chart_config(
        self,
        data: List[Dict[str, Any]],
        columns: List[str],
        chart_type: ChartType
    ) -> ChartConfig:
        """Generate chart configuration."""
        
        if chart_type == ChartType.TABLE:
            return ChartConfig(
                chart_type=ChartType.TABLE,
                title="Data Table",
                description=f"Showing {len(data)} rows"
            )
        
        # Identify categorical and numeric columns
        numeric_cols = []
        categorical_cols = []
        
        for col in columns:
            sample_values = [row[col] for row in data[:10] if row.get(col) is not None]
            if sample_values and all(isinstance(v, (int, float)) for v in sample_values):
                numeric_cols.append(col)
            else:
                categorical_cols.append(col)
        
        if chart_type == ChartType.BAR:
            if categorical_cols and numeric_cols:
                x_col = categorical_cols[0]
                y_cols = numeric_cols[:3]  # Max 3 series
                
                return ChartConfig(
                    chart_type=ChartType.BAR,
                    x_axis=x_col,
                    y_axis=y_cols,
                    title=f"{', '.join(y_cols)} by {x_col}",
                    description=f"Bar chart showing {len(data)} categories"
                )
        
        elif chart_type == ChartType.LINE:
            if len(columns) >= 2:
                x_col = columns[0]
                y_cols = numeric_cols if numeric_cols else columns[1:2]
                
                return ChartConfig(
                    chart_type=ChartType.LINE,
                    x_axis=x_col,
                    y_axis=y_cols,
                    title=f"{', '.join(y_cols)} over {x_col}",
                    description=f"Line chart showing trend across {len(data)} points"
                )
        
        elif chart_type == ChartType.PIE:
            if categorical_cols and numeric_cols:
                label_col = categorical_cols[0]
                value_col = numeric_cols[0]
                
                # Get labels and values
                labels = [str(row[label_col]) for row in data if row.get(label_col)]
                values = [float(row[value_col]) for row in data if row.get(value_col) is not None]
                
                return ChartConfig(
                    chart_type=ChartType.PIE,
                    labels=labels[:10],  # Max 10 slices
                    values=values[:10],
                    title=f"{value_col} Distribution",
                    description=f"Pie chart showing distribution across {len(labels[:10])} categories"
                )
        
        # Fallback to table
        return ChartConfig(
            chart_type=ChartType.TABLE,
            title="Data Table",
            description=f"Showing {len(data)} rows"
        )


# Global visualization service instance
visualization_service = VisualizationService()
