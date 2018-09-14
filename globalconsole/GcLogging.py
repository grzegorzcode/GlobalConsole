"""
.. module:: GcLogging
   :platform: Linux
   :synopsis: Logging Manager for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
try:
    from globalconsole.GcConfig import GcConfig
except ImportError:
    from GcConfig import GcConfig
import logging
from logging.handlers import RotatingFileHandler
from tabulate import tabulate
from colorama import Fore, Style
import os
import inspect


class GcLogging:
    """This class features:

    - setup rotating logs, exit if cannot be done
    - decorate standard logging methods with print function if needed
    - decorate error, critical logging methods with traceback and stack info

    Args:
        suffix (str): - module name that will be added in a log file

    Object of this class uses *RotatingFileHandler*, parameters are stored in **config.ini** file.

    """

    def __init__(self, suffix):
        self.gConfig = GcConfig().config
        try:
            self.logger = logging.getLogger(self.gConfig['LOGGING']['logger_name'] + "." + suffix)
            self.logger.setLevel(self.gConfig['LOGGING']['logging_level'])
            self.handler = RotatingFileHandler("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(GcLogging)))), self.gConfig['LOGGING']['log_file']),  maxBytes=int(self.gConfig['LOGGING']['log_file_size']), backupCount=int(self.gConfig['LOGGING']['log_file_rotate']))
            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)

        except Exception:
            print("configuration of logging is invalid. process terminated..")
            exit(1)

        self.logging_levels = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOSET": 10}
        self.logging_level = self.logging_levels[self.gConfig['LOGGING']['logging_level']]

    def _print(self, msg, methodlevel):
        """
        Internal method to print messages to stdout accordingly to chosen logging_level - object variable that map logging level to numeric value.

        Args:
            msg (str): message to be print
            methodlevel (int): numeric value of specific level

        """
        if self.gConfig['LOGGING']['logging_to_cli'] == "YES":
            if methodlevel >= self.logging_level:
                print(msg)
        else:
            pass

    def show(self, msg):
        """
        This method prints message to stdout independently from chosen logging level.

        Args:
            msg (str): message to print

        """
        if self.gConfig['LOGGING']['logging_silent_cli'] == "NO":
            print(msg)
        else:
            pass

    def tab(self, vtab, vheaders):
        """
        This method prints messages in a form of decorated table.

        Args:
            vtab (list): list of records
            vheaders (list): list of headers

        **number of elements in vheaders must be equal to number of elements in a record**

        """
        headers = list()
        color = eval("Fore." + self.gConfig['LOGGING']['logging_tab_head_color'])

        for k in vheaders:
            headers.append(color + k + Style.RESET_ALL)
        print(tabulate(vtab, headers=headers, tablefmt=self.gConfig['LOGGING']['logging_tab_fmt']))

    def info(self, msg):
        """
        This method writes INFO message to both log file and stdout if level is greater or equal.

        Args:
            msg (str): message to print

        """
        self._print(msg, self.logging_levels["INFO"])
        self.logger.info(msg)

    def error(self, msg):
        """
        This method writes ERROR message to both log file and stdout if level is greater or equal.

        Args:
            msg (str): message to print

        **traceback and stack info will be added to log file**

        """
        self._print(msg, self.logging_levels["ERROR"])
        self.logger.error(msg, exc_info=1, stack_info=1)

    def critical(self, msg):
        """
        This method writes CRITICAL message to both log file and stdout if level is greater or equal.

        Args:
            msg (str): message to print

        **traceback and stack info will be added to log file, execution of program will be terminated, also**

        """
        self._print(msg, self.logging_levels["CRITICAL"])
        self.logger.critical(msg, exc_info=1, stack_info=1)
        exit(1)

    def warning(self, msg):
        """
        This method writes WARNING message to both log file and stdout if level is greater or equal.

        Args:
            msg (str): message to print

        """
        self._print(msg, self.logging_levels["WARNING"])
        self.logger.warning(msg)

    def debug(self, msg):
        """
        This method writes DEBUG message to both log file and stdout if level is greater or equal.

        Args:
            msg (str): message to print

        """
        self._print(msg, self.logging_levels["DEBUG"])
        self.logger.debug(msg)


