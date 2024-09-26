# to run the dockerized workload 
# cd to the location of the dockerfile and 

docker build -t nginx-fastapi-search .
docker run -d -p 8080:80 nginx-fastapi-search
