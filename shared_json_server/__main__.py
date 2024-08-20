import sys
import pathlib
import logging
import logging.handlers
from .server_main import SharedJsonServer


logger = logging.getLogger(__name__)
config = {
    "host": "localhost",
    "port": 10000,
    "data_dir": "./data",
    "log_dir": "./log",
    "log_level": logging.INFO
}
arg_key_map = {
    "-h":{
        "key":"host",
        "type":str
    },
    "-p":{
        "key":"port",
        "type":int
    },
    "-d":{
        "key":"data_dir",
        "type":str
    },
    "-l":{
        "key":"log_dir",
        "type":str
    },
    "-ll":{
        "key":"log_level",
        "type":int
    }
}

def main():
    init_args()
    init_logging()
    try:
        logger.info("start")
        logger.debug("config:%s",config)
        server = SharedJsonServer(config["host"],config["port"],config["data_dir"])
        server.run_forever()
    except Exception as ex:
        logger.exception(ex)
    finally:
        logger.info("end")

def init_args():
    global config
    if len(sys.argv) > 1 and len(sys.argv) % 2 == 1:
        for i in range(1,len(sys.argv),2):
            arg_key = sys.argv[i]
            value = sys.argv[i+1]
            if arg_key in arg_key_map:
                key = arg_key_map[arg_key]["key"]
                key_type = arg_key_map[arg_key]["type"]
                if key_type == str:
                    config[key] = value
                elif key_type == int:
                    config[key] = int(value)

def init_logging():
    log_dir = pathlib.Path(config["log_dir"])
    if not log_dir.exists():
        log_dir.mkdir()
    if not log_dir.is_dir():
        raise Exception("log path is not dir:" + log_dir)
    
    log_txt = log_dir / 'main.log'
    rh = logging.handlers.RotatingFileHandler(
        log_txt, encoding='utf-8', mode='a',
        maxBytes=1000000, backupCount=5,
        )
    logging.basicConfig(
            level=config["log_level"],
            format='{asctime} [{levelname:.4}] {name}: {message}',
            style='{',
            handlers=[rh])


if __name__ == '__main__':
    main()