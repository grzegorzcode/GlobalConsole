"""
.. module:: gutils
   :platform: Linux
   :synopsis: Utilities Module for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
import os
import uuid
import re
from colorama import Fore, Style

class GcUtils:
    """This class features:

    -provide helpful methods shared by other modules

    """
    @staticmethod
    def gcpath():
        """
        This method returns full path of current directory

        Returns:
        str: current directory path

        Examples:

            >>> gcpath()

        """
        return os.getcwd()
        #return os.path.dirname(os.getcwd())

    @staticmethod
    def gcfile(file):
        """
        This method extracts filename from path

        Args:
            file (str): full path of a file

        Returns:
        str: filename

        Examples:

            >>> gcfile('/var/some/file.txt')

        """
        return os.path.basename(file)

    @staticmethod
    def uuid_generator(instring):
        """
        This method generates type 5 uuid based on a given string

        Args:
            instring (str): string being a base to uuid generation.

        Returns:
        uuid: uuid generated based on string

        Examples:

            >>> uuid_generator("group1host1install2")

        """
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, instring))

    @staticmethod
    def trim_ansi(a):
        """
        This method trims string from ansi escape sequences

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

    @staticmethod
    def color_pick(config, item, ver):
        """
        This method colors given string to a value described in a config file

        Args:
            config (object): holds instance of GcConfig class
            item (str): string to color
            ver (str): color to 'pick_yes' or 'pick_no' parameter

        Returns:
        str: string with colors

        Examples:

            >>> color_pick(config, "sometext", config['JSON']['pick_yes'])

        """
        if ver == config['JSON']['pick_yes']:
            color = eval("Fore." + config['JSON']['pick_yes_color'])
            return color + item + Style.RESET_ALL
        else:
            color = eval("Fore." + config['JSON']['pick_no_color'])
            return color + item + Style.RESET_ALL

    # todo un-hardcode
    @staticmethod
    def color_uuid(item):
        """
        This method colors given string to a predefined value

        Args:
            item (str): string to color

        Returns:
        str: string with colors

        Examples:

            >>> color_uuid("sometext")

        """
        return Style.RESET_ALL + Style.DIM + Fore.BLACK + item + Style.RESET_ALL