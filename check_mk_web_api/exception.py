class CheckMkWebApiException(Exception):
    """
    Exception for result_code != 0 in Check_Mk Web API response
    :param reason: String that contains "result"

    Check_Mk Web API returns the following json string
    {"result_code": 1, "result": "No such user"}
    """
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class CheckMkWebApiResponseException(Exception):
    """
    This exception is being thrown when the Check_Mk Web API responds with a HTTP status code != 200
    :param response: http.client.HTTPResponse object that we received from Check_Mk Web API
    """
    def __init__(self, response):
        self.response = response
