"""
.. module:: gvars
   :platform: Linux
   :synopsis: Variables Module for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
from tinydb import TinyDB, Query
import re
import itertools
from operator import itemgetter
#
from globalconsole.gutils import GcUtils as gutils


class GcVars:
    """This class features:

    -handle GC specific variables


    """
    def __init__(self, config, logger):
        """
        Construct object

        Args:
            config (object): holds instance of GcConfig class
            logger (object): holds instance of GcLogging class


        """
        # enable logging and config
        self.gLogging = logger
        self.gConfig = config.config
        #
        try:
            varsfile = "{}/{}".format(gutils.gcpath(), self.gConfig['JSON']['varfile'])
            self.varsfile = TinyDB(varsfile)
            self.varstable = self.varsfile.table("VARS")
            self.allvars = self.varstable.all()
        except Exception:
            self.gLogging.critical("variables definitions cannot be loaded")

    def refreshVars(self):
        """
        This method refreshes list of variables

        Examples:

            >>> refreshVars()

        """
        persistent = self.varstable.all()
        sess = [x for x in self.allvars if x not in persistent and x['persistent'] == 'n']
        #sess = [x for x in self.allvars if x['persistent'] == 'n']
        result = []
        sess.extend(persistent)
        for mydict in sess:
            if mydict not in result:
                result.append(mydict)
        self.allvars = result

    def updateVar(self, varname, value, persistent=True):
        """
        This method updates selected variable

        Args:
            varname (str): variable name
            value (str): value of variable
            persistent (bool): is variable persistent

        Examples:

            >>> updateVar(varname="file", value="myfile1.txt,myfile2.txt", persistent=False)

        """
        self.gLogging.debug("updateVar invoked")
        MyVar = Query()
        try:
            if varname not in [x['varname'] for x in self.allvars]:
                #add
                if persistent:
                    self.varstable.upsert({"varname": varname, "value": value.split(','), "persistent": "y"}, MyVar.varname == varname)
                    self.gLogging.info("added persistent variable: %s " % varname)
                else:
                    self.allvars.append({"varname": varname, "value": value.split(','), "persistent": "n"})
                    self.gLogging.info("added session variable: %s " % varname)
            else:
                #edit
                details = self.searchVarName(varname)
                if details['persistent'] == 'y':
                    self.varstable.upsert({"varname": varname, "value": value.split(','), "persistent": "y"}, MyVar.varname == varname)
                    self.gLogging.info("edited persistent variable: %s " % varname)
                else:
                    self.allvars = [x for x in self.allvars if x['varname'] != varname]
                    self.allvars.append({"varname": varname, "value": value.split(','), "persistent": "n"})
                    self.gLogging.info("edited session variable: %s " % varname)
            self.refreshVars()
        except Exception:
            self.gLogging.error("cannot update variable: " + varname)

    def removeVar(self, varname):
        """
        This method removes selected variable

        Args:
            varname (str): variable name

        Examples:

            >>> removeVar(varname="file")

        """
        self.gLogging.debug("removeVar invoked")
        MyVar = Query()
        try:
            details = self.searchVarName(varname)
            if details['persistent'] == 'y':
                self.varstable.remove(MyVar.varname == varname)
            else:
                self.allvars = [x for x in self.allvars if x["varname"] != varname]
        except Exception:
            self.gLogging.error("cannot remove varname: " + varname)

    def purgeVars(self):
        """
        This method removes all variables

        Examples:

            >>> purgeHosts()

        """
        self.gLogging.debug("purgeVars invoked")
        try:
            self.varstable.purge()
            self.allvars = []
        except Exception:
            self.gLogging.error("cannot purge variables ")

    def searchVarName(self, varname):
        """
        This method searches for a variable

        Args:
            varname (str): variable name to seach

        Returns:
            dict: variable definition as dict

        Examples:

            >>> searchVarName('var1')

        """
        self.gLogging.debug("searchVarName invoked")
        # MyVar = Query()
        try:
            return [x for x in self.allvars if x["varname"] == varname][0]
            # return self.varstable.search(MyVar.varname == varname)
        except Exception:
            return self.gLogging.error("cannot search with variable name: " + varname)

    def getVars(self, sort_reverse=False):
        """
        This method prints info about each variable in a tabular form.

        Args:
            sort_reverse (bool): reverse order of sorting

        Examples:

            >>> getVars(True)

        """
        self.gLogging.debug("getVars invoked")

        self.refreshVars()

        templist = list()
        #docs = self.varstable.all()
        docs = self.allvars
        result = sorted(docs, key=itemgetter("varname"), reverse=sort_reverse)
        try:
            for x in result:
                templist.append([x['varname'], ",".join(x['value']), x['persistent']])
            self.gLogging.tab(templist, ["name", "value", "keep"])
        except Exception:
            self.gLogging.error("cannot get variables definitions")

    def parseString(self, cmd):
        """
        This method parses given string to find variables, name of variable must be written within {{}}

        Args:
            cmd (str): string to parse

        Returns:
            list: list of strings being result of parsing

        Examples:

            >>> parseString("du -ms {{dirs}}")

        """

        self.gLogging.debug("parseString invoked")

        try:
            self.refreshVars()

            vars_pattern = re.compile("\{\{\w{1,}\}\}")
            variables = vars_pattern.findall(cmd)
            variables = [x.replace("{", "").replace("}", "") for x in variables]
            variables = sorted(variables)

            def to_list(instr):
                if isinstance(instr, str):
                    return [instr]
                else:
                    return instr

            args = [to_list(self.searchVarName(x)['value']) for x in variables]
            argsnumber = len(args)

            # print("__args")
            # print(args)

            commands = []
            for combination in itertools.product(*args):
                cmdTmp = cmd
                for i in range(0, argsnumber):
                    cmdTmp = cmdTmp.replace('{{' + variables[i] + '}}', str(combination[i]))
                commands.append(cmdTmp)

            return commands
        except Exception:
            self.gLogging.error("cannot parse command with variables")


