class AppBusinessException(RuntimeError):

    def __init__(self, msg:str, *args):
        super().__init__(*args)
        self.msg = msg