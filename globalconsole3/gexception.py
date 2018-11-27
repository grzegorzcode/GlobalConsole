class GcException(Exception):
    """Base class"""

    ERR_CODES = {
        # GENERAL ERRORS
        1000: "General Exception",
        # CONNECTIVITY ERRORS
        2000: "Invalid Credential"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = [a for a in args][0]

    def __str__(self):
        return repr("GC-{}: {}".format(self.code, self.ERR_CODES[self.code]))


class UnhadledException(object):

    ERR_CODE = "GC-0001: unhandled exception"

    def __init__(self):
        print(self.ERR_CODE)

