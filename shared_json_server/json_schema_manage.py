from jsonschema import validate, ValidationError
import cbpyjsonrpc.jsonrpc_exception as jsonrpc_exception
import json_schema_def

_schema_list = [
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_LOCK,
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_RELEASE,
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_READ_DATA,
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_WRITE_DATA,
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_GET_DATA,
    json_schema_def.JSON_SCHEMA_REQUEST_METHOD_SET_DATA
]
_schema_jsonrpc_request_methods = {}
for schema in _schema_list:
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


