from unittest import TestCase
import unittest.mock
import globalconsole.GcLogging as glogging
import io


log = glogging('unittest')


class TestGcLogging(TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, n, m, func, expected, msg, mock):
        if m > 0:
            func(n, m)
        else:
            func(n)
        self.assertEqual(mock.getvalue(), expected, msg)

    def test__print(self):
        self.assert_stdout("print", 30, log._print, "print\n", "_print method")

    def test_show(self):
        self.assert_stdout("show", 0, log.show, "show\n", "show method")

    def test_tab(self):
        log.tab([['one', 1], ['two', 2]], ['col1', 'col2'])

    def test_info(self):
        self.assert_stdout("info", 0, log.info, "info\n", "info method")

    def test_error(self):
        self.assert_stdout("error", 0, log.info, "error\n", "error method")

    def test_critical(self):
        with self.assertRaises(SystemExit) as cm:
            log.critical("critical")
        self.assertEqual(cm.exception.code, 1)

    def test_warning(self):
        self.assert_stdout("warning", 30, log._print, "warning\n", "warning method")

    def test_debug(self):
        self.assert_stdout("debug", 30, log._print, "debug\n", "debug method")
