"""
.. module:: gconsole
   :platform: Linux
   :synopsis: Cmd Module for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
import cmd
from colorama import Fore, Style
import os
import argparse
import readline
import atexit
import sys
from urllib.request import urlopen
#
from globalconsole.gutils import GcUtils as gutils


class GcConsole(cmd.Cmd):
    """This class features:

    - use cmd module to interact with the app

    Arguments of methods are being parsed by ``argparse``

    """
    prompt = "gc> "

    def __init__(self, config, logger, command):
        """
        Construct object

        Args:
            config (object): holds instance of GcConfig class
            logger (object): holds instance of GcLogging class
            command (object): holds instance of GcCommands class


        """
        cmd.Cmd.doc_header = "GlobalConsole: type <help> to see this message"
        cmd.Cmd.undoc_header = "Commands: type <command> -h to get help (+h for db2 command)"
        cmd.Cmd.__init__(self)

        #initialize required objects
        self.gLogging = logger
        self.gConfig = config.config
        self.gCommand = command
        self.gLogging.info("Session started.")

        #set cmd module environment
        self.epilog = ""
        try:
            if self.gConfig['CMD']['print_header'] == "YES":
                self.header()
        except Exception:
            self.gLogging.warning("not supported terminal, you may experience a strange behaviour")

        #check env variable

        try:
            len(os.environ[self.gConfig['JSON']['decrypt_key_os_var']])
        except Exception:
            self.gLogging.warning("ENV VARIABLE: {} is not set! this may cause problems if password encryption is or will be enabled! Exit program and run: export GC_KEY=<YourPassword>".format(self.gConfig['JSON']['decrypt_key_os_var']))

        #initialize history file
        try:
            if os.path.exists("{}/{}".format(gutils.gcpath(), self.gConfig['CMD']['histfile'])) is False:
                with open("{}/{}".format(gutils.gcpath(), self.gConfig['CMD']['histfile']), "w") as f:
                    f.write("")

            readline.read_history_file("{}/{}".format(gutils.gcpath(), self.gConfig['CMD']['histfile']))
            # default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(int(self.gConfig['CMD']['histlen']))
        except Exception:
            self.gLogging.error("cannot load history file")

    ###GcCreds
    def complete_cred(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['import', 'update', 'rem', 'purge', 'show', 'export', 'encrypt', 'decrypt']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_cred(self, args):
        """
        This method handles all tasks related to credentials

        """
        self.gLogging.debug("do_cred invoked")
        description = "work with credentials"
        try:
            parser = argparse.ArgumentParser(prog="cred", add_help=True, epilog=self.epilog, description=description, usage="cred <command> [<args>]")
            subparsers = parser.add_subparsers()

            import_parser = subparsers.add_parser('import', description="import csv file as credentials", usage="cred import <args>")
            import_parser.set_defaults(which='import')
            import_parser.add_argument('-f', '--filename', type=str, required=True, help="filename")

            update_parser = subparsers.add_parser('update', description="update credential", usage="cred update <args>")
            update_parser.set_defaults(which='update')
            update_parser.add_argument('-p', '--parameter', type=str, required=True, help="parameter to change")
            update_parser.add_argument('-v', '--value', type=str, required=True, help="value to assign")
            update_parser.add_argument('-c', '--credname', type=str, required=True, help="credname")

            rem_parser = subparsers.add_parser('rem', description="remove credential", usage="cred rem <args>")
            rem_parser.set_defaults(which='rem')
            rem_parser.add_argument('-c', '--credname', type=str, required=True, help="credname")

            purge_parser = subparsers.add_parser('purge', description="purge credentials", usage="cred purge <args>")
            purge_parser.set_defaults(which='purge')
            purge_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            show_parser = subparsers.add_parser('show', description="show credentials", usage="cred show <args>")
            show_parser.set_defaults(which='show')
            show_parser.add_argument('-r', '--reverse', action='store_true', help="reverse sort order")
            show_parser.add_argument('-e', '--enc', action='store_true', help="show password as plain text")
            show_parser.add_argument('-f', '--fields', type=str, nargs="*", help="fields to sort on")

            export_parser = subparsers.add_parser('export', description="export credentials to csv file", usage="cred export <args>")
            export_parser.set_defaults(which='export')
            export_parser.add_argument('-f', '--filename', type=str, required=True, help="filename")

            encrypt_parser = subparsers.add_parser('encrypt', description="encrypt stored passwords", usage="cred encrypt <args>")
            encrypt_parser.set_defaults(which='encrypt')
            encrypt_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            decrypt_parser = subparsers.add_parser('decrypt', description="decrypt stored passwords", usage="cred decrypt <args>")
            decrypt_parser.set_defaults(which='decrypt')
            decrypt_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'import':
                self.gCommand.gCreds.importCsvAsCreds(filename=choice['filename'])
            elif choice['which'] == 'update':
                self.gCommand.gCreds.updateCred(definition={choice['parameter']: choice['value']}, credname=choice['credname'])
            elif choice['which'] == 'rem':
                self.gCommand.gCreds.removeCred(credname=choice['credname'])
            elif choice['which'] == 'purge':
                if choice['yes']:
                    self.gCommand.gCreds.purgeCreds()
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'show':
                if choice['fields'] is None:
                    choice['fields'] = ['username']
                self.gCommand.gCreds.getCreds(choice['enc'], choice['reverse'], *choice['fields'])
            elif choice['which'] == 'export':
                self.gCommand.gCreds.exportCredsToCsv(outfile=choice['filename'])
            elif choice['which'] == 'encrypt':
                if choice['yes']:
                    self.gCommand.gCreds.encryptPasswds()
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'decrypt':
                if choice['yes']:
                    self.gCommand.gCreds.decryptPasswdsInFile()
                else:
                    self.gLogging.show("skipped.. ")
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")



    ###GcHosts
    def complete_host(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['import', 'update', 'rem', 'purge', 'pick', 'show', 'export']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_host(self, args):
        """
        This method handles all tasks related to hosts

        """
        self.gLogging.debug("do_host invoked")
        description = "work with hosts"
        try:
            parser = argparse.ArgumentParser(prog="host", add_help=True, epilog=self.epilog, description=description, usage="host <command> [<args>]")
            subparsers = parser.add_subparsers()

            import_parser = subparsers.add_parser('import', description="import csv file as hosts", usage="host import <args>")
            import_parser.set_defaults(which='import')
            import_parser.add_argument('-f', '--filename', type=str, required=True, help="filename")

            update_parser = subparsers.add_parser('update', description="update host", usage="host update <args>")
            update_parser.set_defaults(which='update')
            update_parser.add_argument('-p', '--parameter', type=str, required=True, help="parameter to change")
            update_parser.add_argument('-v', '--value', type=str, required=True, help="value to assign")
            update_parser.add_argument('-s', '--server', type=str, required=True, help="server")

            rem_parser = subparsers.add_parser('rem', description="remove host", usage="host rem <args>")
            rem_parser.set_defaults(which='rem')
            rem_parser.add_argument('-s', '--server', type=str, required=True, help="server")

            purge_parser = subparsers.add_parser('purge', description="purge hosts", usage="host purge <args>")
            purge_parser.set_defaults(which='purge')
            purge_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            pick_parser = subparsers.add_parser('pick', description="pick hosts", usage="host pick <args>")
            pick_parser.set_defaults(which='pick')
            pick_parser.add_argument('-m', '--manual', nargs='*', help="manually select uuids to change")
            pick_parser.add_argument('-r', '--reset', action='store_true', help="reset all items selection")
            pick_parser.add_argument('-c', '--collapse', action='store_false', help="show only groups and hosts")
            pick_parser.add_argument('-o', '--option', type=str, required=False, help="reset option: Y(default) - all to picked, N - none picked")

            show_parser = subparsers.add_parser('show', description="show hosts", usage="host show <args>")
            show_parser.set_defaults(which='show')
            show_parser.add_argument('-r', '--reverse', action='store_true', help="reverse sort order")
            show_parser.add_argument('-f', '--fields', type=str, nargs="*", help="fields to sort on")

            export_parser = subparsers.add_parser('export', description="export hosts to csv file", usage="host export <args>")
            export_parser.set_defaults(which='export')
            export_parser.add_argument('-f', '--filename', type=str, required=True, help="filename")


            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'import':
                self.gCommand.gHosts.importCsvAsHosts(filename=choice['filename'])
            elif choice['which'] == 'update':
                self.gCommand.gHosts.updateHost(definition={choice['parameter']: choice['value']}, hostname=choice['server'])
            elif choice['which'] == 'rem':
                self.gCommand.gHosts.removeHost(hostname=choice['server'])
            elif choice['which'] == 'purge':
                if choice['yes']:
                    self.gCommand.gHosts.purgeHosts()
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'pick':
                if choice['manual']:
                    self.gCommand.gHosts.pickHosts(manual=True, uuids=choice['manual'], collapse=choice['collapse'])
                elif choice['reset']:
                    if choice['option'] is None:
                        choice['option'] = 'Y'
                    self.gCommand.gHosts.pickHosts(reset=choice['reset'], collapse=choice['collapse'], resetOption=choice['option'])
                else:
                    self.gCommand.gHosts.pickHosts(collapse=choice['collapse'])

            elif choice['which'] == 'show':
                if choice['fields'] is None:
                    choice['fields'] = ['hostname']
                self.gCommand.gHosts.getHosts(choice['reverse'], *choice['fields'])
            elif choice['which'] == 'export':
                self.gCommand.gHosts.exportHostsToCsv(outfile=choice['filename'])
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")


    ###GcCommand


    ##connections
    def complete_conn(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['connect', 'show', 'close']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_conn(self, args):
        """
        This method handles all tasks related to connections

        """
        self.gLogging.debug("do_conn invoked")
        description = "work with connections"
        try:
            parser = argparse.ArgumentParser(prog="conn", add_help=True, epilog=self.epilog, description=description, usage="conn <command> [<args>]")
            subparsers = parser.add_subparsers()

            connect_parser = subparsers.add_parser('connect', description="connect to hosts", usage="conn connect <args>")
            connect_parser.set_defaults(which='connect')
            connect_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")
            connect_parser.add_argument('hosts', type=str, nargs="*", help="list of hosts")

            close_parser = subparsers.add_parser('close', description="close connections", usage="conn close <args>")
            close_parser.set_defaults(which='close')
            close_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            show_parser = subparsers.add_parser('show', description="show connections", usage="conn show <args>")
            show_parser.set_defaults(which='show')

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'connect':
                if choice['yes']:
                    self.gCommand.connect(choice['hosts'])
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'close':
                if choice['yes']:
                    self.gCommand.close()
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'show':
                self.gCommand.getConnections()
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")


    ###commands
    def complete_run(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['os', 'scp', 'db2', 'scan']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_run(self, args):
        """
        This method handles all tasks related to commands execution

        """
        self.gLogging.debug("do_run invoked")
        description = "run commands"
        try:
            parser = argparse.ArgumentParser(prefix_chars='-', prog="run", add_help=True, epilog=self.epilog, description=description, usage="run <command> [<args>]")
            subparsers = parser.add_subparsers()

            os_parser = subparsers.add_parser('os', description="run os commands", usage="run os <args>", prefix_chars='+')
            os_parser.set_defaults(which='os')
            os_parser.add_argument('cmd', type=str, nargs="*", help="command to run")
            os_parser.add_argument('+SU', type=str, nargs="?", const="root", help="sudo to root or user")
            os_parser.add_argument('+SH', type=str, nargs="?", help="choose shell")
            os_parser.add_argument('+spool', type=str, nargs="?", help="spool output to file")
            os_parser.add_argument('+repeat', type=str, nargs=2, help="repeat command execution. <NR_OF_REPETITIONS DELAY_IN_SEC>")

            scp_parser = subparsers.add_parser('scp', description="run scp commands", usage="run scp <args>")
            scp_parser.set_defaults(which='scp')
            scp_parser.add_argument('-m', '--mode', type=str, required=True, help="[put | get]")
            scp_parser.add_argument('-s', '--src', type=str, required=True, help="source file, dir")
            scp_parser.add_argument('-d', '--dest', type=str, required=True, help="destination file, dir")
            scp_parser.add_argument('-r', '--recursive', action='store_true', help="copy recursively")
            scp_parser.add_argument('-b', '--batch', action='store_true', help="do not ask for confirmation")

            db2_parser = subparsers.add_parser('db2', description="run db2 commands", usage="run db2 <args>", prefix_chars='+')
            db2_parser.set_defaults(which='db2')
            db2_parser.add_argument('cmd', type=str, nargs="*", help="command to run")
            db2_parser.add_argument('+USR', type=str, nargs="?", help="run as user: [username | current | instance], current is default")
            db2_parser.add_argument('+ENV', type=str, nargs="*", help="set env variable")
            db2_parser.add_argument('+SH', type=str, nargs="?", help="choose shell")
            db2_parser.add_argument('+IN', action='store_true', help="placeholder: use instance instead of dbname")
            db2_parser.add_argument('+OS', action='store_true', help="run in osmode: os commands with loaded db2 profile")
            db2_parser.add_argument('+spool', type=str, nargs="?", help="spool output to file")
            db2_parser.add_argument('+repeat', type=str, nargs=2,  help="repeat command execution. <NR_OF_REPETITIONS DELAY_IN_SEC>")

            scan_parser = subparsers.add_parser('scan', description="run scan command", usage="run scan <args>")
            scan_parser.set_defaults(which='scan')
            scan_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")
            scan_parser.add_argument('-d', '--dry', action='store_true', help="dry run; do not store output")

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'os':
                if choice['spool'] is not None:
                    self.gCommand.set_spool(choice['spool'])

                useSudo = False
                sudoUser = ""
                if choice['SU'] is not None:
                    useSudo = True
                    sudoUser = choice['SU']

                if choice['SH'] is None:
                    choice['SH'] = ""

                if choice['repeat'] is None:
                    choice['repeat'] = [""]

                if len(choice['cmd']) == 0:
                    os_parser.print_help()
                else:
                    self.gCommand.os(cmd=" ".join(choice['cmd']), sudo=useSudo, sudoUser=sudoUser, shell=choice['SH'], repeat=" ".join(choice['repeat']))

            elif choice['which'] == 'scp':
                self.gCommand.scp(mode=choice['mode'], source=choice['src'], dest=choice['dest'], recursive=choice['recursive'], suffix=True, batch=choice['batch'])

            elif choice['which'] == 'db2':
                if choice['spool'] is not None:
                    self.gCommand.set_spool(choice['spool'])

                if choice['USR'] is None:
                    choice['USR'] = 'current'

                if choice['ENV'] is None:
                    choice['ENV'] = ''
                else:
                    choice['ENV'] = ' '.join(choice['ENV']) + '; '

                if choice['SH'] is None:
                    choice['SH'] = ""

                if choice['IN']:
                    vlevel = "IN"
                else:
                    vlevel = "DB"

                if choice['repeat'] is None:
                    choice['repeat'] = [""]

                if len(choice['cmd']) == 0:
                    db2_parser.print_help()
                else:
                    self.gCommand.db2(command=" ".join(choice['cmd']), user=choice['USR'], env=choice['ENV'], shell=choice['SH'], level=vlevel, osmode=choice['OS'], repeat=" ".join(choice['repeat']))

            elif choice['which'] == 'scan':
                if choice['yes']:
                    self.gCommand.scan(dry=choice['dry'])
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def do_exit(self, args):
        """
        This method saves command history and exit program

        """
        self.gLogging.debug("do_exit invoked")
        atexit.register(readline.write_history_file, "{}/{}".format(gutils.gcpath(), self.gConfig['CMD']['histfile']))
        self.gCommand.exit()

    ###Utilities
    def header(self):
        """
        This method gives a pretty header on start

        """
        rows, columns = os.popen('stty size', 'r').read().split()
        self.gLogging.show("".center(int(columns)))
        self.gLogging.show("".center(int(columns)))
        self.gLogging.show(Fore.RED + " #####   #        #######  ######      #     #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#     #  #        #     #  #     #    # #    #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#        #        #     #  #     #   #   #   #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#  ####  #        #     #  ######   #     #  #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#     #  #        #     #  #     #  #######  #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#     #  #        #     #  #     #  #     #  #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + " #####   #######  #######  ######   #     #  #######".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + " #####   #######  #     #   #####   #######  #        #######".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#     #  #     #  ##    #  #     #  #     #  #        #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#        #     #  # #   #  #        #     #  #        #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#        #     #  #  #  #   #####   #     #  #        #####  ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#        #     #  #   # #        #  #     #  #        #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + "#     #  #     #  #    ##  #     #  #     #  #        #      ".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.RED + " #####   #######  #     #   #####   #######  #######  #######".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show("                                          by Grzegorz Cylny".center(int(columns)))
        self.gLogging.show("".center(int(columns)))
        self.gLogging.show("".center(int(columns)))
        self.gLogging.show(Fore.LIGHTYELLOW_EX + "With Great Power Comes Great Responsibility".center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show(Fore.LIGHTWHITE_EX + self.gConfig['LOGGING']['gversion'].center(int(columns)) + Style.RESET_ALL)
        self.gLogging.show("".center(int(columns)))
        self.gLogging.show("".center(int(columns)))

        try:
            with urlopen("https://raw.githubusercontent.com/grzegorzcode/GlobalConsole/master/VERSION") as serv:
                sversion = str(serv.readline()).split(".")
                major = sversion[0].split("'")[1]
                minor = sversion[1]
                fix = sversion[2]
                sversion = int("{major}{minor}{fix}".format(major=major, minor=minor, fix=fix))
                sversionF = "{major}.{minor}.{fix}".format(major=major, minor=minor, fix=fix)

                lversion = self.gConfig['LOGGING']['gversion'].split(".")
                major = lversion[0]
                minor = lversion[1]
                fix = lversion[2]
                lversion = int("{major}{minor}{fix}".format(major=major, minor=minor, fix=fix))

                if sversion > lversion:
                    self.gLogging.show(Fore.LIGHTYELLOW_EX + "!! A NEW VERSION {new} available !!".format(new=sversionF).center(int(columns)) + Style.RESET_ALL)
        except Exception:
            self.gLogging.warning("cannot connect to github.com to check for a new version")

    def emptyline(self):
        """
        This method rewrites default behaviour of ``cmd`` module to re-run last command when enter pressed on empty prompt.

        """
        pass

    def postcmd(self, stop, line):
        """
        This method shows number of active connections after every command

        """
        if self.gConfig['CMD']['show_connections'] == 'YES':
            sys.stdout.write(u"\u001b[1000D" + u"\u001b[34m" + "active connections: " + str(len(self.gCommand.connections)) + " \n" + u"\u001b[0m")
            sys.stdout.flush()
        return stop

    def do_shell(self, args):
        """
        This method gives a possibility to run local os shell commands

        """
        self.gLogging.debug("do_shell invoked")
        description = "work with local shell"
        try:
            os.system(args)
        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def complete_history(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['show', 'clear', 'run', 'find']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_history(self, args):
        """
        This method handles all tasks related to management of history of commands

        """
        self.gLogging.debug("do_history invoked")
        description = "work with commands history"
        try:
            #import argcomplete
            parser = argparse.ArgumentParser(prog="history", add_help=True, epilog=self.epilog, description=description, usage="history <command> [<args>]")
            subparsers = parser.add_subparsers()

            clear_parser = subparsers.add_parser('clear', description="clear history", usage="history clear <args>")
            clear_parser.set_defaults(which='clear')
            clear_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            show_parser = subparsers.add_parser('show', description="show history", usage="history show") #, aliases=['s']
            show_parser.set_defaults(which='show')

            rem_parser = subparsers.add_parser('run', description="run command again", usage="history run <args>")
            rem_parser.set_defaults(which='run')
            rem_parser.add_argument('-c', '--command', type=int, required=True, help="command number")

            find_parser = subparsers.add_parser('find', description="find command", usage="history find <args>")
            find_parser.set_defaults(which='find')
            find_parser.add_argument('-c', '--command', type=str, required=True, help="command substring")

            #completer = argcomplete.CompletionFinder(parser)
            #readline.set_completer_delims("")
            #readline.set_completer(completer.rl_complete)
            #readline.parse_and_bind("tab: complete")

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'clear':
                if choice['yes']:
                    readline.clear_history()
                else:
                    self.gLogging.show("skipped.. ")
            elif choice['which'] == 'show':
                for i in range(readline.get_current_history_length()):
                    print(i+1, readline.get_history_item(i + 1))
            elif choice['which'] == 'run':
                self.onecmd(readline.get_history_item(choice['command']))
            elif choice['which'] == 'find':
                for i in range(readline.get_current_history_length()):
                    if choice['command'] in readline.get_history_item(i + 1):
                        print(i+1, readline.get_history_item(i + 1))
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def do_version(self, args):
        """
        This method prints GC version

        """
        try:
            self.gLogging.show(self.gConfig['LOGGING']['gversion'])
        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def complete_var(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['show', 'edit', 'rem', 'purge']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_var(self, args):
        """
        This method handles all tasks related to management of variables

        """
        self.gLogging.debug("do_var invoked")
        description = "work with variables"

        try:
            parser = argparse.ArgumentParser(prog="var", add_help=True, epilog=self.epilog, description=description, usage="var <command> [<args>]")
            subparsers = parser.add_subparsers()

            show_parser = subparsers.add_parser('show', description="show variables", usage="var show <args>")
            show_parser.set_defaults(which='show')
            show_parser.add_argument('-r', '--reverse', action='store_true', help="reverse sort order")

            edit_parser = subparsers.add_parser('edit', description="add or update variable", usage="var edit <args>")
            edit_parser.set_defaults(which='edit')
            edit_parser.add_argument('-V', '--varname', type=str, required=True, help="variable to add or update")
            edit_parser.add_argument('-v', '--value', type=str, required=True, help="variable to add or update")
            edit_parser.add_argument('-p', '--persistent', action='store_true', help="persistent variable if True")

            rem_parser = subparsers.add_parser('rem', description="remove variable", usage="var rem <args>")
            rem_parser.set_defaults(which='rem')
            rem_parser.add_argument('-V', '--varname', type=str, required=True, help="variable to remove")

            purge_parser = subparsers.add_parser('purge', description="purge variables", usage="var purge <args>")
            purge_parser.set_defaults(which='purge')
            purge_parser.add_argument('-Y', '--yes', action='store_true', required=True, help="confirm")

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'show':
                self.gCommand.gVars.getVars(sort_reverse=choice['reverse'])
            elif choice['which'] == 'edit':
                self.gCommand.gVars.updateVar(varname=choice['varname'], value=choice['value'], persistent=choice['persistent'])
            elif choice['which'] == 'rem':
                self.gCommand.gVars.removeVar(varname=choice['varname'])
            elif choice['which'] == 'purge':
                if choice['yes']:
                    self.gCommand.gVars.purgeVars()
                else:
                    self.gLogging.show("skipped.. ")
            else:
                parser.print_help()


        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def do_batch(self, args):
        """
        This method gives a possibility to run commands being stored in a file

        """
        self.gLogging.debug("do_batch invoked")
        description = "work with batch files"
        try:
            parser = argparse.ArgumentParser(prog="batch", add_help=True, epilog=self.epilog, description=description, usage="batch -f <filename>")
            parser.add_argument('-f', '--filename', type=str, required=True, help="batch file")
            errLine = ""
            errLineNr = 0
            choice = parser.parse_args(args.split())
            if choice.filename:
                with open(choice.filename, 'r') as infile:
                    self.gCommand.chain_proceed = 1
                    self.gCommand.check = ([], True)
                    for x, line in enumerate(infile.readlines()):
                        line = line.strip("\n")
                        if len(line) > 0:
                            if not line.startswith("#") and not line.startswith("exit") and not line.startswith("quit"):
                                errLine = line
                                errLineNr = x+1
                                self.gLogging.show("command: %s" % line)
                                self.onecmd(line)
                                if self.gCommand.chain_proceed == 0:
                                    raise AssertionError
                                self.gCommand.chain_proceed = 1
        except AssertionError:
            self.gLogging.info("--!--check failed on line:{}, command: {}".format(errLineNr, errLine))
            #self.gLogging.info("--!--check condition: {}, is present: {}".format(" ".join(self.gCommand.check[0]), self.gCommand.check[1]))
            self.gCommand.chain_proceed = 1
            self.gCommand.check = ([], True)
        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def complete_check(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        inlist = ['set', 'show']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_check(self, args):
        """
        This method handles all tasks related to management of variables being used  by ``batch`` method as a control points

        """
        self.gLogging.debug("do_check invoked")
        description = "check step in chain of commands"
        try:
            parser = argparse.ArgumentParser(prefix_chars='-', prog="check", add_help=True, epilog=self.epilog, description=description, usage="check <command> [<args>]")
            subparsers = parser.add_subparsers()

            set_parser = subparsers.add_parser('set', description="set text to check", usage="check set <args>")
            set_parser.set_defaults(which='set')
            set_parser.add_argument('cmd', type=str, nargs="*", help="text which output should contains")
            set_parser.add_argument('-r', '--reverse', action='store_false', help="do not contains; negation")

            show_parser = subparsers.add_parser('show', description="show text to check", usage="check show <args>")
            show_parser.set_defaults(which='show')

            choice = vars(parser.parse_args(args.split()))

            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'set':
                self.gCommand.check = (choice['cmd'], choice['reverse'])
            elif choice['which'] == 'show':
                self.gLogging.show("")
                self.gLogging.show("--------check-------- ")
                self.gLogging.show("text: ")
                self.gLogging.show(" ".join(self.gCommand.check[0]))
                self.gLogging.show("should be present: {}".format(self.gCommand.check[1]))
                self.gLogging.show("")

            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")


    def complete_config(self, text, line, start_index, end_index):
        """
        This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

        """
        #todo - finish setting
        inlist = ['show'] #, 'set']
        if text:
            return [item for item in inlist if item.startswith(text)]
        else:
            return inlist

    def do_config(self, args):
        """
        This method handles all tasks related to internal configuration

        """
        self.gLogging.debug("do_config invoked")
        description = "work with configuration"
        try:
            #import argcomplete
            parser = argparse.ArgumentParser(prog="config", add_help=True, epilog=self.epilog, description=description, usage="config <command> [<args>]")
            subparsers = parser.add_subparsers()

            show_parser = subparsers.add_parser('show', description="show config", usage="config show") #, aliases=['s']
            show_parser.set_defaults(which='show')
            show_parser.add_argument('-s', '--section', type=str, required=False, help="section of config")
            show_parser.add_argument('-o', '--option', type=str, required=False, help="option to show")

            # set_parser = subparsers.add_parser('set', description="set config option", usage="config set <args>")
            # set_parser.set_defaults(which='set')
            # set_parser.add_argument('-s', '--section', type=str, required=True, help="section of config")
            # set_parser.add_argument('-o', '--option', type=str, required=True, help="option to pick")
            # set_parser.add_argument('-v', '--value', type=str, required=True, help="value to set")

            choice = vars(parser.parse_args(args.split()))
            if len(args) == 0:
                parser.print_help()
            elif choice['which'] == 'show':
                GcConfig().get(section=choice['section'], option=choice['option'])
            # elif choice['which'] == 'set':
            #     config.set(section=choice['section'], option=choice['option'], value=choice['value'])
            else:
                parser.print_help()

        except SystemExit:
            pass
        except Exception:
            self.gLogging.error("cannot parse given arguments")

    def app(self):
        """
        This method start the app

        """
        self.cmdloop()


