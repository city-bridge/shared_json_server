# shared_json_server

## Introduction
* Save Data To Server
  * File or Memory 
* Locked Access Data
* Access UDP
* Json RPC 2.0 format

## inlstall
```
pip install jsonschema
pip install git+https://github.com/city-bridge/cbpyjsonrpc.git
pip install git+https://github.com/city-bridge/shared_json_server.git
```

## start server
```
python3 -m shared_json_server -h localhost -p 10000 -l ./log -d ./data
```
