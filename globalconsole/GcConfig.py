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

    # def set(self, section, option, value=None):
    #     """
    #     This method sets config option to given value
    #
    #     Args:
    #         section (str): section from config file
    #         option (str): option from config file
    #         value (str): value to set
    #
    #     Examples:
    #
    #         >>> set('COMMAND', 'csv_delimiter', '!')
    #
    #     """
    #     try:
    #         self.config.set(section=section, option=option, value=value)
    #     except Exception:
    #         print("invalid parameters, cannot be set")

    def get(self, section=None, option=None):
        """
        This method gets config option

        Args:
            section (str): section from config file
            option (str): option from config file

        Examples:

            >>> get('COMMAND', 'csv_delimiter')

        """
        try:
            if section is None and option is None:
                for section in sorted(list(self.config.sections())):
                    for item in list(self.config.items(section=section)):
                        print("section: %s option: %s value: %s" % (section, item[0], item[1]))
            elif section is not None and option is None:
                for item in list(self.config.items(section=section)):
                    print("section: %s option: %s value: %s" % (section, item[0], item[1]))
            elif section is None and option is not None:
                for section in sorted(list(self.config.sections())):
                    for item in list(self.config.items(section=section)):
                        if item[0] == option:
                            print("section: %s option: %s value: %s" % (section, item[0], item[1]))
            else:
                for item in list(self.config.items(section=section)):
                    if item[0] == option:
                        print("section: %s option: %s value: %s" % (section, item[0], item[1]))
        except Exception:
            print("invalid parameters, cannot get config")


