# check-mk-web-api [![Build Status](https://travis-ci.org/brennerm/check-mk-web-api.svg?branch=master)](https://travis-ci.org/brennerm/check-mk-web-api)
## supported Checkmk versions
- 1.6.0
- 1.5.0

## Installation
- From source code
```
git clone https://github.com/brennerm/check-mk-web-api
cd check-mk-web-api
sudo python setup.py install
```

- With pip
```
pip install check_mk_web_api
```

## [API Documentation](https://brennerm.github.io/check-mk-web-api/check_mk_web_api/)

## Quickstart
#### Initialization
```
import check_mk_web_api
api = check_mk_web_api.WebApi('http://checkmk.company.com/check_mk/webapi.py', username='automation', secret='123456')
```

#### Add Host
```
>>> api.add_host('webserver00.com')
```

#### Add Host in an existing WATO folder
```
>>> api.add_host('webserver00.com', folder='webservers')
```
Note there is no leading '/' on the folder name.

#### Edit Host
```
>>> api.edit_host('webserver00.com', ipaddress='192.168.0.100')
```

#### Delete Host
```
>>> api.delete_host('webserver00.com')
```

#### Delete Hosts
```
>>> api.delete_hosts(['webserver00.com', 'webserver01.com' ])
```

#### Get Host
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

#### Get All Hosts
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

#### Discover Services
```
>>> api.discover_services('webserver00.com')
{'removed': '0', 'new_count': '16', 'added': '16', 'kept': '0'}
```

#### Bake Agents
```
>>> api.bake_agents()
```

#### Activate Changes
```
>>> api.activate_changes()
```
