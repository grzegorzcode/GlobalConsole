import configparser
import glob
#
import globalconsole3.gexception as gexception
from globalconsole3.gutils import GcUtils as gutils

class GcConfig:

    CONFIG_MASK = "config/*.ini"

    def __init__(self):

        for file in glob.glob("{}/{}".format(gutils.gcpath(), self.CONFIG_MASK)):
            print(file)

        # if not os.path.isfile():
        #     print("configuration file config.ini not found in directory config. process terminated..")
        #     exit(1)
        #
        # self.config = configparser.ConfigParser()
        # self.config.read("{}/config/config.ini")
        #
        # if "".join(self.config.sections()) != "LOGGINGJSONCOMMANDBATCHCMD":
        #     print("configuration file config.ini invalid. process terminated..")
        #     exit(2)

