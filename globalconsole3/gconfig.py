import configparser
import glob
#
from globalconsole3.gutils import GcUtils as gutils

class GcConfig:

    CONFIG_MASK = "config/*.ini"
    CONFIG_MAIN = "config.ini"
    CONFIG_MAIN_SECTIONS = ['LOGGING', 'JSON', 'COMMAND', 'BATCH', 'CMD']

    def __init__(self):

        self.config = configparser.ConfigParser()

        try:
            loaded = self.config.read(glob.glob("{}/{}".format(gutils.gcpath(), self.CONFIG_MASK)))

            if self.CONFIG_MAIN not in [gutils.gcfile(file) for file in loaded]:
                raise Exception("main config file: {} cannot be found. exiting..".format(self.CONFIG_MAIN))

            if not all(elem in self.config.sections() for elem in self.CONFIG_MAIN_SECTIONS):
                raise Exception("main config file: {} seems to be invalid. exiting..".format(self.CONFIG_MAIN))

        except Exception as e:
            print(e)
            exit(1)


