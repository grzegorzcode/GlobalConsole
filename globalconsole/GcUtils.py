"""
.. module:: GcCommand
   :platform: Linux
   :synopsis: Utils for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
try:
    from globalconsole.GcConfig import GcConfig
except ImportError:
    from GcConfig import GcConfig
import uuid
import re
from colorama import Fore, Back, Style

class GcUtils:
    """This class features:

    -generates uuids
    -trim ansi escape sequences

    """
    def __init__(self):
        self.gConfig = GcConfig().config

    def uuid_generator(self, instring):
        """
        This method generates uuid based on a given string

        Args:
            instring (str): string being a base to uuid generation.

        Returns:
        uuid: uuid generated based on string

        Examples:

            >>> uuid_generator("group1host1install2")

        """
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, instring))


    def trim_ansi(self, a):
        """
        This method trim string from ansi escape sequences

        Args:
            a (str): string to trim

        Returns:
        str: string without escape sequences

        Examples:

            >>> trim_ansi(u"\u001b[1000D" + u"\u001b[34m" + "text" + u"\u001b[0m")

        """
        ESC = r'\x1b'
        CSI = ESC + r'\['
        OSC = ESC + r'\]'
        CMD = '[@-~]'
        ST = ESC + r'\\'
        BEL = r'\x07'
        pattern = '(' + CSI + '.*?' + CMD + '|' + OSC + '.*?' + '(' + ST + '|' + BEL + ')' + ')'
        return re.sub(pattern, '', a)

    def color_pick(self, item, ver):
        """
        This method colors given string to value described in a config file

        Args:
            item (str): string to color
            ver (str): color to 'pick_yes' or 'pick_no' parameter

        Returns:
        str: string with colors

        Examples:

            >>> trim_ansi(u"\u001b[1000D" + u"\u001b[34m" + "text" + u"\u001b[0m")

        """
        if ver == self.gConfig['JSON']['pick_yes']:
            color = eval("Fore." + self.gConfig['JSON']['pick_yes_color'])
            return color + item + Style.RESET_ALL
        else:
            color = eval("Fore." + self.gConfig['JSON']['pick_no_color'])
            return color + item + Style.RESET_ALL