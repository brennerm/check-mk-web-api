# check-mk-web-api

##Quickstart
####Initialization
```
api = WebApi('http://checkmk.company.com/check_mk/webapi.py', username='automation', secret='123456')
```

####Add Host
```
>>> api.add_host('webserver00.com')
```

####Edit Host
```
>>> api.edit_host('webserver00.com', ipaddress='192.168.0.100')
```

####Delete Host
```
>>> api.delete_host('webserver00.com')
```

####Get Host
```
>>> api.get_host('webserver00.com')
{
    'hostname': 'webserver00.com',
    'attributes': {
        'ipaddress': '192.168.0.100'
    },
    'path': ''
}
```

####Get All Hosts
```
>>> api.get_all_hosts()
{
    'webserver00.com': {
        'hostname': 'webserver00.com',
        'attributes': {
            'ipaddress': '192.168.0.100'
        },
        'path': ''
    },
    'webserver01.com': {
        'hostname': 'webserver01.com',
        'attributes': {
            'ipaddress': '192.168.0.101'
        },
        'path': ''
    }
}
```

####Discover Services
```
>>> api.discover_services('webserver00.com')
{'removed': '0', 'new_count': '16', 'added': '16', 'kept': '0'}
```

####Bake Agents
```
>>> api.bake_agents()
```

####Activate Changes
```
>>> api.activate_changes()
```
