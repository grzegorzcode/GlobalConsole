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

    # commands
    gcom = gcomm.GcCommand(gconf, glog, gvars, gcreds, ghosts)



    #enabling panaceum
    #monkey patching of GcCommand
    if gconf.config['PANACEUM']['enabled'] == 'YES':
        try:
            from plugins import panaceum
            gcon.GcConsole.do_yaml = panaceum.do_testing
            # console
            gcon = gcon.GcConsole(gconf, glog, gcom)
            gcon.gLogging.info("Panaceum plugin enabled!")
            #adding to instance
            # from plugins import panaceum
            # import types
            # gcon.do_testing = types.MethodType(panaceum.do_testing, gcon)
        except Exception as e:
            # console
            gcon = gcon.GcConsole(gconf, glog, gcom)
            gcon.gLogging.warning("Panaceum plugin cannot be enabled..")

    #start app
    gcon.app()
