"""
.. module:: GcConfig
   :platform: Linux
   :synopsis: Configuration Manager for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""

import configparser
import os.path
import inspect


class GcConfig:
    """This class features:

    - load parameter file, exit if not found
    - check headers in config file, exit if not valid ones


    Object of this class will look up for a config file **config/config.ini**.
    Config file must have a proper structure, because of this fact headers needs to be validated.


    """

    def __init__(self):
        if not os.path.isfile("{}/config/config.ini".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(GcConfig)))))):
            print("configuration file config.ini not found in directory config. process terminated..")
            exit(1)

        self.config = configparser.ConfigParser()
        self.config.read("{}/config/config.ini".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(GcConfig))))))

        if "".join(self.config.sections()) != "LOGGINGJSONCOMMANDBATCHCMD":
            print("configuration file config.ini invalid. process terminated..")
            exit(2)


