from check_mk_web_api.web_api_agents import WebApiAgents
from check_mk_web_api.web_api_alerts import WebApiAlerts
from check_mk_web_api.web_api_contactgroups import WebApiContactGroups
from check_mk_web_api.web_api_downtimes import WebApiDowntimes
from check_mk_web_api.web_api_folders import WebApiFolders
from check_mk_web_api.web_api_hostgroup import WebApiHostGroup
from check_mk_web_api.web_api_hosts import WebApiHosts
from check_mk_web_api.web_api_hosttags import WebApiHosttags
from check_mk_web_api.web_api_problems import WebApiProblems
from check_mk_web_api.web_api_ruleset import WebApiRuleset
from check_mk_web_api.web_api_servicegroup import WebApiServiceGroup
from check_mk_web_api.web_api_site import WebApiSite
from check_mk_web_api.web_api_users import WebApiUsers


class WebApi(WebApiHosts, WebApiFolders, WebApiHosttags, WebApiUsers, WebApiSite, WebApiServiceGroup, WebApiRuleset, WebApiAgents, WebApiAlerts, WebApiContactGroups, WebApiDowntimes, WebApiHostGroup, WebApiProblems):
    """
    # Arguments
    check_mk_url (str): URL to Check_Mk web application, multiple formats are supported
    username (str): Name of user to connect as. Make sure this is an automation user.
    secret (str): Secret for automation user. This is different from the password!

    # Examples
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk/webapi.py', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor', 'automation', 'secret')
    ```
    """
    pass
    # def __implement(self):
    #     return None
