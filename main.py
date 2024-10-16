# fast API AWS s3 implementation : 
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
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
            # Get the object content as bytes and decode manually
        file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])['Body'].read()
        try:
            # Try UTF-8 first
            decoded_content = file_content.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 if UTF-8 fails
                decoded_content = file_content.decode('latin-1')
            except UnicodeDecodeError:
                logger.warning(f"Could not decode file {obj['Key']}, skipping...")
                continue
            
            # Perform a simple case-insensitive search
        if query.query.lower() in decoded_content.lower():
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
        # Read the content as bytes
        content_bytes = response['Body'].read()
        # Try to detect the content type
        content_type = response.get('ContentType', 'text/plain')
        
        try:
            # Try UTF-8 with BOM first
            content = content_bytes.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 if UTF-8 fails
                content = content_bytes.decode('latin-1')
            except UnicodeDecodeError:
                raise HTTPException(status_code=500, detail="Unable to decode file content")

        # Return a Response object with appropriate headers
        return Response(
            content=content,
            media_type="text/plain",
            headers={
                "Content-Type": "text/plain; charset=utf-8",
                # Prevent any content-type sniffing
                "X-Content-Type-Options": "nosniff",
                # Ensure newlines are preserved
                "White-Space": "pre"
            }
        )
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found")
        else:
            logger.error(f"Error retrieving file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving file")
