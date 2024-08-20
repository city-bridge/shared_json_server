import logging
import pathlib
import json
import jsonschema

logger = logging.getLogger(__name__)

class SharedDataException (Exception):
    pass

class SharedData:
    data_name:str
    lock_name:str
    data:dict
    base_dir:pathlib.Path

    def __init__(self,base_dir_path:str,data_name:str) -> None:
        self.lock_name = None
        self.data = None
        self.data_name = data_name
        self.base_dir = self._data_name_to_base_dir(base_dir_path,data_name)
    
    def set_data(self,data:dict):
        tmp_schema = self.read_schema()
        if tmp_schema != None:
            jsonschema.validate(data,tmp_schema)
        if self.schema != None:
            jsonschema.validate(data,self.schema)
        self.data = data

    def get_data(self)->dict:
        return self.data
    
    def is_locked(self,lock_name:str)->bool:
        locked = False
        if self.lock_name != None:
            if self.lock_name != lock_name:
                locked = True
        return locked

    def throw_excpet_if_locked(self,lock_name:str):
        if self.is_locked(lock_name):
            raise SharedDataException('data_name:'+ self.data_name + 'is locked'  + ' by:' + self.lock_name)
    
    def lock_data(self,lock_name:str):
        if not self.is_locked(lock_name):
            self.lock_name = lock_name

    def release_data(self,lock_name:str)->bool:
        if not self.is_locked(lock_name):
            self.lock_name = None

    def _data_name_to_base_dir(self,base_dir_path:str,data_name:str)->pathlib.Path:
        base_dir = pathlib.Path(base_dir_path)
        if not base_dir.exists():
            raise SharedDataException('data dir is not exists:' + str(base_dir))
        if not base_dir.is_dir():
            raise SharedDataException('data dir is not directory:' + str(base_dir))

        for name in data_name.split('/'):
            if len(name) == 0:
                continue
            base_dir = base_dir / name
            if not base_dir.exists():
                base_dir.mkdir()
            
            if not base_dir.is_dir():
                raise SharedDataException('error dir:' + str(base_dir))
        return base_dir

    def _data_name_to_path(self)->pathlib.Path:
        return self.base_dir / 'data.json'

    def _data_name_to_schema_path(self)->pathlib.Path:
        return self.base_dir / 'schema.json'

    def _data_name_to_default_data_path(self)->pathlib.Path:
        return self.base_dir / 'default.json'

    def write_data(self,data:dict):
        tmp_schema = self.read_schema()
        if tmp_schema != None:
            jsonschema.validate(data,tmp_schema)
        file_path = self._data_name_to_path()
        with file_path.open('w',encoding='utf8') as f:
            json.dump(data,f)

    def read_data(self)->dict:
        file_path = self._data_name_to_path()
        ret = None
        if file_path.exists():
            with file_path.open('r',encoding='utf8') as f:
                ret = json.load(f)
        return ret
    
    def save_data(self):
        self.write_data(self.data)
    
    def load_data(self):
        self.data = self.read_data()
    
    def write_schema(self,schema:dict):
        file_path = self._data_name_to_schema_path()
        with file_path.open('w',encoding='utf8') as f:
            json.dump(schema,f)
    
    def read_schema(self)->dict:
        file_path = self._data_name_to_schema_path()
        ret = None
        if file_path.exists():
            with file_path.open('r',encoding='utf8') as f:
                ret = json.load(f)
        return ret
    
    def write_default_data(self,default_data:dict):
        tmp_schema = self.read_schema()
        if tmp_schema != None:
            jsonschema.validate(default_data,tmp_schema)
        file_path = self._data_name_to_default_data_path()
        with file_path.open('w',encoding='utf8') as f:
            json.dump(default_data,f)
    
    def read_default_data(self)->dict:  
        file_path = self._data_name_to_default_data_path()
        ret = None
        if file_path.exists():
            with file_path.open('r',encoding='utf8') as f:
                ret = json.load(f)
        return ret

class SharedDataManager:
    _AllData:dict
    data_path:str
    def __init__(self,data_path:str) -> None:
        self._AllData = {}
        self.data_path = data_path

    def get_data_obj(self, data_name:str)->SharedData:
        if data_name in self._AllData:
            shd = self._AllData[data_name]
        else:
            shd = SharedData(self.data_path,data_name)
            self._AllData[data_name] = shd
        return shd

    def get_data_names(self)->list:
        return list(self._AllData.keys())

    def get_data_name_tree(self)->dict:
        ret = {}
        for name in self.get_data_names():
            tmp = ret
            for n in name.split('/'):
                if len(n) == 0:
                    continue
                if n not in tmp:
                    tmp[n] = {}
                tmp = tmp[n]
        return ret