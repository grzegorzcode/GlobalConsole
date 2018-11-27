import globalconsole3.gexception as gexception
import globalconsole3.gconfig as gconfig
import globalconsole3.glogging as glogging
if __name__ == '__main__':

    #config
    gconf = gconfig.GcConfig()

    #logging
    glog = glogging.GcLogging(gconf)


    try:
        a = 1/0
        #raise gexception.GcException(1000, "TEST LOG AND ERR TOGETHER")
    except gexception.GcException as e:
        glog.error(e)
    except Exception as e:
        glog.error(gexception.UnhadledException.msg(e, "just testing"))
