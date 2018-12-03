from tinydb import TinyDB, Query
import re
import itertools
from operator import itemgetter
#
from globalconsole3.gutils import GcUtils as gutils


class GcVars:

    def __init__(self, config, logger):
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
        self.gLogging.debug("purgeVars invoked")
        try:
            self.varstable.purge()
            self.allvars = []
        except Exception:
            self.gLogging.error("cannot purge variables ")

    def searchVarName(self, varname):
        self.gLogging.debug("searchVarName invoked")
        # MyVar = Query()
        try:
            return [x for x in self.allvars if x["varname"] == varname][0]
            # return self.varstable.search(MyVar.varname == varname)
        except Exception:
            return self.gLogging.error("cannot search with variable name: " + varname)

    def getVars(self, sort_reverse=False):
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


