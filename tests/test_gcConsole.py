from unittest import TestCase
import unittest.mock
import io
import os
#
import sys
sys.path.append(os.getcwd())
#
import globalconsole.gconfig as gconfig
import globalconsole.glogging as glogging
import globalconsole.ghosts as ghosts
import globalconsole.gcreds as gcreds
import globalconsole.gvars as gvars
import globalconsole.gcommands as gcomm
import globalconsole.gconsole as gcon


class TestGcConsole(TestCase):

    #if True then print to stderr
    PTSTDERR = True

    def print_to_stderr(self, msg):
        if self.PTSTDERR is True:
            print(msg, file=sys.stderr)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, m, func, expectedlen, expectedcontains, expectednotcontains, msg, mock):
        func(m)
        self.print_to_stderr(mock.getvalue())

        #equal len
        if expectedlen:
            self.assertEqual(len(mock.getvalue().splitlines()), expectedlen, msg)
        #contains
        if expectedcontains:
            if expectedcontains in mock.getvalue():
                res = expectedcontains
            else:
                res = "not found"
            self.assertEqual(res, expectedcontains, msg)
        #not contains
        if expectednotcontains:
            if expectednotcontains not in mock.getvalue():
                res = expectednotcontains
            else:
                res = "found"
            self.assertEqual(res, expectednotcontains, msg)

    def setUp(self):
        os.environ["GC_KEY"] = "MySecretPass"
        self.gconf = gconfig.GcConfig()
        self.gconf.config['CMD']['print_header'] = "NO"
        self.glog = glogging.GcLogging(self.gconf)
        self.gcreds = gcreds.GcCreds(self.gconf, self.glog)
        self.gcreds.purgeCreds()
        self.gcreds.importCsvAsCreds('tests/credsTEST.csv')
        self.ghosts = ghosts.GcHosts(self.gconf, self.glog)
        self.ghosts.purgeHosts()
        self.ghosts.importCsvAsHosts('tests/hostsTEST.csv')
        self.gvars = gvars.GcVars(self.gconf, self.glog)
        self.gcom = gcomm.GcCommand(self.gconf, self.glog, self.gvars, self.gcreds, self.ghosts)
        self.gcon = gcon.GcConsole(self.gconf, self.glog, self.gcom)

    def tearDown(self):
        #self.gcon.onecmd("exit")
        self.gvars.varsfile.close()
        self.gcreds.credfile.close()
        self.ghosts.hostfile.close()
        #DEBUGGING PURPOSES
        # print("---------------LOG INFO---------------")
        # with open('logs/global_console.log', 'r') as file:
        #     for line in file.readlines():
        #         print(line)

    def test_do_conn(self):
        self.assert_stdout("conn connect -Y", self.gcon.onecmd, 2, "INFO", "ERROR", "connection test")

    def test_do_run(self):
        self.gcon.onecmd("conn connect -Y")
        self.assert_stdout("run os whoami", self.gcon.onecmd, 4, "travis", "root", "os command test")
        self.assert_stdout("run os whoami +SU", self.gcon.onecmd, 4, "root", "travis", "sudo os command test")
        self.assert_stdout("run os whoami | awk '{print $1}' +SU", self.gcon.onecmd, 4, "root", "travis", "sudo os command with apostrophe test")
        self.assert_stdout("run scan -Y", self.gcon.onecmd, 11, "TESTDB", "ERROR", "scanning functionality test")
        self.assert_stdout("run db2 db2select +OS +USR instance", self.gcon.onecmd, 8, "IBMREQD", "ERROR", "db2 command test")
        self.assert_stdout("run scp -m put -s /home/travis/.ssh/id_rsa -d /home/travis/rsa -b", self.gcon.onecmd, 4, "id_rsa", "ERROR", "db2 scp test")
        try:
            with open('/home/travis/rsa', 'r') as file:
                file.readlines()
                val = 1
        except Exception:
            val = 0
        self.assertEqual(val, 1, "db2 scp result test")
        self.assert_stdout("run scp -m get -s /home/travis/.ssh/id_rsa -d /home/travis/ -b", self.gcon.onecmd, 4, "done:", "ERROR", "db2 scp test2")
        try:
            with open('/home/travis/id_rsa_myhost1', 'r') as file:
                file.readlines()
                val = 1
        except Exception:
            val = 0
        self.assertEqual(val, 1, "db2 scp result test2")

    #
    # def test_do_cred(self):
    #     self.fail()
    #
    # def test_do_host(self):
    #     self.fail()
    #
    # def test_do_shell(self):
    #     self.fail()
    #
    # def test_do_history(self):
    #     self.fail()
    #
    # def test_do_version(self):
    #     self.fail()
    #
    # def test_do_var(self):
    #     self.fail()
    #
    # def test_do_batch(self):
    #     self.fail()
    #
    # def test_do_check(self):
    #     self.fail()
    #
    # def test_do_config(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()

