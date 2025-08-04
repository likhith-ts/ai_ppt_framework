"""
Data analysis module for understanding datasets and generating insights.

This module analyzes data from various sources to understand patterns,
trends, and generate meaningful insights for presentation creation.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum

from core.exceptions import FrameworkError


class DataType(Enum):
    """Types of data analysis"""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TIME_SERIES = "time_series"
    MIXED = "mixed"


class ChartType(Enum):
    """Recommended chart types for data"""
    BAR_CHART = "bar_chart"
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    HISTOGRAM = "histogram"
    AREA_CHART = "area_chart"
    COLUMN_CHART = "column_chart"
    DONUT_CHART = "donut_chart"


@dataclass
class DataInsight:
    """Represents a data insight for presentation"""
    title: str
    description: str
    chart_type: ChartType
    data: Dict[str, Any]
    key_metrics: Dict[str, Any]  # Changed from Dict[str, float] to Dict[str, Any]
    trend: str  # "increasing", "decreasing", "stable"
    significance: float  # 0-1 score for importance


@dataclass
class DataAnalysisResult:
    """Complete data analysis result"""
    dataset_overview: Dict[str, Any]
    insights: List[DataInsight]
    recommended_charts: List[Dict[str, Any]]
    key_findings: List[str]
    presentation_recommendations: Dict[str, Any]


class DataAnalyzer:
    """
    Analyzes datasets to extract insights and recommend visualizations.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_dataset(self, df: pd.DataFrame, 
                       dataset_name: str = "Dataset") -> DataAnalysisResult:
        """
        Perform comprehensive analysis of a dataset.
        
        Args:
            df: DataFrame to analyze
            dataset_name: Name for the dataset
            
        Returns:
            Complete analysis results
        """
        try:
            # Basic dataset overview
            overview = self._get_dataset_overview(df, dataset_name)
            
            # Extract insights
            insights = self._extract_insights(df)
            
            # Recommend charts
            charts = self._recommend_charts(df, insights)
            
            # Generate key findings
            findings = self._generate_key_findings(df, insights)
            
            # Presentation recommendations
            presentation_recs = self._get_presentation_recommendations(
                df, insights, charts
            )
            
            return DataAnalysisResult(
                dataset_overview=overview,
                insights=insights,
                recommended_charts=charts,
                key_findings=findings,
                presentation_recommendations=presentation_recs
            )
            
        except Exception as e:
            self.logger.error(f"Data analysis failed: {e}")
            raise FrameworkError(f"Data analysis failed: {e}")
    
    def _get_dataset_overview(self, df: pd.DataFrame, 
                             name: str) -> Dict[str, Any]:
        """Get basic overview of the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        return {
            'name': name,
            'rows': len(df),
            'columns': len(df.columns),
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(categorical_cols),
            'column_names': df.columns.tolist(),
            'numeric_column_names': numeric_cols,
            'categorical_column_names': categorical_cols,
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'completeness': ((df.count() / len(df)) * 100).round(1).to_dict()
        }
    
    def _extract_insights(self, df: pd.DataFrame) -> List[DataInsight]:
        """Extract meaningful insights from the data"""
        insights = []
        
        # Analyze numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in df.columns:
                insight = self._analyze_numeric_column(df, col)
                if insight:
                    insights.append(insight)
        
        # Analyze categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in df.columns:
                insight = self._analyze_categorical_column(df, col)
                if insight:
                    insights.append(insight)
        
        # Look for correlations
        if len(numeric_cols) > 1:
            correlation_insights = self._analyze_correlations(df, list(numeric_cols))
            insights.extend(correlation_insights)
        
        # Time series analysis if date column exists
        date_cols = self._detect_date_columns(df)
        if date_cols and numeric_cols:
            time_insights = self._analyze_time_series(df, date_cols, list(numeric_cols))
            insights.extend(time_insights)
        
        return insights
    
    def _analyze_numeric_column(self, df: pd.DataFrame, 
                               col: str) -> Optional[DataInsight]:
        """Analyze a numeric column"""
        try:
            series = df[col].dropna()
            if len(series) == 0:
                return None
            
            # Calculate statistics
            mean_val = series.mean()
            median_val = series.median()
            std_val = series.std()
            
            # Determine trend if data appears ordered
            if len(series) > 2:
                trend = self._calculate_trend(np.array(series.values))
            else:
                trend = "stable"
            
            # Create chart data
            chart_data = {
                'values': series.tolist(),
                'labels': [f"Row {i+1}" for i in range(len(series))],
                'statistics': {
                    'mean': mean_val,
                    'median': median_val,
                    'std': std_val,
                    'min': series.min(),
                    'max': series.max()
                }
            }
            
            return DataInsight(
                title=f"{col} Analysis",
                description=f"Statistical analysis of {col} values",
                chart_type=ChartType.HISTOGRAM,
                data=chart_data,
                key_metrics={
                    'mean': mean_val,
                    'median': median_val,
                    'std_dev': std_val
                },
                trend=trend,
                significance=0.7
            )
        except Exception as e:
            self.logger.warning(f"Failed to analyze column {col}: {e}")
            return None
    
    def _analyze_categorical_column(self, df: pd.DataFrame, 
                                   col: str) -> Optional[DataInsight]:
        """Analyze a categorical column"""
        try:
            value_counts = df[col].value_counts()
            if len(value_counts) == 0:
                return None
            
            # Create chart data
            chart_data = {
                'labels': value_counts.index.tolist(),
                'values': value_counts.values.tolist(),
                'percentages': (value_counts / len(df) * 100).round(1).tolist()
            }
            
            # Determine if suitable for pie chart (not too many categories)
            chart_type = ChartType.PIE_CHART if len(value_counts) <= 6 else ChartType.BAR_CHART
            
            return DataInsight(
                title=f"{col} Distribution",
                description=f"Distribution of values in {col}",
                chart_type=chart_type,
                data=chart_data,
                key_metrics={
                    'unique_values': len(value_counts),
                    'most_common': str(value_counts.index[0]),
                    'most_common_count': float(value_counts.iloc[0])
                },
                trend="stable",
                significance=0.6
            )
        except Exception as e:
            self.logger.warning(f"Failed to analyze column {col}: {e}")
            return None
    
    def _analyze_correlations(self, df: pd.DataFrame, 
                             numeric_cols: List[str]) -> List[DataInsight]:
        """Analyze correlations between numeric columns"""
        insights = []
        try:
            correlation_matrix = df[numeric_cols].corr()
            
            # Find strong correlations
            for i, col1 in enumerate(numeric_cols):
                for j, col2 in enumerate(numeric_cols[i+1:], i+1):
                    try:
                        corr_value = correlation_matrix.loc[col1, col2]
                        if pd.notna(corr_value) and isinstance(corr_value, (int, float)) and abs(corr_value) > 0.7:  # Strong correlation
                            chart_data = {
                                'x_values': df[col1].tolist(),
                                'y_values': df[col2].tolist(),
                                'correlation': float(corr_value)
                            }
                            
                            insights.append(DataInsight(
                                title=f"{col1} vs {col2} Correlation",
                                description=f"Strong correlation ({corr_value:.2f}) between {col1} and {col2}",
                                chart_type=ChartType.SCATTER_PLOT,
                                data=chart_data,
                                key_metrics={'correlation': float(corr_value)},
                                trend="correlated",
                                significance=0.8
                            ))
                    except (TypeError, ValueError):
                        continue
        except Exception as e:
            self.logger.warning(f"Correlation analysis failed: {e}")
        
        return insights
    
    def _detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that might contain dates"""
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to parse a sample as date
                try:
                    pd.to_datetime(df[col].dropna().iloc[0])
                    date_cols.append(col)
                except:
                    continue
        return date_cols
    
    def _analyze_time_series(self, df: pd.DataFrame, 
                            date_cols: List[str], 
                            numeric_cols: List[str]) -> List[DataInsight]:
        """Analyze time series data"""
        insights = []
        for date_col in date_cols:
            for numeric_col in numeric_cols:
                try:
                    # Create time series data
                    ts_df = df[[date_col, numeric_col]].dropna()
                    ts_df[date_col] = pd.to_datetime(ts_df[date_col])
                    ts_df = ts_df.sort_values(date_col)
                    
                    if len(ts_df) > 2:
                        trend = self._calculate_trend(np.array(ts_df[numeric_col].values))
                        
                        chart_data = {
                            'dates': ts_df[date_col].dt.strftime('%Y-%m-%d').tolist(),
                            'values': ts_df[numeric_col].tolist()
                        }
                        
                        insights.append(DataInsight(
                            title=f"{numeric_col} Over Time",
                            description=f"Time series analysis of {numeric_col}",
                            chart_type=ChartType.LINE_CHART,
                            data=chart_data,
                            key_metrics={
                                'start_value': ts_df[numeric_col].iloc[0],
                                'end_value': ts_df[numeric_col].iloc[-1],
                                'change': ts_df[numeric_col].iloc[-1] - ts_df[numeric_col].iloc[0]
                            },
                            trend=trend,
                            significance=0.9
                        ))
                except Exception as e:
                    self.logger.warning(f"Time series analysis failed for {date_col}, {numeric_col}: {e}")
                    continue
        
        return insights
    
    def _calculate_trend(self, values: np.ndarray) -> str:
        """Calculate trend direction from values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _recommend_charts(self, df: pd.DataFrame, 
                         insights: List[DataInsight]) -> List[Dict[str, Any]]:
        """Recommend chart types and configurations"""
        recommendations = []
        
        for insight in insights:
            recommendation = {
                'title': insight.title,
                'chart_type': insight.chart_type.value,
                'data': insight.data,
                'description': insight.description,
                'confidence': insight.significance
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_key_findings(self, df: pd.DataFrame, 
                              insights: List[DataInsight]) -> List[str]:
        """Generate key findings from the analysis"""
        findings = []
        
        # Dataset size finding
        findings.append(f"Dataset contains {len(df)} records with {len(df.columns)} columns")
        
        # Missing data finding
        missing_data = df.isnull().sum().sum()
        if missing_data > 0:
            findings.append(f"Dataset has {missing_data} missing values requiring attention")
        
        # Top insights
        sorted_insights = sorted(insights, key=lambda x: x.significance, reverse=True)
        for insight in sorted_insights[:3]:  # Top 3 insights
            if insight.trend != "stable":
                findings.append(f"{insight.title}: Shows {insight.trend} trend")
        
        return findings
    
    def _get_presentation_recommendations(self, df: pd.DataFrame,
                                        insights: List[DataInsight],
                                        charts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate recommendations for presentation structure"""
        return {
            'suggested_slides': len(charts) + 2,  # Charts + overview + summary
            'chart_slides': len(charts),
            'overview_slide': True,
            'summary_slide': True,
            'recommended_layout': 'data_focused',
            'color_scheme': 'professional_blue',
            'emphasis': 'data_visualization'
        }
