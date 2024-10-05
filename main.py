# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# # Sample data for demonstration
# sample_texts = [
#     "The quick brown fox jumps over the lazy dog",
#     "Python is a versatile programming language",
#     "FastAPI provides fast performance for production",
#     "Text search can be implemented in various ways"
# ]

# class SearchQuery(BaseModel):
#     query: str

# class SearchResult(BaseModel):
#     results: List[str]

# @app.post("/search", response_model=SearchResult)
# async def search(query: SearchQuery):
#     if not query.query:
#         raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
#     # Simple case-insensitive search
#     results = [text for text in sample_texts if query.query.lower() in text.lower()]
    
#     return SearchResult(results=results)

# Note: We've removed the `if __name__ == "__main__":` block as we'll be using Gunicorn to run the app

# fast API AWS s3 implementation : 
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import logging
import traceback

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# Initialize S3 client
s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    results: List[str]

@app.post("/search", response_model=SearchResult)
async def search(query: SearchQuery):
    logger.info(f"Received search query: {query.query}")
    if not query.query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    # List all objects in the bucket
    logger.info(f"Listing objects in bucket: {S3_BUCKET_NAME}")
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)

    results = []
    for obj in response.get('Contents', []):
        logger.info(f"Searching in object: {obj['Key']}")
            # Get the object content
        file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])['Body'].read().decode('utf-8')
            
            # Perform a simple case-insensitive search
        if query.query.lower() in file_content.lower():
            results.append(f"Match found in document: {obj['Key']}")

    logger.info(f"Search completed. Found {len(results)} results.")
    return SearchResult(results=results)
