# to run the dockerized workload 
# cd to the location of the dockerfile and 

docker build -t nginx-fastapi-search .
docker run -d -p 8080:80 nginx-fastapi-search


# pushing images to docker hub : 
docker tag nginx-fastapi-search:latest eishanops/project-site:poc-1.0.0
docker push eishanops/project-site:poc-1.0.0