import argparse
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from urllib.request import urlopen


def complete_yaml(self, text, line, start_index, end_index):
    """
    This method uses ``inlist`` variable to enable ``cmd`` module command autocompletion

    """
    inlist = ['run']
    if text:
        return [item for item in inlist if item.startswith(text)]
    else:
        return inlist

def do_yaml(self, args):
    """
    This method handles all tasks related to management of yaml execution

    """
    self.gLogging.debug("do_yaml invoked")
    description = "work with yaml files"

    try:
        parser = argparse.ArgumentParser(prog="yaml", add_help=True, epilog=self.epilog, description=description, usage="yaml <command> [<args>]")
        subparsers = parser.add_subparsers()

        run_parser = subparsers.add_parser('run', description="run yaml file", usage="yaml run <args>")
        run_parser.set_defaults(which='run')
        run_parser.add_argument('-s', '--source', type=str, required=True, help="file to run, local or github")
        run_parser.add_argument('-S', '--stopping', action='store_false', required=False, help="disable stopping before next step execution")

        choice = vars(parser.parse_args(args.split()))
        if len(args) == 0:
            parser.print_help()
        elif choice['which'] == 'run':
            self.yamlExecutor(source=choice['source'], stopping=choice['stopping'])
        else:
            parser.print_help()
    except SystemExit:
        pass
    except Exception:
        self.gLogging.error("cannot parse given arguments")


def yamlExecutor(self, source, stopping=True):
    """
    This method executes yaml file step by step.

    If verification will fail for a current db, instance or host, it will be removed from a next step execution list.

    Args:
        source (str): file to execute, local or github (raw)
        stopping (bool): disable stopping before next step execution

    Examples:

        >>> yamlExecutor('/tmp/file.yaml', True)
    """


    try:
        with urlopen(source) as gitfile:
            gfile = serv.read().decode()
    except ValueError:
        pass

    try:
        gfile = open(source, 'r')
    except FileNotFoundError:
        self.gLogging.error("file: %s not found" % source)
    except Exception:
        self.gLogging.error("cannot load source file: %s" % source)

    try:
        yfile = yaml.load(gfile, Loader=Loader)
    except Exception:
        self.gLogging.error("cannot parse as valid yaml file: %s" % source)

    if stopping:
        self.gLogging.show("--- press Enter to load host file ---")
        input()

    try:
        hosts = [hosts['hosts'] for hosts in yfile if hosts.get('hosts', None) is not None][0]
        self.gCommand.gHosts.importCsvAsHosts(hosts)
        self.gLogging.info("hosts loaded from a yaml, location: %s" % hosts)
    except Exception:
        self.gLogging.info("hosts loaded from a GC")

    if stopping:
        self.gLogging.show("--- press Enter to load cred file ---")
        input()

    try:
        creds = [creds['creds'] for creds in yfile if creds.get('creds', None) is not None][0]
        self.gCommand.gCreds.importCsvAsCreds(creds)
        self.gLogging.info("creds loaded from a yaml, location: %s" % creds)
    except Exception:
        self.gLogging.info("creds loaded from a GC")

    def runcmd(cmd):
        self.onecmd(cmd)

    def removeUuid(uuid):
        detailedInfo = self.gCommand.gHosts.searchByUuid(uuid)
        self.gLogging.info("removing: %s with uuid %s from next step execution" % (detailedInfo[1], uuid))
        self.gCommand.gHosts.pickHosts(manual=True, uuids=[uuid], _printing=False)

    def runUuid(uuid, fixcmd):
        backuphosts = self.gCommand.gHosts.hosttable.all()
        backupconnections = self.gCommand.connections
        ##
        detailedInfo = self.gCommand.gHosts.searchByUuid(uuid)
        # print("-------detailed")
        # print(detailedInfo)
        self.gCommand.connections = [(host, client) for host, client in backupconnections if host == detailedInfo[0][0]['hostname']]

        self.gCommand.gHosts.pickHosts(reset=True, _printing=False, resetOption='N')
        self.gCommand.gHosts.hosttable.write_back(detailedInfo[0])
        if detailedInfo[1] == 'host':
            print("---------------------------changed")
        elif detailedInfo[1] == 'instance':
            pass
        elif detailedInfo[1] == 'db':
            pass
        else:
            pass
        print("----------------------------------FIXCMD")
        runcmd(fixcmd)
        # print("---------------------------back")
        self.gCommand.gHosts.hosttable.write_back(backuphosts)
        self.gCommand.connections = backupconnections
        # self.gCommand.gHosts.pickHosts(_printing=True)


    def analyze(condition, result, verify=False):
        msg = condition.get('msg', None)
        expect = condition.get('expect', False)
        failsolve = condition.get('failsolve', [None])
        output = result[0].decode()
        self.gLogging.info("phrases to check: %s" % ",".join(msg))
        self.gLogging.info("expected: %s" % expect)

        if verify is False:
            self.gLogging.info("trying to fix with: %s" % failsolve)

        if any(msg in output for msg in msg):
            if expect is True:
                self.gLogging.info("condition passed")
                return True
            else:
                if verify is False:
                    for fixstep in failsolve:
                        self.gLogging.info("running fix step: %s" % fixstep)
                        runUuid(result[6], fixstep)
                else:
                    pass
                return False
        else:
            if expect is True:
                if verify is False:
                    for fixstep in failsolve:
                        self.gLogging.info("running fix step (expect): %s" % fixstep)
                        runUuid(result[6], fixstep)
                else:
                    pass
                return False
            else:
                self.gLogging.info("condition passed")
                return True

    steps = [step['step'] for step in yfile if step.get('step', None) is not None]

    if len(steps) == 0:
        self.gLogging.critical("no steps to run has been found")
    else:
        pass
        if stopping:
            self.gLogging.show("--- press Enter to connect to hosts ---")
            input()

        #do connect to a hosts
        self.gCommand.close()
        self.gCommand.connect()
        # get list of active connections
        self.gLogging.show("working on: %s hosts" % str(len(self.gCommand.connections)))

    for step in steps:
        if stopping:
            self.gLogging.show(" ")
            self.gLogging.show("--- press Enter to run a next step.. ---")
            self.gLogging.show(" ")
            input()

        self.gLogging.show("--- cmd: %s ---" % step['cmd'])
        self.gLogging.show("--- desc: %s ---" % step.get('desc', ''))

        cmd = step['cmd']
        # running command
        runcmd(cmd)

        for result in self.gCommand.result:
            for condition in step.get('fail', [None]):
                if condition is not None:
                    if analyze(condition, result):
                        pass
                    else:
                        runUuid(result[6], cmd)
                        if analyze(condition, result, verify=True):
                            pass
                        else:
                            print("stopping flow...")
                            removeUuid(result[6])
                            break
        if self.gCommand.gConfig['PANACEUM']['showpicked'] == 'YES':
            self.gCommand.gHosts.pickHosts(_printing=True)

    if stopping:
        self.gLogging.show("--- press Enter to close active connections ---")
        input()

    # do connect to a hosts
    self.gCommand.close()


if __name__ == '__main__':
    yamlExecutor(1, 'file.yaml', True)
