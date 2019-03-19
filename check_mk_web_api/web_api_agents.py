from check_mk_web_api.web_api_base import WebApiBase


class WebApiAgents(WebApiBase):

    def bake_agents(self):
        """
        Bakes all agents

        Enterprise Edition only!
        """
        return self.make_request('bake_agents')
