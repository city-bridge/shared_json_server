import logging
import logging.handlers
import shared_data_manager
import json_schema_manage
import cbpyjsonrpc
import config
import pathlib

logger = logging.getLogger(__name__)
class SharedJsonServer (cbpyjsonrpc.JsonRPCServerUDP):
    def __init__(self):
        super().__init__(config.SERVER_HOST,config.SERVER_PORT)
    
    def _validate_request(self, request):
        json_schema_manage.validate_jsonrpc_request_method(request)
        
server = SharedJsonServer()
def main():
    init_logging()
    init_methods(server)
    try:
        logger.info("start")
        server.run_forever()
    except Exception as ex:
        logger.exception(ex)
    finally:
        logger.info("end")

def init_logging():
    log_dir = pathlib.Path(config.LOG_DIR)
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
            level=config.LOGGING_LEVEL,
            format='{asctime} [{levelname:.4}] {name}: {message}',
            style='{',
            handlers=[rh])

def init_methods(server:cbpyjsonrpc.JsonRPCServerUDP):
    #common methods
    server.set_method('debug_notify',method_debug_notify)
    server.set_method('echo',method_echo)
    server.set_method('echo_error',method_echo_error)
    server.set_method('server_stop',method_server_stop)

    #shared data methods
    server.set_method('get_data_name_tree',method_get_data_name_tree)
    server.set_method('get_data',method_get_data)
    server.set_method('set_data',method_set_data)
    server.set_method('read_data',method_read_data)
    server.set_method('write_data',method_write_data)
    server.set_method('read_schema',method_read_schema)
    server.set_method('write_schema',method_write_schema)
    server.set_method('lock_data',method_lock_data)
    server.set_method('release_data',method_release_data)

'''-------------------------------------------------------------
common methods
'''
def method_server_stop(params:dict)->None:
    logger.info('stop requeset received')
    server.stop_request()
    return None

def method_debug_notify(params:dict)->None:
    for param in params:
        logger.info('debug notify:%s', param)
    return None

def method_echo(params:dict)->dict:
    return params

def method_echo_error(params:dict):
    raise Exception('error echo')

'''-------------------------------------------------------------
shared data methods
'''
def method_get_data_name_tree(params:dict)->dict:
    return shared_data_manager.get_data_name_tree()

def method_set_data(params:dict)->dict:
    data_name = params['data_name']
    data = params['data']
    lock_name = None
    if 'lock_name' in params:
        lock_name = params['lock_name']
    
    shd = shared_data_manager.get_data_obj(data_name)
    shd.throw_excpet_if_locked(lock_name)
    shd.data = data

def method_get_data(params:dict)->dict:
    data_name = params['data_name']
    lock_name = None
    if 'lock_name' in params:
        lock_name = params['lock_name']
    
    shd = shared_data_manager.get_data_obj(data_name)
    shd.throw_excpet_if_locked(lock_name)
    return shd.data

def method_write_data(params:dict)->dict:
    data_name = params['data_name']
    data = params['data']
    lock_name = None
    if 'lock_name' in params:
        lock_name = params['lock_name']
    
    shd = shared_data_manager.get_data_obj(data_name)
    shd.throw_excpet_if_locked(lock_name)
    shd.write_data(data)

def method_read_data(params:dict)->dict:
    data_name = params['data_name']
    lock_name = None
    if 'lock_name' in params:
        lock_name = params['lock_name']
    
    shd = shared_data_manager.get_data_obj(data_name)
    shd.throw_excpet_if_locked(lock_name)
    return shd.read_data()

def method_write_schema(params:dict)->dict:
    data_name = params['data_name']
    schema = params['schema']
    shd = shared_data_manager.get_data_obj(data_name)
    shd.write_schema(schema)
    return None

def method_read_schema(params:dict)->dict:
    data_name = params['data_name']
    shd = shared_data_manager.get_data_obj(data_name)
    return shd.read_schema()

def method_lock_data(params:dict)->dict:
    data_name = params['data_name']
    lock_name = params['lock_name']
    shd = shared_data_manager.get_data_obj(data_name)
    shd.lock_data(lock_name)
    return {
        'locked':shd.is_locked(lock_name),
        'lock_name':shd.lock_name
    }

def method_release_data(params:dict)->dict:
    data_name = params['data_name']
    lock_name = params['lock_name']
    shd = shared_data_manager.get_data_obj(data_name)
    shd.release_data(lock_name)
    return {
        'locked':shd.is_locked(lock_name),
        'lock_name':shd.lock_name
    }

main()