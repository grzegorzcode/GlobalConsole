import sys
import os
sys.path.append(os.getcwd())
import globalconsole.gconfig as gconfig
import globalconsole.glogging as glogging
import globalconsole.ghosts as ghosts
import globalconsole.gcreds as gcreds
import globalconsole.gvars as gvars
import globalconsole.gcommands as gcomm
import globalconsole.gconsole as gcon
from signal import signal, SIGINT, SIG_IGN

if __name__ == '__main__':
    #disable CTRL+C exiting program
    signal(SIGINT, SIG_IGN)

    #config
    gconf = gconfig.GcConfig()

    #logging
    glog = glogging.GcLogging(gconf)

    #hosts
    ghosts = ghosts.GcHosts(gconf, glog)

    #creds
    gcreds = gcreds.GcCreds(gconf, glog)

    #vars
    gvars = gvars.GcVars(gconf, glog)

    #enabling panaceum
    #monkey patching of GcCommand
    if gconf.config['PANACEUM']['enabled'] == 'YES':
        try:
            from plugins import panaceum
            gcomm.GcCommand.yamlExecutor = panaceum.yamlExecutor
            gcon.GcConsole.do_yaml = panaceum.do_yaml
            gcon.GcConsole.complete_yaml = panaceum.complete_yaml
            # commands
            gcom = gcomm.GcCommand(gconf, glog, gvars, gcreds, ghosts)
            # console
            gcon = gcon.GcConsole(gconf, glog, gcom)
            gcon.gLogging.info("Panaceum plugin version %s enabled!" % gconf.config['PANACEUM']['pversion'])
            #adding to instance
            # from plugins import panaceum
            # import types
            # gcon.do_testing = types.MethodType(panaceum.do_testing, gcon)
        except Exception as e:
            # commands
            gcom = gcomm.GcCommand(gconf, glog, gvars, gcreds, ghosts)
            # console
            gcon = gcon.GcConsole(gconf, glog, gcom)
            gcon.gLogging.warning("Panaceum plugin version %s cannot be enabled.." % gconf.config['PANACEUM']['pversion'])

    #start app
    gcon.app()
