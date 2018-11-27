class GcException(Exception):
    """Base class"""

    ERR_CODES = {
        # GENERAL ERRORS
        1000: "General Exception",
        # FILES ERRORS
        2000: "Main config file not found",
        2001: "Main config file is invalid"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = [a for a in args][0]
        self.msg = ""
        if len(args) > 1:
            self.msg = ", details: {}".format([a for a in args][1])

    def __str__(self):
        return repr("GC-{}: {}{}".format(self.code, self.ERR_CODES[self.code], self.msg))


class UnhadledException(object):

    @staticmethod
    def msg(e, msg=None):

        ERR_CODE = "GC-0001: unhandled exception"

        if msg:
            msg = " - {}".format(msg)
        else:
            msg = ""
        return repr("{}, details: {}{}".format(ERR_CODE, e, msg))
