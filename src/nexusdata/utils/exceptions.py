class NexusQueryException(RuntimeError):

    def __init__(self, msg:str):
        self.msg = msg