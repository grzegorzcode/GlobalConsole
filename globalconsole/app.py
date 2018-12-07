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

if __name__ == '__main__':

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

    #console
    gcon = gcon.GcConsole(gconf, glog, gcom)

    #start app
    gcon.app()
