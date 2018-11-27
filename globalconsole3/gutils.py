import os

class GcUtils:

    @staticmethod
    def gcpath():
        return os.path.dirname(os.getcwd())
