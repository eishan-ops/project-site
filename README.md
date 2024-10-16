# project-site

This is project site 

This repository has frontend and backend code 

The front end is a simple HTML and JavaScript and is back by an Nginx web server. (index.html, nginx.conf)

Backend is backed by Python and FastAPI (main.py, supervisord.conf)

All of the above is containerized with the help of Dockerfile.

## Running the code 

`docker build -t nginx-fastapi-search`
`docker run -d -p 8080:80 nginx-fastapi-search`

## Latest build 

Latest build can be found in docker hub `project-site:poc-2.0.0`

Build now has s3 integration, search bar takes a search term, then Python-fastAPI connects to an s3 backend and returns the name of the S3 object , in which the user search term was found.

The file name in which user search term was found now can be clicked and the file can be viewed as is. 

When the file is being viewed, 'back to welcome page' button is now available for user to get back to the welcome/home page. 