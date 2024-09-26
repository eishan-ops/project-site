# project-site

This is project site 

This repository has frontend and backend code 

The front end is a simple HTML and JavaScript and is back by an Nginx web server. (index.html, nginx.conf)

Backend is backed by Python and FastAPI (main.py, supervisord.conf)

All of the above is containerized with the help of Dockerfile.

## Running the code 

`docker build -t nginx-fastapi-search`
`docker run -d -p 8080:80 nginx-fastapi-search`

