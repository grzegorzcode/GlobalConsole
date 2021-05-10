import os
import subprocess
from collections import defaultdict
from collections import namedtuple
import re
# pyinstaller  --onefile scannning.py


Database = namedtuple('Database', ('name', 'profile'))


class Instance:
    def __init__(self):
        self._databases = []

    def report_db(self, name, profile):
        self._databases.append(Database(name, profile))

    def show(self):
        for db in self._databases:
            print(db.name, db.profile)


class Installation:
    def __init__(self):
        self._instances = defaultdict(Instance)

    def get_instance(self, name):
        return self._instances[name]

    def show(self):
        for key, value in self._instances.items():
            print(key)
            value.show()


class ScanBook:
    def __init__(self):
        self.installations = defaultdict(Installation)

    def get_installation(self, name):
        return self.installations[name]

    def show(self):
        for key, value in self.installations.items():
            print(key)
            value.show()


class ScanBookMixin:
    __shared_state = {}
    scan_book = None

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.scan_book:
            self.scan_book = ScanBook()

    def report_db(self, hostname, installation, instance, profile, db):
        input_installation = self.scan_book.get_installation(installation)
        input_instance = input_installation.get_instance(instance)
        input_instance.report_db(db, profile)


#
class ScanInstallations(ScanBookMixin):
    def __init__(self, hostname):
        super(ScanInstallations, self).__init__()
        self.hostname = hostname

    def run(self):
        results = subprocess.check_output(['/usr/local/bin/db2ls'])
        for line in results.splitlines():
            if line.startswith(bytearray("/", 'utf8')) and b'bashrc' not in line:
                install = line.decode("utf-8").split(" ")[0]
                ScanInstances().run(self.hostname, install)
        self.scan_book.show()


class ScanInstances:
    def __init__(self):
        pass

    def run(self, hostname, installation):
        instances_process = subprocess.check_output(["%s/bin/db2ilist" % installation])
        for line in instances_process.splitlines():
            if b'bashrc' not in line:
                instance = line.decode("utf-8")
                profile_process = os.popen('sudo su - -c "cat /etc/passwd | grep ^%s: | cut -d: -f6"' % instance).read().strip()
                ScanDbs().run(hostname, installation, instance, profile_process)


class ScanDbs(ScanBookMixin):
    def __init__(self):
        super(ScanDbs, self).__init__()

    def run(self, hostname, installation, instance, profile):
        profile_file = '%s/sqllib/db2profile' % profile
        db_process = os.popen('sudo su - -c ". %s; db2 list db directory"' % profile_file).read().strip()
        for line in re.findall('entry.*?Catalog', str(db_process), re.DOTALL):
            if "Indirect" in line:
                for names in line.splitlines():
                    if "name" in names:
                        db = names.split("=")[1].split("Database")[0].split("\\r")[0].strip()
                        self.report_db(hostname, installation, instance, profile, db)
#


gscanner = ScanInstallations('sample hostname')  # get from os package
gscanner.run()


