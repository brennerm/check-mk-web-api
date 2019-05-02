import vcr
from functools import wraps
import re


# caputures the server url and replaces IP or name with localhost-testing to help with cassette errors
def scrub_string(string, replacement=""):
    def before_record_response(response):
        regexp_http = '^https?://[^/]+/'
        regexp_username = "_username=[a-zA-Z]+"
        regexp_secret = "_secret=.*$"

        replaced_uri = re.sub(regexp_http, 'http://localhost/', response.uri)
        replaced_uri = re.sub(regexp_username, "_username=automation", replaced_uri)
        replaced_uri = re.sub(regexp_secret, "_secret=not_a_secret", replaced_uri)
        response.uri = replaced_uri

        return response

    return before_record_response


my_vcr = vcr.VCR(
    # decode_compressed_response=True,
    before_record=scrub_string("_secret", "username")
)


# with my_vcr.use_cassette('test.yml'):
# your http code here


def filter_uri(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print("Calling decorated function")
        # s = str(inspect.stack()[1][3]).split()[0][2:]

        path_name = f.__qualname__
        # print(s)
        print(path_name)
        with my_vcr.use_cassette('cassettes/' + path_name + '.yaml'):
            return f(*args, **kwds)
    return wrapper


