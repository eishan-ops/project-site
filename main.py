from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Sample data for demonstration
sample_texts = [
    "The quick brown fox jumps over the lazy dog",
    "Python is a versatile programming language",
    "FastAPI provides fast performance for production",
    "Text search can be implemented in various ways"
]

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    results: List[str]

@app.post("/search", response_model=SearchResult)
async def search(query: SearchQuery):
    if not query.query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    # Simple case-insensitive search
    results = [text for text in sample_texts if query.query.lower() in text.lower()]
    
    return SearchResult(results=results)

# Note: We've removed the `if __name__ == "__main__":` block as we'll be using Gunicorn to run the app

## fast API AWS s3 implementation : 
# import boto3
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import os

# app = FastAPI()

# # AWS S3 configuration
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
# S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# # Initialize S3 client
# s3_client = boto3.client('s3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     region_name=AWS_REGION
# )

# class SearchQuery(BaseModel):
#     query: str

# class SearchResult(BaseModel):
#     results: List[str]

# @app.post("/search", response_model=SearchResult)
# async def search(query: SearchQuery):
#     if not query.query:
#         raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
#     try:
#         # List all objects in the bucket
#         response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        
#         results = []
#         for obj in response.get('Contents', []):
#             # Get the object content
#             file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])['Body'].read().decode('utf-8')
            
#             # Perform a simple case-insensitive search
#             if query.query.lower() in file_content.lower():
#                 results.append(f"Match found in document: {obj['Key']}")
        
#         return SearchResult(results=results)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# # Optional: Add an endpoint to upload documents to S3
# @app.post("/upload")
# async def upload_document(filename: str, content: str):
#     try:
#         s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=content)
#         return {"message": f"Document {filename} uploaded successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


### before running docker container :
### Before running the container, you need to provide the AWS credentials and S3 bucket name as environment variables. You can do this when running the Docker container:
# docker run -d -p 80:80 \
#   -e AWS_ACCESS_KEY_ID=your_access_key \
#   -e AWS_SECRET_ACCESS_KEY=your_secret_key \
#   -e AWS_REGION=your_region \
#   -e S3_BUCKET_NAME=your_bucket_name \
#   nginx-fastapi-s3-search