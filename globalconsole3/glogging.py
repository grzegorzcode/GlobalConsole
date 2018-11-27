import logging
from logging.handlers import RotatingFileHandler
from tabulate import tabulate
from colorama import Fore, Style
#
import globalconsole3.gexception as gexception
from globalconsole3.gutils import GcUtils as gutils


class GcLogging:

    def __init__(self, config):
        self.gConfig = config.config
        try:
            self.logger = logging.getLogger(self.gConfig['LOGGING']['logger_name'])
            self.logger.setLevel(self.gConfig['LOGGING']['logging_level'])
            self.handler = RotatingFileHandler("{}/{}".format(gutils.gcpath(), self.gConfig['LOGGING']['log_file']),  maxBytes=int(self.gConfig['LOGGING']['log_file_size']), backupCount=int(self.gConfig['LOGGING']['log_file_rotate']))
            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)

        except Exception as e:
            gexception.UnhadledException(e, "cannot start logging mechanism")
            exit(1)

        self.logging_levels = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOSET": 10}
        self.logging_level = self.logging_levels[self.gConfig['LOGGING']['logging_level']]

    def _print(self, msg, methodlevel):
        if self.gConfig['LOGGING']['logging_to_cli'] == "YES":
            if methodlevel >= self.logging_level:
                print(msg)
        else:
            pass

    def show(self, msg):
        if self.gConfig['LOGGING']['logging_silent_cli'] == "NO":
            print(msg)
        else:
            pass

    def tab(self, vtab, vheaders):
        headers = list()
        color = eval("Fore." + self.gConfig['LOGGING']['logging_tab_head_color'])

        for k in vheaders:
            headers.append(color + k + Style.RESET_ALL)
        print(tabulate(vtab, headers=headers, tablefmt=self.gConfig['LOGGING']['logging_tab_fmt']))

    def info(self, msg):
        self._print(msg, self.logging_levels["INFO"])
        self.logger.info(msg)

    def error(self, msg):
        self._print(msg, self.logging_levels["ERROR"])
        self.logger.error(msg, exc_info=1, stack_info=1)

    def critical(self, msg):
        self._print(msg, self.logging_levels["CRITICAL"])
        self.logger.critical(msg, exc_info=1, stack_info=1)
        exit(1)

    def warning(self, msg):
        self._print(msg, self.logging_levels["WARNING"])
        self.logger.warning(msg)

    def debug(self, msg):
        self._print(msg, self.logging_levels["DEBUG"])
        self.logger.debug(msg)


