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
    inlist = ['show', 'run']
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

        show_parser = subparsers.add_parser('show', description="show yaml", usage="yaml show <args>")
        show_parser.set_defaults(which='show')
        show_parser.add_argument('-v', '--verbose', action='store_true', help="yaml with logic analyzed")

        run_parser = subparsers.add_parser('run', description="run yaml file", usage="yaml run <args>")
        run_parser.set_defaults(which='run')
        run_parser.add_argument('-s', '--source', type=str, required=True, help="file to run, local or github")
        run_parser.add_argument('-S', '--stopping', action='store_false', required=False, help="disable stopping before next step execution")

        choice = vars(parser.parse_args(args.split()))
        if len(args) == 0:
            parser.print_help()
        elif choice['which'] == 'show':
            self.gLogging.show("yaml show " + str(choice['verbose']))
        elif choice['which'] == 'run':
            #self.gLogging.show("yaml run " + str(choice['source']))
            self.gCommand.yamlExecutor(source=choice['source'], stopping=choice['stopping'])
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

    try:
        hosts = [hosts['hosts'] for hosts in yfile if hosts.get('hosts', None) is not None][0]
        self.gLogging.info("hosts loaded from a yaml, location: %s" % hosts)
    except Exception:
        #TODO !!
        hosts = 'aa'
        self.gLogging.info("hosts loaded from a GC")


    try:
        creds = [creds['creds'] for creds in yfile if creds.get('creds', None) is not None][0]
        self.gLogging.info("creds loaded from a yaml, location: %s" % creds)
    except Exception:
        # TODO !!
        creds = 'aaa'
        self.gLogging.info("creds loaded from a GC")

    def runcmd(cmd):
        print("running cmd: %s" % cmd)

    def analyze(condition, result, verify=False):
        msg = condition.get('msg', None)
        expect = condition.get('expect', False)
        failsolve = condition.get('failsolve', [None])
        print("msg: ", msg)
        print("expect: ", expect)
        print("failsolve: ", failsolve)

        if any(msg in result for msg in msg):
            if expect is True:
                print("condition passed")
                return True
            else:
                if verify is False:
                    for fixstep in failsolve:
                        print("running fix step: ", fixstep)
                        runcmd(fixstep)
                else:
                    pass
                return False
        else:
            if expect is True:
                if verify is False:
                    for fixstep in failsolve:
                        print("running fix step (expect): ", fixstep)
                        runcmd(fixstep)
                else:
                    pass
                return False
            else:
                print("condition passed")
                return True


    steps = [step['step'] for step in yfile if step.get('step', None) is not None]

    if len(steps) == 0:
        self.gLogging.warning("no steps to run has been found")
    else:
        pass
        #do connect to a hosts
        #get a list of hosts, dbs etc.. uuids?

    for step in steps:
        #load hosts to use

        for condition in step.get('fail', [None]):
            cmd = step['cmd']
            desc = step.get('desc', '')
            #running command
            runcmd(cmd)
            #result = runcmd(cmd)
            result = """
                    command completed
                    0 erWror, 1 warning. 
                    closing
                    """

            print("with desc: %s" % desc)
            if condition is not None:
                if analyze(condition, result):
                    pass
                else:
                    #rerun command
                    # result = runcmd(cmd)
                    runcmd(cmd)
                    if analyze(condition, result, verify=True):
                        pass
                    else:
                        print("stopping flow...")

                        #remove this host path from next step execution list

                        break

        if stopping:
            print("--- press Enter to run a new step.. ---")
            #self.gLogging.show("press any key to continue..")
            input()

        print("---")



if __name__ == '__main__':
    yamlExecutor(1, 'file.yaml', True)
