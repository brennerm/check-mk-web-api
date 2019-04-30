import vcr
from functools import wraps

my_vcr = vcr.VCR(record_mode='none')


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
