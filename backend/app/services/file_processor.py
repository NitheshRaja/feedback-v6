"""
File processing service for CSV/Excel uploads
"""
import pandas as pd
import os
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)


class FileProcessor:
    """Process uploaded CSV/Excel files"""
    
    REQUIRED_COLUMNS = [
        "trainee_id",
        "location",
        "training_batch",
        "rating_score",
        "open_text"
    ]
    
    OPTIONAL_COLUMNS = [
        "category_tags",
        "week_start_date",
        "week_end_date"
    ]
    
    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    async def process_file(self, file: UploadFile) -> Dict:
        """
        Process uploaded file and return structured data
        
        Returns:
            {
                "success": bool,
                "data": List[Dict],
                "errors": List[str],
                "total_rows": int
            }
        """
        try:
            # Save file temporarily
            file_path = os.path.join(self.upload_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Determine file type and read
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return {
                    "success": False,
                    "data": [],
                    "errors": [f"Unsupported file type: {file.filename}"],
                    "total_rows": 0
                }
            
            # Validate columns
            errors = []
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            
            if errors:
                return {
                    "success": False,
                    "data": [],
                    "errors": errors,
                    "total_rows": len(df)
                }
            
            # Normalize column names (handle case variations)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Process data
            processed_data = []
            for idx, row in df.iterrows():
                try:
                    # Extract and validate data
                    record = {
                        "trainee_id": str(row.get("trainee_id", "")).strip(),
                        "location": str(row.get("location", "")).strip(),
                        "training_batch": str(row.get("training_batch", "")).strip(),
                        "rating_score": self._parse_rating(row.get("rating_score")),
                        "open_text": str(row.get("open_text", "")).strip(),
                        "category_tags": str(row.get("category_tags", "")).strip() if pd.notna(row.get("category_tags")) else None,
                    }
                    
                    # Parse dates if provided
                    week_start = row.get("week_start_date")
                    week_end = row.get("week_end_date")
                    
                    if pd.notna(week_start):
                        try:
                            record["week_start_date"] = pd.to_datetime(week_start)
                        except:
                            record["week_start_date"] = None
                    else:
                        record["week_start_date"] = None
                    
                    if pd.notna(week_end):
                        try:
                            record["week_end_date"] = pd.to_datetime(week_end)
                        except:
                            record["week_end_date"] = None
                    else:
                        record["week_end_date"] = None
                    
                    # Validate required fields
                    if not record["trainee_id"] or not record["open_text"]:
                        errors.append(f"Row {idx + 2}: Missing required data")
                        continue
                    
                    processed_data.append(record)
                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")
                    continue
            
            # Clean up temp file
            try:
                os.remove(file_path)
            except:
                pass
            
            return {
                "success": len(errors) == 0 or len(processed_data) > 0,
                "data": processed_data,
                "errors": errors,
                "total_rows": len(df),
                "processed_rows": len(processed_data)
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return {
                "success": False,
                "data": [],
                "errors": [f"Error processing file: {str(e)}"],
                "total_rows": 0
            }
    
    def _parse_rating(self, value) -> Optional[int]:
        """Parse rating score to integer (1-5)"""
        if pd.isna(value):
            return None
        try:
            rating = int(float(value))
            if 1 <= rating <= 5:
                return rating
            return None
        except:
            return None



