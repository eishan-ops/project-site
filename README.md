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

Latest build can be found in docker hub `project-site:poc-2.1.0`

Build now directory tree structure when a file is searched. This appears at the left thand side of the view port.

Files are now (OR have to be) organized in a directory format for the directory tree structure to render correctly to the front end.

Search results now are displayed in tabulated manner instead of blue hyperlinks.

Color enhancements and icons in the directory tree structure.

When the file is being viewed, 'back to welcome page' button is still available for user to get back to the welcome/home page. 