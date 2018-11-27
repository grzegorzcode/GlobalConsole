import os

class GcUtils:

    @staticmethod
    def gcpath():
        return os.path.dirname(os.getcwd())

    @staticmethod
    def gcfile(file):
        return os.path.basename(file)
