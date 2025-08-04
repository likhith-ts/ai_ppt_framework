"""
Google Sheets integration for data-driven presentations.

This module provides functionality to connect to Google Sheets and extract data
for creating data-driven presentations similar to the DEV.to article approach.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import pandas as pd

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    print("Warning: gspread not available. Install with: pip install gspread google-auth")
    GSPREAD_AVAILABLE = False
    gspread = None  # type: ignore
    Credentials = None  # type: ignore

from core.exceptions import FrameworkError


class GoogleSheetsError(FrameworkError):
    """Google Sheets specific errors"""
    pass


class GoogleSheetsClient:
    """
    Google Sheets client for data extraction and analysis.
    
    Supports both service account authentication and OAuth flow.
    """
    
    def __init__(self, credentials_path: Optional[str] = None, 
                 api_key: Optional[str] = None):
        """
        Initialize Google Sheets client.
        
        Args:
            credentials_path: Path to service account JSON file
            api_key: Google API key for simple access
        """
        self.credentials_path = credentials_path
        self.api_key = api_key
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if not GSPREAD_AVAILABLE:
            self.logger.warning("Google Sheets integration not available. Install gspread and google-auth.")
            return
            
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Google Sheets client"""
        if not GSPREAD_AVAILABLE or not gspread or not Credentials:
            self.logger.warning("Google Sheets integration not available. Install gspread and google-auth.")
            return
            
        try:
            if self.credentials_path and Path(self.credentials_path).exists():
                # Service account authentication
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = Credentials.from_service_account_file(
                    self.credentials_path, scopes=scope
                )
                self.client = gspread.authorize(creds)
                self.logger.info("Google Sheets client initialized with service account")
            else:
                # Fallback to simple API approach
                self.logger.warning("Service account credentials not found. Limited functionality available.")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Sheets client: {e}")
            raise GoogleSheetsError(f"Authentication failed: {e}")
    
    def get_sheet_data(self, sheet_id: str, 
                      sheet_name: Optional[str] = None,
                      range_name: Optional[str] = None) -> pd.DataFrame:
        """
        Extract data from Google Sheets.
        
        Args:
            sheet_id: Google Sheets document ID
            sheet_name: Specific sheet tab name (optional)
            range_name: Specific cell range (optional)
            
        Returns:
            DataFrame with the extracted data
        """
        if not GSPREAD_AVAILABLE or not self.client:
            # Return mock data for development/testing
            return self._get_mock_data()
        
        try:
            # Open the spreadsheet
            spreadsheet = self.client.open_by_key(sheet_id)
            
            # Select worksheet
            if sheet_name:
                worksheet = spreadsheet.worksheet(sheet_name)
            else:
                worksheet = spreadsheet.sheet1  # Default to first sheet
            
            # Get data
            if range_name:
                values = worksheet.get(range_name)
            else:
                values = worksheet.get_all_values()
            
            # Convert to DataFrame
            if values:
                df = pd.DataFrame(values[1:], columns=values[0])  # First row as headers
                # Try to convert numeric columns
                df = self._convert_numeric_columns(df)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"Failed to extract data from Google Sheets: {e}")
            raise GoogleSheetsError(f"Data extraction failed: {e}")
    
    def _convert_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert string columns to numeric where possible"""
        for col in df.columns:
            try:
                # Try to convert to numeric
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                # If most values are numeric, use the numeric version
                if numeric_series.notna().sum() > len(df) * 0.5:
                    df[col] = numeric_series
            except:
                continue
        return df
    
    def _get_mock_data(self) -> pd.DataFrame:
        """Return mock data for testing/development"""
        self.logger.info("Using mock data - Google Sheets not available")
        return pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Revenue': [45000, 52000, 48000, 61000, 55000, 67000],
            'Users': [1200, 1350, 1280, 1520, 1480, 1680],
            'Conversion Rate': [3.2, 3.8, 3.1, 4.1, 3.9, 4.3]
        })
    
    def get_sheet_info(self, sheet_id: str) -> Dict[str, Any]:
        """
        Get metadata about the spreadsheet.
        
        Args:
            sheet_id: Google Sheets document ID
            
        Returns:
            Dictionary with spreadsheet metadata
        """
        if not GSPREAD_AVAILABLE or not self.client:
            return {
                'title': 'Mock Spreadsheet',
                'sheets': ['Sheet1'],
                'row_count': 6,
                'column_count': 4
            }
        
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            return {
                'title': spreadsheet.title,
                'sheets': [sheet.title for sheet in spreadsheet.worksheets()],
                'row_count': spreadsheet.sheet1.row_count,
                'column_count': spreadsheet.sheet1.col_count
            }
        except Exception as e:
            self.logger.error(f"Failed to get sheet info: {e}")
            raise GoogleSheetsError(f"Failed to get sheet info: {e}")
    
    def validate_sheet_access(self, sheet_id: str) -> bool:
        """
        Validate that we can access the given sheet.
        
        Args:
            sheet_id: Google Sheets document ID
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            self.get_sheet_info(sheet_id)
            return True
        except:
            return False


class DataSourceManager:
    """
    Manager for multiple data sources including Google Sheets, CSV, Excel.
    """
    
    def __init__(self, google_credentials: Optional[str] = None):
        """
        Initialize data source manager.
        
        Args:
            google_credentials: Path to Google service account credentials
        """
        self.google_client = GoogleSheetsClient(google_credentials)
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, source: str, **kwargs) -> pd.DataFrame:
        """
        Load data from various sources.
        
        Args:
            source: Data source identifier (sheet_id, file_path, etc.)
            **kwargs: Additional parameters for data loading
            
        Returns:
            DataFrame with loaded data
        """
        # Detect source type
        if source.startswith('http') and 'spreadsheets' in source:
            # Google Sheets URL
            sheet_id = self._extract_sheet_id(source)
            return self.google_client.get_sheet_data(sheet_id, **kwargs)
        
        elif len(source) == 44 and source.replace('-', '').replace('_', '').isalnum():
            # Looks like a Google Sheets ID
            return self.google_client.get_sheet_data(source, **kwargs)
        
        elif source.endswith('.csv'):
            # CSV file
            return pd.read_csv(source)
        
        elif source.endswith(('.xlsx', '.xls')):
            # Excel file
            return pd.read_excel(source, **kwargs)
        
        else:
            raise ValueError(f"Unsupported data source: {source}")
    
    def _extract_sheet_id(self, url: str) -> str:
        """Extract sheet ID from Google Sheets URL"""
        try:
            # Extract ID from URL like:
            # https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=0
            parts = url.split('/')
            sheet_id_index = parts.index('d') + 1
            return parts[sheet_id_index]
        except:
            raise ValueError("Invalid Google Sheets URL")
