import multiprocessing

bind = "0.0.0.0:8000"
max_requests = 1000
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
# reload_extra_file = ["./templates/**"]
certfile = "cert.pem"
keyfile = "key.pem"
