from unittest import TestCase
import globalconsole.GcConsole as gconsole
import os
import inspect

gcon = gconsole.GcConsole()

#fixme complete testing

#python -m unittest tests/test_gcConsole_USE.py
class TestGcConsole(TestCase):
    def test_complete_cred(self):
        res = gcon.complete_cred("", "", "", "")
        self.assertEqual(len(res), 8)

    # def test_do_cred(self):
    #     self.fail()
    #
    # def test_complete_host(self):
    #     self.fail()
    #
    # def test_do_host(self):
    #     self.fail()
    #
    # def test_complete_conn(self):
    #     self.fail()
    #
    # def test_do_conn(self):
    #     self.fail()
    #
    # def test_complete_run(self):
    #     self.fail()
    #
    # def test_do_run(self):
    #     self.fail()
    #
    # def test_do_quit(self):
    #     self.fail()
    #
    # def test_do_exit(self):
    #     self.fail()
    #
    # def test_header(self):
    #     self.fail()
    #
    # def test_emptyline(self):
    #     self.fail()
    #
    # def test_postcmd(self):
    #     self.fail()
    #
    # def test_do_shell(self):
    #     self.fail()
    #
    # def test_complete_history(self):
    #     self.fail()
    #
    # def test_do_history(self):
    #     self.fail()
    #
    # def test_do_version(self):
    #     self.fail()
    #
    # def test_complete_var(self):
    #     self.fail()
    #
    # def test_do_var(self):
    #     self.fail()
    #
    # def test_do_batch(self):
    #     self.fail()
    #
    # def test_complete_check(self):
    #     self.fail()
    #
    # def test_do_check(self):
    #     self.fail()
