class NoNoneValueDict(dict):
    """Dictionary that does not allow items with None as value"""
    def __init__(self, dictionary=None):
        super(NoNoneValueDict, self).__init__()
        if dictionary:
            for k, v in dictionary.items():
                self.__setitem__(k, v)

    def __setitem__(self, key, value):
        if value is not None:
            super(NoNoneValueDict, self).__setitem__(key, value)
