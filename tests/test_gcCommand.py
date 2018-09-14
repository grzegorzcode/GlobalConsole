from unittest import TestCase
import globalconsole.GcCommand as gcommand
import os
import inspect

gcom = gcommand()


class TestGcCommand(TestCase):

    def test_getConnections(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        var = len(gcom.connections)
        gcom.close()
        self.assertEqual(var, 2)

    def test_connect(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        var = len(gcom.connections)
        gcom.close()
        self.assertEqual(var, 2)

    def test_scan(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        gcom.scan(dry=False)
        var = len(gcom.gHosts.hosttable.all()[0]['installations'])
        gcom.close()
        self.assertEqual(int(var), 1)


    def test_close(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        gcom.close()
        var = len(gcom.connections)
        self.assertEqual(var, 0)

    def test_quit(self):
        with self.assertRaises(SystemExit) as cm:
            gcom.quit()
        self.assertEqual(cm.exception.code, 0)

    def test_exit(self):
        with self.assertRaises(SystemExit) as cm:
            gcom.exit()
        self.assertEqual(cm.exception.code, 0)

    def test_os(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        gcom.os("df -h | wc -l", sudo=False)
        gcom.close()
        var = gcom.result[1][0].decode("utf-8")
        self.assertEqual(int(var), 10)

    def test_db2(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        gcom.scan(dry=False)
        gcom.db2("select * from sysibm.sysdummy1", user="instance")
        var = len(gcom.result)
        self.assertEqual(var, 6)

        gcom.db2("pwd", osmode=True)
        var = len(gcom.result)
        self.assertEqual(var, 6)

        gcom.db2("db2pd -db {} -wlocks", user="instance", osmode=True)
        var = len(gcom.result)
        self.assertEqual(var, 6)

        gcom.db2("get dbm cfg | grep buffer", user="instance", osmode=False, level='IN')
        var = len(gcom.result)
        self.assertEqual(var, 4)

        gcom.close()

    def test_scp(self):
        gcom.gCreds.purgeCreds()
        gcom.gCreds.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "creds/credsVM.csv"))
        gcom.gHosts.purgeHosts()
        gcom.gHosts.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcommand)))), "hosts/hostsVM.csv"))
        gcom.connect()
        gcom.os("rm -f /tmp/myfile1_12123.txt", sudo=True)
        gcom.scp(mode="put", source="/home/pl55227/Documents/GlobalConsole/GlobalConsole2/upload/myfile1_12123.txt", dest="/tmp", recursive=False, suffix=True, batch=True)
        gcom.os("ls /tmp/myfile1_12123.txt | wc -l", sudo=True)
        gcom.close()
        var = gcom.result[0][0].decode("utf-8")
        self.assertEqual(int(var), 1)
