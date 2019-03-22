from check_mk_web_api.web_api_hosts import WebApiHosts
from check_mk_web_api.web_api_folders import WebApiFolders


# in web_api.py
class WebApi(WebApiHosts, WebApiFolders):
    def checking(self):
        print('Yeppers')