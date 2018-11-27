import globalconsole3.gexception as gexception
import globalconsole3.gconfig as gconfig

if __name__ == '__main__':

    #exceptions
    try:
        #a = 1/0
        raise gexception.GcException(1000)
    except gexception.GcException as e:
        print(e)
    except Exception as e:
        gexception.UnhadledException()

    #config
    gconf = gconfig.GcConfig()