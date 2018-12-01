import globalconsole3.gconfig as gconfig
import globalconsole3.glogging as glogging
import globalconsole3.ghosts as ghosts
if __name__ == '__main__':

    #config
    gconf = gconfig.GcConfig()

    #logging
    glog = glogging.GcLogging(gconf)

    try:
        a = 1/0
    except Exception as e:
        glog.critical("Testing stuff")

    #hosts
    #ghosts = ghosts.GcHosts(gconf, glog, 'hosts/hosts.json')
    #ghosts = ghosts.GcHosts(gconf, glog)