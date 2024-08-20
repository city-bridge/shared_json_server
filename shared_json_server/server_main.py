import logging
import logging.handlers
from .shared_data_manager import SharedDataManager
from .json_schema_manage import validate_jsonrpc_request_method
import cbpyjsonrpc

logger = logging.getLogger(__name__)
class SharedJsonServer (cbpyjsonrpc.JsonRPCServerUDP):
    def __init__(self,host:str, port:int, data_dir:str) -> None:
        super().__init__(host, port)
        self._init_func()
        self.shared_data_manager = SharedDataManager(data_path=data_dir)

    
    def _validate_request(self, request):
        validate_jsonrpc_request_method(request)
    
    def _init_func(self):
        #common methods
        self.set_method('debug_notify',lambda param:self.method_debug_notify(param))
        self.set_method('echo',lambda param:self.method_echo(param))
        self.set_method('echo_error',lambda param:self.method_echo_error(param))
        self.set_method('server_stop',lambda param:self.method_server_stop(param))
        #shared data methods
        self.set_method('get_data_name_tree',lambda param:self.method_get_data_name_tree(param))
        self.set_method('get_data',lambda param:self.method_get_data(param))
        self.set_method('set_data',lambda param:self.method_set_data(param))
        self.set_method('read_data',lambda param:self.method_read_data(param))
        self.set_method('write_data',lambda param:self.method_write_data(param))
        self.set_method('read_schema',lambda param:self.method_read_schema(param))
        self.set_method('write_schema',lambda param:self.method_write_schema(param))
        self.set_method('lock_data',lambda param:self.method_lock_data(param))
        self.set_method('release_data',lambda param:self.method_release_data(param))

    '''-------------------------------------------------------------
    common methods
    '''
    def method_server_stop(self,params:dict)->None:
        logger.info('stop requeset received')
        self.stop_request()
        return None

    def method_debug_notify(self,params:dict)->None:
        for param in params:
            logger.info('debug notify:%s', param)
        return None

    def method_echo(self,params:dict)->dict:
        return params

    def method_echo_error(self,params:dict):
        raise Exception('error echo')

    '''-------------------------------------------------------------
    shared data methods
    '''
    def method_get_data_name_tree(self,params:dict)->dict:
        return self.shared_data_manager.get_data_name_tree()

    def method_set_data(self,params:dict)->dict:
        data_name = params['data_name']
        data = params['data']
        lock_name = None
        if 'lock_name' in params:
            lock_name = params['lock_name']
        
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.throw_excpet_if_locked(lock_name)
        shd.data = data

    def method_get_data(self,params:dict)->dict:
        data_name = params['data_name']
        lock_name = None
        if 'lock_name' in params:
            lock_name = params['lock_name']
        
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.throw_excpet_if_locked(lock_name)
        return shd.data

    def method_write_data(self,params:dict)->dict:
        data_name = params['data_name']
        data = params['data']
        lock_name = None
        if 'lock_name' in params:
            lock_name = params['lock_name']
        
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.throw_excpet_if_locked(lock_name)
        shd.write_data(data)

    def method_read_data(self,params:dict)->dict:
        data_name = params['data_name']
        lock_name = None
        if 'lock_name' in params:
            lock_name = params['lock_name']
        
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.throw_excpet_if_locked(lock_name)
        return shd.read_data()

    def method_write_schema(self,params:dict)->dict:
        data_name = params['data_name']
        schema = params['schema']
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.write_schema(schema)
        return None

    def method_read_schema(self,params:dict)->dict:
        data_name = params['data_name']
        shd = self.shared_data_manager.get_data_obj(data_name)
        return shd.read_schema()

    def method_lock_data(self,params:dict)->dict:
        data_name = params['data_name']
        lock_name = params['lock_name']
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.lock_data(lock_name)
        return {
            'locked':shd.is_locked(lock_name),
            'lock_name':shd.lock_name
        }

    def method_release_data(self,params:dict)->dict:
        data_name = params['data_name']
        lock_name = params['lock_name']
        shd = self.shared_data_manager.get_data_obj(data_name)
        shd.release_data(lock_name)
        return {
            'locked':shd.is_locked(lock_name),
            'lock_name':shd.lock_name
        }

