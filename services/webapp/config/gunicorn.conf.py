from alpha.dirs import DIR_APP

bind = "0.0.0.0:80"
chdir = DIR_APP.as_posix()
graceful_timeout = 30
max_requests = 200
max_requests_jitter = 20
pythonpath = DIR_APP.as_posix()
reload = False
timeout = graceful_timeout * 2
worker_class = "uvicorn.workers.UvicornH11Worker"
workers = 4
