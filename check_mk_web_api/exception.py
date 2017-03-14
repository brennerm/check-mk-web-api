class CheckMkWebApiException(Exception):
    """
    Exception for result_code != 0 in Check_Mk Web API response
    """


class CheckMkWebApiResponseException(Exception):
    """
    This exception is being thrown when the Check_Mk Web API responds with a HTTP status code != 200
    :param response: http.client.HTTPResponse object that we received from Check_Mk Web API
    """
    def __init__(self, response):
        self.response = response


class CheckMkWebApiAuthenticationException(Exception):
    """
    This exception is being thrown when the Check_Mk Web API responds with an authentication error
    """
    pass
