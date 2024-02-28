from fastapi import FastAPI
from uvicorn import run

from config_parsing import ConfigParser, EnvConfigParser
from v1 import ApplicationV1

if __name__ == '__main__':
    config_parser: ConfigParser = EnvConfigParser()

    app: FastAPI = FastAPI()
    app_v1: FastAPI = ApplicationV1()
    app.mount('/v1', app_v1)

    run(app=app, host=config_parser.parse_host(), port=config_parser.parse_port())
