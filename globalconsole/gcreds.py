"""
.. module:: gcreds
   :platform: Linux
   :synopsis: Credentials Module for GlobalConsole

.. moduleauthor:: Grzegorz Cylny

"""
from tinydb import TinyDB, Query
import os
from Crypto.Cipher import AES
import base64
from getpass import getpass
from operator import itemgetter
#
from globalconsole.gutils import GcUtils as gutils

class GcCreds:
    """This class features:

    -handle GC definition of credentials


    """
    def __init__(self, config, logger, credfile=None):
        """
        Construct object

        Args:
            config (object): holds instance of GcConfig class
            logger (object): holds instance of GcLogging class
            credfile (str): json file with definitions


        """
        # enable logging and config, create a proper objects
        self.gLogging = logger
        self.gConfig = config.config
        #if credfile not provided, use default one from config file
        #start TinyDB object
        try:
            if credfile is None:
                credfile = "{}/{}".format(gutils.gcpath(), self.gConfig['JSON']['credfile'])
                self.credfile = TinyDB(credfile)
                self.credtable = self.credfile.table("CREDS")
            else:
                self.credfile = TinyDB(credfile)
                self.credfile = self.credfile.table("CREDS")
        except Exception:
            self.gLogging.critical("credentials definitions cannot be loaded")


    def importCsvAsCreds(self, filename):
        """
        This method imports csv file with credentials.

        Args:
            filename (str): path to csv file with credentials definitions

        **csv file must follow format(no headers):**

        **credname,username,password,path_to_key,key_password,use_password_or_key*,encrypted_yes_or_no,env_var_used_to_encrypt**

        *valid options: password | key

        Examples:

            format:

            >>> rootVM,root,MyPass,/path/to/key,key_password,password,no,GC_KEY

            execution:

            >>> importCsvAsCreds("creds/creds.csv")
        """
        #todo strip whitespace
        self.gLogging.debug("importCsvAsCreds invoked")
        MyCred = Query()
        try:
            with open(filename, 'r') as infile:
                for line in infile:
                    if len(line) > 4:
                        self.credtable.upsert({"credname": line.split(",")[0], "username": line.split(",")[1], "password": line.split(",")[2], "key": line.split(",")[3], "key_password": line.split(",")[4], "use": line.split(",")[5], "encrypted": line.split(",")[6], "secret_env_key": line.split(",")[7].strip("\n")}, MyCred.credname == line.split(",")[0])
        except Exception:
            self.gLogging.error("cannot open or invalid csv file: " + filename)

    def updateCred(self, definition, credname):
        """
        This method updates selected credential


        Args:
            definition (dict): dictionary with credential definition
            credname (str): credential name to update


        Examples:

            >>> updateCred({'username': 'user1', 'use': 'key'}, 'credname3')

        """
        self.gLogging.debug("updateCred invoked")
        MyCred = Query()
        try:
            self.credtable.update(definition, MyCred.credname == credname)
        except Exception:
            self.gLogging.error("cannot update credential: " + credname)

    def removeCred(self, credname):
        """
        This method removes selected credential

        Args:
            credname (str): credential name to remove

        Examples:

            >>> removeCred('credname3')


        """
        self.gLogging.debug("removeCred invoked")
        MyCred = Query()
        try:
            self.credtable.remove(MyCred.credname == credname)
        except Exception:
            self.gLogging.error("cannot remove credname: " + credname)

    def purgeCreds(self):
        """
        This method removes all credentials

        Examples:

            >>> purgeCreds()

        """
        self.gLogging.debug("purgeCreds invoked")
        try:
            self.credtable.purge()
        except Exception:
            self.gLogging.error("cannot purge credentials " )

    def searchCredName(self, credname):
        """
        This method searches for a credential by name

        Args:
            credname (str): credential name to find

        Returns:
            list: credential definition as dict, packed into list object

        Examples:

            >>> searchCredName('credname3')

        """
        self.gLogging.debug("searchCredName invoked")
        MyCred = Query()
        try:
            return self.credtable.search(MyCred.credname == credname)
        except Exception:
            try:
                return self.credtable.search(MyCred.credname == credname)
            except Exception:
                return self.gLogging.error("cannot search with credential name: " + credname)

    def getCreds(self, show, sort_reverse, *args):
        """
        This method prints most important info about each credential in a tabular form.

        Args:
            show (bool): show passwords as plain text
            sort_reverse (bool): reverse order of sorting
            *args (list): list of columns to be a sorting key

        Examples:

            >>> getCreds(True, False, 'username', 'encrypted')

        """
        self.gLogging.debug("getCreds invoked")
        #list of records to display
        templist = list()
        docs = self.credtable.all()

        result = sorted(docs, key=itemgetter(*args), reverse=sort_reverse)
        try:
            for cred in result:
                if show:
                    passwds = self.decryptPasswds(cred)
                    passwd = passwds[0]
                    key_passwd = passwds[1]
                else:
                    passwd = "********"
                    key_passwd = "********"

                templist.append([cred.doc_id, cred["credname"], cred["username"], passwd, cred["key"], key_passwd, cred["use"], cred["encrypted"], cred["secret_env_key"]])
            self.gLogging.tab(templist, ["id", "credname", "username", "password", "key", "key_password", "use", "encrypted", "secret_env_key"])
        except Exception:
            self.gLogging.error("cannot get creds definitions")

    def exportCredsToCsv(self, outfile=""):
        """
        This method exports csv file with credentials.

        Args:
            outfile (str): path to csv file with credentials definitions

        **csv file format:**

        **credname,username,password,path_to_key,key_password,use_password_or_key*,encrypted_yes_or_no,env_var_used_to_encrypt**

        *valid options: password | key

        Examples:

            format:

            >>> rootVM,root,MyPass,/path/to/key,key_password,password,no,GC_KEY

            execution:

            >>> exportCredsToCsv("creds/credsExp.csv")

        """
        self.gLogging.debug("exportCredsToCsv invoked")
        try:
            with open(outfile, "w") as f:
                for cred in self.credtable.all():
                    f.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    cred["credname"], cred["username"], cred["password"], cred["key"], cred["key_password"], cred["use"], cred["encrypted"], cred["secret_env_key"]))
                self.gLogging.info("successfully exported to %s" % outfile)
        except Exception:
            self.gLogging.error("cannot export credentials definitions to: " + outfile)

    def _upto16(self, passwd):
        """
        Internal method to generates string with at least 16 signs and divisible by 16

        Args:
            passwd (str): string to proceed

        Examples:

            >>> _upto16('MyPasswd')

        """
        modpass = divmod(16, len(passwd))
        if int(modpass[0]) == int(0):
            modpass = divmod(len(passwd), 16)
            return passwd * modpass[0] + passwd[:16 - modpass[1]]
        else:
            return passwd * modpass[0] + passwd[:modpass[1]]

    def encryptPasswds(self, _utest=False):
        """
        This method encrypts passwords in loaded json with definitions of credentials. Fields 'password' and 'key_password' are subjects of encryption.

        Args:
            _utest (bool): internal parameter, only for automatic testing, method doesn't need environmental variable to be set

        Examples:

            >>> encryptPasswds(_utest=False)

        """
        secret_key = ""
        secret_key2 = " "
        #print(_utest, 'iiiiiiiiiiiiii')
        try:
            if _utest:
                secret_key = "MySecretPass"
            else:
                #get value of env variable, set by export VAR=xyz
                secret_key = os.environ[self.gConfig['JSON']['decrypt_key_os_var']]

            if len(secret_key) < 8:
                self.gLogging.warning("secret key must be 8 signs at least, change %s value. terminated.." % self.gConfig['JSON']['decrypt_key_os_var'])
                #sys.exit(1)
                raise KeyError
            secret_key = str.encode(self._upto16(secret_key))
            self.gLogging.info("secret key successfully entered using %s env variable" % self.gConfig['JSON']['decrypt_key_os_var'])
        except KeyError:
            while secret_key != secret_key2:
                secret_key = getpass("your secret key: ")
                secret_key2 = getpass("confirm: ")
                if secret_key == secret_key2:
                    if len(secret_key) < 8:
                        self.gLogging.warning("secret key must be 8 signs at least, change %s value. " % self.gConfig['JSON']['decrypt_key_os_var'])
                        secret_key = ""
                        secret_key2 = " "
                    else:
                        secret_key = str.encode(self._upto16(secret_key))
                        self.gLogging.info("secret key successfully entered ")
                        break
                else:
                    self.gLogging.info("passwords do not match.. try again")

        cipher = AES.new(secret_key, AES.MODE_ECB)

        ans = "N"
        if _utest:
            ans = "Y"
        else:
            self.gLogging.warning("ALL NOT ENCRYPTED PASSWORDS WILL BE AFFECTED, CONTINUE? [Y/n]")
            ans = input("answer: ")

        if ans == "Y":
            for cred in self.credtable.all():
                if cred["encrypted"] == "no":
                    try:
                        #password
                        msg_text = str.encode(cred["password"].rjust(32))
                        encoded = base64.b64encode(cipher.encrypt(msg_text))
                        cred["password"] = encoded.decode()
                        #key_password
                        msg_text = str.encode(cred["key_password"].rjust(32))
                        encoded = base64.b64encode(cipher.encrypt(msg_text))
                        cred["key_password"] = encoded.decode()
                        #encrypted var
                        cred["encrypted"] = "yes"
                        cred["secret_env_key"] = self.gConfig['JSON']['decrypt_key_os_var']
                        self.updateCred(cred, cred["credname"])
                        #pprint(cred)
                        self.gLogging.debug("successfully encrypted password for cred: %s - user %s" % (cred["credname"], cred["username"]))
                        self.gLogging.debug("successfully encrypted key password for cred: %s - user %s" % (cred["credname"], cred["username"]))
                    except Exception:
                        self.gLogging.critical("cannot encrypt passwords. process terminated..")
        else:
            print("skipped")

    def decryptPasswds(self, cred, _utest=False):
        """
        This method decrypts in memory passwords in loaded json with definitions of credentials. Fields 'password' and 'key_password' are subjects of dencryption.

        Args:
            _utest (bool): internal parameter, only for automatic testing, method doesn't need environmental variable to be set
            cred (dict): credential definition

        Returns:
            tuple: decrypted password, decrypted password to key (passwd, key_password)

        To decrypt you must provide secret key using env variable

        Raises:
        UnicodeDecodeError: Environmental variable must be not-empty unicode string

        Examples:

            >>> decryptPasswds(searchCredName('credname3'), _utest=False)

        """
        self.gLogging.debug("decryptPasswds invoked")

        if cred["encrypted"] == "yes":
            # decrypt:
            try:
                if _utest:
                    secret_key = str.encode(self._upto16("MySecretPass"))
                else:
                    secret_key = str.encode(self._upto16(os.environ[cred["secret_env_key"]]))

                cipher = AES.new(secret_key, AES.MODE_ECB)
                #pass
                encoded = str.encode(cred["password"].rjust(32))
                decoded = cipher.decrypt(base64.b64decode(encoded))
                password = decoded.decode().strip()
                # key
                encoded = str.encode(cred["key_password"].rjust(32))
                decoded = cipher.decrypt(base64.b64decode(encoded))
                key_password = decoded.decode().strip()

                # encrypted var
                # cred["encrypted"] = "yes"

                self.gLogging.debug(
                    "successfully decrypted password for: %s - user %s" % (cred["credname"], cred["username"]))
                self.gLogging.debug(
                    "successfully decrypted key password for: %s - user %s" % (cred["credname"], cred["username"]))

                return (password, key_password)

            except KeyError:
                self.gLogging.error("cannot decrypt password. environmental variable %s is not set" % self.gConfig['JSON']['decrypt_key_os_var'])
            except UnicodeDecodeError:
                self.gLogging.error("invalid secret_key provided. process terminated..")
            except Exception:
                self.gLogging.error("cannot decrypt password. process terminated..")

        else:
            return (cred["password"], cred["key_password"])

    def decryptPasswdsInFile(self, _utest=False):
        """
        This method decrypts in file passwords in loaded json with definitions of credentials. Fields 'password' and 'key_password' are subjects of dencryption.

        Args:
            _utest (bool): internal parameter, only for automatic testing, method doesn't need environmental variable to be set

        To decrypt you must provide secret key using env variable

        Examples:

            >>> decryptPasswdsInFile()

        """
        self.gLogging.debug("decryptPasswdsInFile invoked")

        utest = _utest
        if _utest:
            ans = "Y"
        else:
            self.gLogging.warning("ALL ENCRYPTED PASSWORDS WILL BE VISIBLE AS PLAIN TEXT, CONTINUE? [Y/n]")
            ans = input("answer: ")

        if ans == "Y":
            for cred in self.credtable.all():
                try:
                    passwds = self.decryptPasswds(cred, _utest=utest)
                    cred["password"] = passwds[0]
                    cred["key_password"] = passwds[1]
                    cred["encrypted"] = "no"
                    cred["secret_env_key"] = "None"
                    self.updateCred(cred, cred["credname"])
                except Exception:
                    self.gLogging.error("cannot decrypt passwords to file. process terminated..")


