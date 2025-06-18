# Bind to all interfaces so Nginx server can access it
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
keepalive = 2

# Security and performance
preload_app = True
max_worker_connections = 1000
worker_tmp_dir = "/dev/shm"