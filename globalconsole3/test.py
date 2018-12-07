import sys
import os

sys.path.append(os.getcwd())


import globalconsole3.gconfig as gconfig
import globalconsole3.glogging as glogging
import globalconsole3.ghosts as ghosts
import globalconsole3.gcreds as gcreds
import globalconsole3.gvars as gvars
import globalconsole3.gcommands as gcomm
import globalconsole3.gconsole as gcon

if __name__ == '__main__':

    #config
    gconf = gconfig.GcConfig()

    #logging
    glog = glogging.GcLogging(gconf)

    # try:
    #     a = 1/0
    # except Exception as e:
    #     glog.critical("Testing stuff")

    #hosts
    #ghosts = ghosts.GcHosts(gconf, glog, 'hosts/hosts.json')
    ghosts = ghosts.GcHosts(gconf, glog)

    # ghosts.purgeHosts()
    # ghosts.importCsvAsHosts('/home/myuser/Documents/GlobalConsole/GlobalConsole2/hosts/hostsVM.csv')
    # ghosts.updateHost({'host': '10.10.10.10'}, 'myhost1')
    # ghosts.removeHost('myhost1')
    # print(ghosts.searchHostName('myhost2'))
    # print("--")
    # print(ghosts.searchGroupName('VM'))
    # print("--")
    # print(ghosts.searchByUuid('e411ae67-8526-5d18-b05a-b5e57b486a6a'))
    # print("--")
    # print(ghosts.hosttable.all())
    # print('--pick--')
    # ghosts.pickHosts(manual=True, uuids=['5645848e-8cd4-5ff5-87fe-2a906d660aa0'])
    # print('--pick--')
    # ghosts.pickHosts(reset=True, resetOption='Y')
    # print("--")
    # ghosts.pickHosts(reset=True, resetOption='N')
    # print("--")
    # print(ghosts.hosttable.all())
    # print("--")
    # ghosts.getHosts(True, 'port', 'group')
    # ghosts.exportHostsToCsv('/home/myuser/Documents/GlobalConsole/GlobalConsole2/hosts/hosts3exp.csv')

    #creds
    gcreds = gcreds.GcCreds(gconf, glog)

    # gcreds.purgeCreds()
    # gcreds.importCsvAsCreds('/home/myuser/Documents/GlobalConsole/GlobalConsole2/creds/credsVM.csv')
    # gcreds.updateCred({'key_password': 'adawddwa'}, 'rootVM')
    # gcreds.removeCred('meVM')
    # print("--")
    # print(gcreds.searchCredName('rootVM'))
    # gcreds.encryptPasswds(_utest=True)
    # gcreds.decryptPasswdsInFile(_utest=True)
    # gcreds.getCreds(False, True, 'credname')
    # gcreds.exportCredsToCsv('/home/myuser/Documents/GlobalConsole/GlobalConsole2/creds/creds3exp.csv')

    #vars
    gvars = gvars.GcVars(gconf, glog)

    # gvars.purgeVars()
    # gvars.updateVar(varname="tar", value="t, g, z", persistent=True)
    # gvars.updateVar(varname="gzip", value="C, a, 2", persistent=True)
    # gvars.updateVar(varname="dir", value="myfil1.txt", persistent=False)
    # gvars.updateVar(varname="file", value="myfil1.txt", persistent=False)
    # gvars.getVars(False)
    # print(gvars.searchVarName('file'))
    # print(gvars.searchVarName('gzip'))
    # gvars.removeVar('tar')
    # gvars.removeVar('file')
    # gvars.getVars(False)
    # print(gvars.parseString("select * from {{gzip}}"))
    # print(gvars.parseString("select * from {{dir}}"))

    # commands
    gcom = gcomm.GcCommand(gconf, glog, gvars, gcreds, ghosts)
    # gcom.connect()
    # gcom.getConnections()
    # gcom.scan()
    # gcom.os("cat /etc/shadow | wc -l", sudo=False)
    # gcom.db2("select * from sysibm.sysdummy1", user="instance")
    # gcom.scp(mode="put", source="/home/myuser/Documents/GlobalConsole/GlobalConsole2/upload/myfile1.txt", dest="/tmp", recursive=False, suffix=True, batch=True)
    # gcom.os("ls -la  /tmp/myfile1.txt | awk '{print $1 }'", sudo=True)
    # gcom.os("ls -la  /tmp/myfile1.txt", sudo=False)
    # gcom.close()
    # gcom.exit()

    #console

    gcon = gcon.GcConsole(gconf, glog, gcom)
    gcon.onecmd("conn connect -Y")
    gcon.onecmd("run os uname -a")
    gcon.onecmd("exit")
    #gcon.app()
