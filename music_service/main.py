from fastapi import FastAPI
from uvicorn import run

from config_parsing import ConfigParser
from application import Application
from v1 import ApplicationV1

if __name__ == '__main__':
    config_parser = ConfigParser()

    port: int = config_parser.parse_port() or 8888
    host: str = config_parser.parse_host() or '127.0.0.1'

    app_v1: Application = ApplicationV1()
    app: FastAPI = FastAPI(on_startup=[app_v1.on_startup], on_shutdown=[app_v1.on_shutdown])
    app.mount('/v1', app_v1)

    run(app=app, port=port, host=host)
