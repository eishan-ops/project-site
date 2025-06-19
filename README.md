# project-site

This is project site 

This repository has frontend and backend code 

The front end is a simple HTML and JavaScript and is back by an Nginx web server. (index.html, nginx.conf)

Backend is backed by Python and FastAPI (main.py, supervisord.conf[for docker], gunicorn WSGI[for ec2 vms])

All of the above is containerized with the help of Dockerfile under `docker-implementation` directory.

## Running the code 
### Docker
`cp index.html docker-implementation`  

`cp main.py docker-implementation`  

`cd docker-implementation`  

`docker build -t nginx-fastapi-search`  

`docker run -d -p 8080:80 nginx-fastapi-search`  

The docker implementation uses supervisord as the process manager for managing multiple processes inside a single container,
this should only be used for testing purposes of new features

### EC2 
Purpose is to simulate a live production environment.  
Nginx webserver holds the `index.html` file and the project-site config under `sites-available/project-site`  
Application server has the gunicorn WSGI configuration under `opt/project-site/gunicorn.conf.py` ,   
Application server has a systemd service that boots up and enables fastAPI whose configuration can be found under `etc/systemd/system/project-site.service`

## Latest Docker build 

Latest build can be found in docker hub `project-site:poc-2.1.0`

Build now directory tree structure when a file is searched. This appears at the left thand side of the view port.

Files are now (OR have to be) organized in a directory format for the directory tree structure to render correctly to the front end.

Search results now are displayed in tabulated manner instead of blue hyperlinks.

Color enhancements and icons in the directory tree structure.

When the file is being viewed, 'back to welcome page' button is still available for user to get back to the welcome/home page. 

## What's next
This repository is only meant for Application code and not for configuration files. In further interations, these config files will be moved to a config management repo.

As of now , Web and application concerns have been separated, but we will continue to maintain `docker-implementation` under this repo.

All new application features and enhancements will be carried out in this repo. 

All new Infrastructure and Config managements changes , please refer to other repos. 

## What's next in application implementation tips

### Performance with many many files : 

Add pagination to the directory structure API 
Cache the directory structure to avoid frequent s3 list requests 
consider limiting the depth of the directory tree (lower priority)

### Filtering :

we could add options to filter the tree by file type or name 

### S3 Bucket Organization :

Using bucket prefixes to separate different types of content

Adding metadata to s3 objects for additional file information 

setting approiate s3 lifecycles policies for cost management

you might want to keep the number of files from small to medium 