from unittest import TestCase
import globalconsole.GcCreds as gcreds
import os
import inspect
from tinydb import Query

gcr = gcreds()

class TestGcCreds(TestCase):
    def test_importCsvAsCreds(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        self.assertEqual(len(gcr.credtable.all()), 3)

    def test_updateCred(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.updateCred({'encrypted': 'yes', 'password': 'some_pass'}, 'credname3')
        self.assertEqual(gcr.credtable.count(Query().password == 'some_pass'), 1)

    def test_removeCred(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.removeCred('credname3')
        self.assertEqual(len(gcr.credtable.all()), 2)

    def test_purgeCreds(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.purgeCreds()
        self.assertEqual(len(gcr.credtable.all()), 0)

    def test_getCreds(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.getCreds(False, False, 'encrypted', 'username')

    def test_exportCredsToCsv(self):
        gcr.purgeCreds()
        if os.path.exists("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/credsExp.csv")):
            os.remove("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/credsExp.csv"))
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.exportCredsToCsv(outfile="{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/credsExp.csv"))
        boolExp = os.path.exists("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/credsExp.csv"))
        self.assertEqual(boolExp, True)

    def test__upto16(self):
        self.assertEqual(gcr._upto16('mypass'), 'mypassmypassmypa')
        self.assertEqual(gcr._upto16('supersecuRePass!rd'), 'supersecuRePass!rdsupersecuRePas')

    def test_encryptPasswds(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.encryptPasswds(_utest=True)
        self.assertEqual(gcr.credtable.count(Query().password == 'password'), 0)
        self.assertEqual(gcr.credtable.count(Query().key_password == 'key_password'), 0)

    def test_decryptPasswds(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.encryptPasswds(_utest=True)
        val = gcr.decryptPasswds(gcr.credtable.all()[0], _utest=True)
        print(val)
        self.assertEqual(val[0], 'password')
        self.assertEqual(val[1], 'key_password')

    def test_decryptPasswdsInFile(self):
        gcr.purgeCreds()
        gcr.importCsvAsCreds("{}/{}".format(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getsourcefile(gcreds)))), "creds/creds.csv"))
        gcr.encryptPasswds(_utest=True)
        gcr.decryptPasswdsInFile(_utest=True)
        self.assertEqual(gcr.credtable.count(Query().password == 'password'), 1)
        self.assertEqual(gcr.credtable.count(Query().key_password == 'key_password'), 1)
