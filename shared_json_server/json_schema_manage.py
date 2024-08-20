from jsonschema import validate, ValidationError
import cbpyjsonrpc.jsonrpc_exception as jsonrpc_exception
from .json_schema_def import JSON_SCHEMA_REQUEST_METHOD_LIST

_schema_jsonrpc_request_methods = {}
for schema in JSON_SCHEMA_REQUEST_METHOD_LIST:
    _schema_jsonrpc_request_methods[schema['properties']['method']['const']] = schema


def validate_jsonrpc_request_method(data):
    method_name = data['method']
    schema = None
    if method_name in _schema_jsonrpc_request_methods:
        schema = _schema_jsonrpc_request_methods[method_name]
    
    if schema != None:
        err_msg = None
        try:
            validate(data,schema)
        except ValidationError as ve:
            err_msg = ' json path="' + ve.json_path + '" msg=' + ve.message
        
        if err_msg != None:
            raise jsonrpc_exception.JsonRPCInvalidParameterError(err_msg)


