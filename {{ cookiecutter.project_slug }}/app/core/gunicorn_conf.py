import multiprocessing
import os

from tabulate import tabulate

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind = os.getenv("BIND", f"{host}:{port}")

workers_per_core = int(os.getenv("WORKERS_PER_CORE", "1"))
worker_tmp_dir = "/dev/shm"

max_workers_str = os.getenv("MAX_WORKERS")
max_workers = int(max_workers_str) if max_workers_str else None
cores = multiprocessing.cpu_count()

default_workers = cores * workers_per_core
workers = min(max_workers, default_workers) if max_workers else default_workers

loglevel = os.getenv("LOG_LEVEL", "info")
accesslog_var = os.getenv("ACCESS_LOG", "-")
accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
errorlog = errorlog_var or None

graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

print(
    """
    ░██████╗░██╗░░░██╗███╗░░██╗██╗░█████╗░░█████╗░██████╗░███╗░░██╗
    ██╔════╝░██║░░░██║████╗░██║██║██╔══██╗██╔══██╗██╔══██╗████╗░██║
    ██║░░██╗░██║░░░██║██╔██╗██║██║██║░░╚═╝██║░░██║██████╔╝██╔██╗██║
    ██║░░╚██╗██║░░░██║██║╚████║██║██║░░██╗██║░░██║██╔══██╗██║╚████║
    ╚██████╔╝╚██████╔╝██║░╚███║██║╚█████╔╝╚█████╔╝██║░░██║██║░╚███║
    ░╚═════╝░░╚═════╝░╚═╝░░╚══╝╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝
    """
)

table_rows = [
    ("Host", host),
    ("Port", port),
    ("Workers Per Core", workers_per_core),
    ("Max Workers", max_workers),
    ("Workers", workers),
    ("Log Level", loglevel),
    ("Access Log", accesslog),
    ("Error Log", errorlog),
    ("Graceful Timeout", graceful_timeout_str),
    ("Timeout", timeout_str),
    ("Keep Alive", keepalive_str),
]

print(tabulate(table_rows, headers=["Name", "Value"]))
