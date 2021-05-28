class ArgumentError(ValueError):
    ...


class PathOpError(ValueError):
    ...

class AssertFailed(AssertionError):
    code = "assertion.failed"
    msg_template = "Assertion failed, \n got : {got}\n want: {want}{extras}"
    def __init__(self, got, want, **kwargs):
        self.got = got
        self.want = want
        self.kwargs = kwargs
