# fast API AWS s3 implementation : 
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import logging
from urllib.parse import unquote

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

@app.get("/api/file-contents/{file_name:path}")
async def get_file_contents(file_name: str):
    # Decode the URL-encoded file name
    decoded_file_name = unquote(file_name)
    logger.info(f"Attempting to fetch file: {decoded_file_name}")
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=decoded_file_name)
        content = response['Body'].read().decode('utf-8')
        logger.info(f"Successfully fetched file: {decoded_file_name}")
        return content
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found")
        else:
            raise HTTPException(status_code=500, detail="Error retrieving file")
