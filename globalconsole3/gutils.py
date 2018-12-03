import os
import uuid
import re
from colorama import Fore, Style

class GcUtils:

    @staticmethod
    def gcpath():
        return os.path.dirname(os.getcwd())

    @staticmethod
    def gcfile(file):
        return os.path.basename(file)

    @staticmethod
    def uuid_generator(instring):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, instring))

    @staticmethod
    def trim_ansi(a):
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
        if ver == config['JSON']['pick_yes']:
            color = eval("Fore." + config['JSON']['pick_yes_color'])
            return color + item + Style.RESET_ALL
        else:
            color = eval("Fore." + config['JSON']['pick_no_color'])
            return color + item + Style.RESET_ALL

    # todo un-hardcode
    @staticmethod
    def color_uuid(item):
        return Style.RESET_ALL + Style.DIM + Fore.BLACK + item + Style.RESET_ALL