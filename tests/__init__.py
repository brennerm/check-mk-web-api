import vcr
from functools import wraps
import re

# caputures the server url and replaces IP or name with localhost-testing to help with cassette errors
def scrub_string(string, replacement=''):
    def before_record_response(response):
        regexp = '^https?://[^/]+/'
        replaced_uri = re.sub(regexp, 'http://localhost-testing/', response.uri)
        response.uri = replaced_uri

        return response
    return before_record_response


my_vcr = vcr.VCR(
    # decode_compressed_response=True,
    before_record=scrub_string('_secret', 'username'),

)


# with my_vcr.use_cassette('test.yml'):
# your http code here

def my_workingvcr(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        # s = str(inspect.stack()[1][3]).split()[0][2:]

        path_name = f.__qualname__
        # print(s)
        print(path_name)
        with my_vcr.use_cassette('cassettes/' + path_name + '.yml',
                                 filter_query_parameters=['_secret', '_username']):

            return f(*args, **kwds)

    return wrapper
