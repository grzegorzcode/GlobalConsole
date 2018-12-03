from tinydb import TinyDB, Query
from operator import itemgetter
#
from globalconsole3.gutils import GcUtils as gutils


class GcHosts:
    def __init__(self, config, logger, hostfile=None):
        # enable logging and config, add some utils, create a proper objects
        self.gLogging = logger
        self.gConfig = config.config
        #used by _indexHosts, list of 5element tuples contain uuids from every level
        self.hosts_idx = []
        #used to drill down hierarchy of objects such as groups, hosts..
        self.pick_drill = ""
        # if hostfile not provided, use default one from config file
        # start TinyDB object
        try:
            if hostfile is None:
                hostfile = "{}/{}".format(gutils.gcpath(), self.gConfig['JSON']['hostfile'])
                self.hostfile = TinyDB(hostfile)
                self.hosttable = self.hostfile.table("HOSTS")
            else:
                self.hostfile = TinyDB(hostfile)
                self.hosttable = self.hostfile.table("HOSTS")
            #refresh uuids
            self._indexHosts()
        except Exception as e:
            self.gLogging.critical("hosts definitions cannot be loaded")


    def importCsvAsHosts(self, filename):
        self.gLogging.debug("importCsvAsHosts invoked")
        MyHost = Query()
        try:
            with open(filename, 'r') as infile:
                for line in infile:
                    if len(line) > 4:
                        self.hosttable.upsert(
                            {"group": line.split(",")[4].strip("\n"), "group_uuid": gutils.uuid_generator(line.split(",")[4].strip("\n")), "group_checked": self.gConfig['JSON']['pick_yes'], "host_checked": self.gConfig['JSON']['pick_yes'], "port": line.split(",")[2],
                             "installations": [], "scanned": "no",
                             "def_cred": line.split(",")[3], "host": line.split(",")[1], "host_uuid": gutils.uuid_generator(line.split(",")[4].strip("\n") + line.split(",")[0]),
                             "hostname": line.split(",")[0]}, MyHost.hostname == line.split(",")[0])
            self._indexHosts()
        except Exception:
            self.gLogging.error("cannot open or invalid csv file: " + filename)

    def updateHost(self, definition, hostname):
        self.gLogging.debug("updateHost invoked")
        MyHost = Query()
        try:
            self.hosttable.update(definition, MyHost.hostname == hostname)
            self._indexHosts()
        except Exception:
            self.gLogging.error("cannot update hostname: " + hostname)

    def removeHost(self, hostname):
        self.gLogging.debug("removeHost invoked")
        MyHost = Query()
        try:
            self.hosttable.remove(MyHost.hostname == hostname)
            self._indexHosts()
        except Exception:
            self.gLogging.error("cannot remove hostname: " + hostname)

    def purgeHosts(self):
        self.gLogging.debug("purgeHosts invoked")
        try:
            self.hosttable.purge()
            self.hosts_idx = []
        except Exception:
            self.gLogging.error("cannot purge hostnames " )

    def searchHostName(self, hostname):
        self.gLogging.debug("searchHostName invoked")
        MyHost = Query()
        try:
            return self.hosttable.search(MyHost.hostname == hostname)
        except Exception:
            try:
                return self.hosttable.search(MyHost.hostname == hostname)
            except Exception:
                return self.gLogging.error("cannot search with hostname: " + hostname)


    def searchGroupName(self, groupname):
        self.gLogging.debug("searchGroupName invoked")
        MyHost = Query()
        try:
            return self.hosttable.search(MyHost.group == groupname)
        except Exception:
            return self.gLogging.error("cannot search with groupname: " + groupname)


    def searchByUuid(self, uuid):
        self.gLogging.debug("searchByUuid invoked")

        try:
            MyGroup = Query()
            MyHost = Query()
            MyInstall = Query()
            MyInstance = Query()
            MyDb = Query()

            out_dict = {0: "group", 1: "host", 2: "installation", 3: "instance", 4: "db"}

            lvl = [(a, b, c, d, e).index(uuid) for a, b, c, d, e in self.hosts_idx if
                   a == uuid or b == uuid or c == uuid or d == uuid or e == uuid]

            level = out_dict[lvl[0]]

            #out_dict = {"group": "group_uuid", "host": "host_uuid", "installation": "installation_uuid", "instance": "instance_uuid", "db": "db_uuid"}

            if level == 'group':
                return self.hosttable.search(MyGroup.group_uuid == uuid), level
            elif level == 'host':
                return self.hosttable.search(MyHost.host_uuid == uuid), level
            elif level == 'installation':
                return self.hosttable.search(MyHost.installations.any(MyInstall.installation_uuid == uuid)), level
            elif level == 'instance':
                return self.hosttable.search(MyHost.installations.any(MyInstall.instances.any(MyInstance.instance_uuid == uuid))), level
            else:
                return self.hosttable.search(MyHost.installations.any(MyInstall.instances.any(MyInstance.databases.any(MyDb.db_uuid == uuid)))), level
        except Exception:
            self.gLogging.error("cannot search over uuid: " + uuid)

    def _indexHosts(self):
        self.gLogging.debug("_indexHosts invoked")

        try:
            self.hosts_idx = []

            seen_groups = set()
            for i in self.hosttable.all():
                seen_groups.add((i['group'], i['group_uuid']))
            templist = list()
            for group, group_uuid in seen_groups:
                for host in self.searchGroupName(group):
                    if host['group'] == group:
                        templist.extend([group_uuid, host['host_uuid'], 0, 0, 0])
                        if len(host["installations"]) == 0:
                            host["installations"] = [{'installation_name': "__NA__", 'instances': []}]
                        for install in host["installations"]:
                            if install['installation_name'] != "__NA__":
                                templist.insert(2, install['installation_uuid'])
                            if len(install["instances"]) == 0:
                                install["instances"] = [{'instance_name': "__NA__", 'databases': []}]
                            for instance in install["instances"]:
                                if instance['instance_name'] != "__NA__":
                                    templist.insert(3, instance['instance_uuid'])
                                if len(instance["databases"]) == 0:
                                    instance["databases"] = [{'db_name': "__NA__"}]
                                for db in instance["databases"]:
                                    if db['db_name'] != "__NA__":
                                        templist.insert(4, db['db_uuid'])
                                    self.hosts_idx.append(tuple(templist[0:5]))
                        templist = []
        except Exception:
            self.gLogging.error("cannot index loaded hosts")

    def pickHosts(self, manual=False, reset=False, _printing=True, collapse=True, uuids=[], resetOption='E'):
        self.gLogging.debug("pickHosts invoked")

        try:
            def get_structure():
                choices = []
                seen_groups = set()
                for i in self.hosttable.all():
                    seen_groups.add((i['group'], i['group_checked'], i['group_uuid']))

                seen_groups = sorted(seen_groups, key=lambda x: x[0])

                for group, group_checked, group_uuid in seen_groups:
                    choices.append(gutils.color_pick(self.gConfig, "group: " + group, group_checked) + gutils.color_uuid(" id: " + group_uuid))
                    for host in sorted(self.searchGroupName(group), key=lambda x: x['hostname']):
                        choices.append(gutils.color_pick(self.gConfig, "\t--host: " + host["hostname"], host["host_checked"]) + gutils.color_uuid(" id: " + host['host_uuid']))
                        if collapse:
                            for install in host["installations"]:
                                if install['installation_name'] != '__NA__':
                                    choices.append(gutils.color_pick(self.gConfig, "\t\t--install: " + install["installation_name"], install['installation_checked']) + gutils.color_uuid(" id: " + install['installation_uuid']))
                                for instance in install["instances"]:
                                    if instance['instance_name'] != "__NA__":
                                        choices.append(gutils.color_pick(self.gConfig, "\t\t\t--instance: " + instance["instance_name"], instance["instance_checked"]) + gutils.color_uuid(" id: " + instance['instance_uuid']))
                                    for db in instance["databases"]:
                                        if db['db_name'] != "__NA__":
                                            choices.append(gutils.color_pick(self.gConfig, "\t\t\t\t--db: " + db["db_name"], db["db_checked"]) + gutils.color_uuid(" id: " + db['db_uuid']))
                #todo remove
                choices.append("STOP")
                return choices

            def reverse_pick(item, idx):
                if item == self.gConfig['JSON']['pick_yes']:
                    self.pick_drill = self.gConfig['JSON']['pick_no']
                    return self.gConfig['JSON']['pick_no']
                else:
                    if self.gConfig['JSON']['pick_no'] not in idx:
                        self.pick_drill = self.gConfig['JSON']['pick_yes']
                        return self.gConfig['JSON']['pick_yes']
                    else:
                        self.pick_drill = self.gConfig['JSON']['pick_no']
                        #todo replace with logging
                        print("\033[2J\033[1;1f")
                        print("! FORBIDDEN - ONE OF THE ITEMS ABOVE IS UNSELECTED !")
                        print("try again.. ")
                        return self.gConfig['JSON']['pick_no']

            def picker(search, groupreset="E"):
                if search == '0':
                    return -1
                if groupreset == "Y":
                    result = self.hosttable.all()

                    reseter = self.gConfig['JSON']['pick_yes']
                    for host in result:
                        #pathIdx = ('x')
                        host["group_checked"] = reseter
                        host["host_checked"] = reseter
                        for install in host["installations"]:
                            install["installation_checked"] = reseter
                            for instance in install["instances"]:
                                instance["instance_checked"] = reseter
                                for db in instance["databases"]:
                                    db["db_checked"] = reseter
                        # pprint(host)
                        self.updateHost(host, host["hostname"])

                elif groupreset == "N":
                    result = self.hosttable.all()

                    reseter = self.gConfig['JSON']['pick_no']

                    for host in result:
                        #pathIdx = ('x')
                        host["group_checked"] = reseter
                        host["host_checked"] = reseter
                        for install in host["installations"]:
                            install["installation_checked"] = reseter
                            for instance in install["instances"]:
                                instance["instance_checked"] = reseter
                                for db in instance["databases"]:
                                    db["db_checked"] = reseter
                        # pprint(host)
                        self.updateHost(host, host["hostname"])


                else:
                    if search != "NA":
                        result = self.searchByUuid(search)

                        if result[1] == 'group':

                            for host in result[0]:
                                pathIdx = ('x')
                                host["group_checked"] = reverse_pick(host["group_checked"], pathIdx)
                                host["host_checked"] = self.pick_drill
                                for install in host["installations"]:
                                    install["installation_checked"] = self.pick_drill
                                    for instance in install["instances"]:
                                        instance["instance_checked"] = self.pick_drill
                                        for db in instance["databases"]:
                                            db["db_checked"] = self.pick_drill
                                #pprint(host)
                                self.updateHost(host, host["hostname"])

                        elif result[1] == 'host':

                            for host in result[0]:
                                pathIdx = (host["group_checked"])
                                host["host_checked"] = reverse_pick(host["host_checked"], pathIdx)
                                for install in host["installations"]:
                                    install["installation_checked"] = self.pick_drill
                                    for instance in install["instances"]:
                                        instance["instance_checked"] = self.pick_drill
                                        for db in instance["databases"]:
                                            db["db_checked"] = self.pick_drill
                                #pprint(host)
                                self.updateHost(host, host["hostname"])

                        elif result[1] == 'installation':

                            for host in result[0]:
                                for install in host["installations"]:
                                    if install["installation_uuid"] == search:
                                        pathIdx = (host["group_checked"], host["host_checked"])
                                        install["installation_checked"] = reverse_pick(install["installation_checked"], pathIdx)
                                        for instance in install["instances"]:
                                            instance["instance_checked"] = self.pick_drill
                                            for db in instance["databases"]:
                                                db["db_checked"] = self.pick_drill
                                #pprint(host)
                                self.updateHost(host, host["hostname"])

                        elif result[1] == 'instance':

                            for host in result[0]:
                                for install in host["installations"]:
                                    for instance in install["instances"]:
                                        if instance["instance_uuid"] == search:
                                            pathIdx = (host["group_checked"], host["host_checked"], install["installation_checked"])
                                            instance["instance_checked"] = reverse_pick(instance["instance_checked"], pathIdx)
                                            for db in instance["databases"]:
                                                db["db_checked"] = self.pick_drill
                                #pprint(host)
                                self.updateHost(host, host["hostname"])


                        elif result[1] == 'db':

                            for host in result[0]:
                                for install in host["installations"]:
                                    for instance in install["instances"]:
                                        for db in instance["databases"]:
                                            if db["db_uuid"] == search:
                                                pathIdx = (host["group_checked"], host["host_checked"], install["installation_checked"], instance["instance_checked"])
                                                db["db_checked"] = reverse_pick(db["db_checked"], pathIdx)
                                #pprint(host)
                                self.updateHost(host, host["hostname"])

                        else:
                            pass

            def manual_picker(uuids=[]):
                for uuid in uuids:
                    picker(uuid)

            def print_items(_printing=True, collapse=True):
                lines = get_structure()
                lines = lines[:-1]
                for line in lines:
                    if _printing:
                        if collapse:
                            print(line)
                        else:
                            if 'group' in line or 'host' in line:
                                print(line)
                if not _printing:
                    return lines

            if manual:
                manual_picker(uuids=uuids)
                print_items(_printing=_printing, collapse=collapse)
            elif reset:
                picker("NA", groupreset=resetOption)
                print_items(_printing=_printing, collapse=collapse)
            else:
                #lines are needed to show connections
                if _printing:
                    print_items(_printing=_printing, collapse=collapse)
                else:
                    res = print_items(_printing=_printing, collapse=True)
                    return res

        except Exception:
            self.gLogging.error("cannot pick loaded hosts")

    def getHosts(self, sort_reverse, *args):
        self.gLogging.debug("getHosts invoked")
        templist = list()
        docs = self.hosttable.all()

        result = sorted(docs, key=itemgetter(*args), reverse=sort_reverse)
        try:
            for host in result:
                templist.append(
                    [host["hostname"], host["host"], host["port"], host["group"], host["def_cred"], host["scanned"]])
            self.gLogging.tab(templist, ["hostname", "host", "port", "group", "def_cred", "scanned"])

        except Exception:
            self.gLogging.error("cannot get hosts definitions")

    def exportHostsToCsv(self, outfile=""):
        self.gLogging.debug("exportHostsCsv invoked")
        try:
            with open(outfile, "w") as f:
                for host in self.hosttable.all():
                    f.write("%s,%s,%s,%s,%s\n" % (
                    host["hostname"], host["host"], host["port"], host["def_cred"], host["group"]))
                self.gLogging.info("successfully exported to %s" % outfile)
        except Exception:
            self.gLogging.error("cannot export hosts definitions to: " + outfile)

