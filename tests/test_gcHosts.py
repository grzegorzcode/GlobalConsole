from unittest import TestCase
import unittest.mock
import globalconsole.GcHosts as ghosts
import os
import inspect
from tinydb import Query
import io

gho = ghosts()


class TestGcHosts(TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, n, m, func, expected, msg, mock):
        if m > 0:
            func(n, m)
        else:
            func(n)
        self.assertEqual(len(mock.getvalue().splitlines()), expected, msg)

    def test_importCsvAsHosts(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assertEqual(len(gho.hosttable.all()), 5)

    def test_updateHost(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        gho.updateHost({'port': '33333', 'group': 'some'}, 'myhost5')
        self.assertEqual(gho.hosttable.count(Query().port == '33333'), 1)

    def test_removeHost(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        gho.removeHost('myhost3')
        self.assertEqual(len(gho.hosttable.all()), 4)

    def test_purgeHosts(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        gho.purgeHosts()
        self.assertEqual(len(gho.hosttable.all()), 0)

    def test_searchHostName(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assertEqual(len(gho.searchHostName('myhost5')), 1)

    def test_searchGroupName(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assertEqual(len(gho.searchGroupName('default')), 3)

    def test_searchByUuid(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assertEqual(len(gho.searchByUuid('ea886322-421e-5254-92da-07c6ac921a87')[0]), 1)
        self.assertEqual(gho.searchByUuid('ea886322-421e-5254-92da-07c6ac921a87')[1], 'host')

    def test__indexHosts(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assertEqual(len(gho.hosts_idx), 5)
        self.assertEqual(len(gho.hosts_idx[0]), 5)

    def test_pickHosts(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        self.assert_stdout(False, 0, gho.pickHosts, 12, "pickHosts method")

    def test_getHosts(self):
        gho.purgeHosts()
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        gho.getHosts(True, 'port', 'group')

    def test_exportHostsToCsv(self):
        gho.purgeHosts()
        if os.path.exists("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hostsExp.csv")):
            os.remove("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hostsExp.csv"))
        gho.importCsvAsHosts("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hosts.csv"))
        gho.exportHostsToCsv(outfile="{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hostsExp.csv"))
        boolExp=os.path.exists("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(ghosts)))), "hosts/hostsExp.csv"))

        self.assertEqual(boolExp, True)
