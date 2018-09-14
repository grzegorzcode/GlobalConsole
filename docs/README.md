===============

GlobalConsole

===============

GlobalConsole is a tool designed to run commands on many Linux/Unix machines at the same time.
What distinguishes GlobalConsole from similar software is ability to handle DB2 database environments.
You can:

- run os commands
- run db2 specific commands
- use scp over connected servers 

It's worth to mention, also:

- **multithreaded**
- stored passwords can be encrypted
- output of command can be saved within **excel** or **csv** file
- hosts can be picked up using visual editor
- local shell commands are supported
- history of invoked commands is persistent over sessions
- custom variables can be set to improve productivity
- batch mode with checking output's results is available
- docker scripts to build and run GlobalConsole are provided


----------------
Installation
----------------

GlobalConsole can be installed on Linux, Windows, OSX.

- Linux : supports both venv and docker path 

- Windows : supports docker path (needs testing and custom ``gDockerBuild.sh`` and ``gDockerRun.sh`` scripts)

- OSX : supports both venv and docker path 



^^^^^^^^^
docker
^^^^^^^^^

GlobalConsole was made with Docker in mind. 
Every release has its own *Dockerfile*. You don't have to install all required packages at your workstation.

To successfully put GlobalConsole in a container:

1. move all files to a desired directory, for example:

*/home/user/DockerVMs/GlobalConsole/GC*

2. build your image (provided Dockerfile will be used) using ``gDockerBuild.sh`` script or change its content to your needs:

.. code-block:: bash

    $ ./gDockerBuild.sh


.. note::

    File **Dockerfile** will be used. 


you should get something like:

.. code-block:: bash

    $ docker images
    REPOSITORY                   TAG                 IMAGE ID            CREATED              SIZE
    global_console               v2.0.0              35f57b7c4918        16 seconds ago       710MB


3. run container using ``gDockerRun.sh`` script or change its content to your needs:

.. code-block:: bash

    $ ./gDockerRun.sh


4. use executable ``GlobalConsole`` to work with GlobalConsole

.. note::

    remember to set **GC_KEY** env variable to encrypt/decrypt passwords before starting GlobalConsole
    example: export GC_KEY=MySecretPass 

.. code-block:: bash

    $ export GC_KEY=MySecretPass 
    $ GlobalConsole


We start container with volume option, so all changes will be persistent. 
However, your secret_key is save - container session will be removed every single time.


--

If you want to remove an old version, simply:

1. remove directory with source directory

.. note::

    you may want to copy your important files; content of directories:
    batch, config, creds, download, hosts, logs, spool, upload, vars


2. find you image

.. code-block:: bash

    $ docker images
    REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
    global_console               v2.0.0              86f270035c22        About an hour ago   728MB


3. delete image

.. code-block:: bash

    $ docker rmi 86f270035c22



^^^^^^^
venv
^^^^^^^

1. install latest python3 (and python3-dev(el) package)

2. move all files to a desired directory, for example:

*/home/user/DockerVMs/GlobalConsole/GC*

3. create python3 virtual environment

more info `https://docs.python.org/3/library/venv.html <https://docs.python.org/3/library/venv.html>`_ 


.. code-block:: bash
    
    cd /home/user/DockerVMs/GlobalConsole/GC/
    
    mkdir venv
    
    python3 -m venv /home/user/DockerVMs/GlobalConsole/GC/venv

    source venv/bin/activate


4. install all required packages

.. code-block:: bash
    
    pip3 install -r requirements.txt

5. start GlobalConsole

.. code-block:: bash

    cd /home/user/DockerVMs/GlobalConsole/GC
    
    source venv/bin/activate
    
    unset HISTFILE
    
    export GC_KEY=MySecretPass
    
    ./GlobalConsole


.. note::

    ``unset HISTFILE`` is to disable shell history for a session, therefore your GC_KEY will not be stored 
    
    you can put commands from point 5 to a runnable script 
    
    
----------------
Quickstart
----------------

You need a simple setup to start using GlobalConsole.


1. Create csv file with definitions of credentials. 
The file will be called *credsVM.csv* to end of this chapter.

.. code-block:: bash

    rootVM,root,MySuperPass,/path/to/key,key_password,password,no,GC_KEY

where fields means:

- rootVM : credential's chosen name

- root : user's name

- MySuperPass : user's password

- /path/to/key : path to your ssh private key. make path visible or copy file to ``creds`` directory if using docker
 
- key_password : password to ssh private key

- password: should GlobalConsole use *password* or *key* as a connection method
 
- no : is password encrypted

- GC_KEY : name of the bash environmental variable, that will be used to encrypt credentials
     

.. note::

    **creds** directory seems to be a good place to store this file
    

2. Create csv file with definitions of hosts.
The file will be called *hostsVM.csv* to end of this chapter.

.. code-block:: bash

    myhost1,192.168.57.101,22,rootVM,VM
    myhost2,192.168.56.102,22,rootVM,VM

where fields means (based on the first row):

- myhost1 : host's chosen name

- 192.168.57.101 : host's ip

- 22 : host's ssh port

- rootVM : name of a credential. **it has to be a valid credential's chosen name**, please take a look on step 1 for more details

- VM : host's chosen name of a group. 
 

.. note::

    **hosts** directory seems to be a good place to store this file
  
    
3. Set your encryption key, start GC and import created files

.. code-block:: bash
    
    $ export GC_KEY=MyEncryptPass
    
    $ GlobalConsole
    
    gc> cred import -f creds/credsVM.csv
    
    gc> cred show
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    1 │ rootVM     │ root       │ ********   │ /path/to/key │ ********       │ password │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    
    gc> host import -f hosts/hostsVM.csv
    
    gc> host show
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    1 │ myhost1    │ 192.168.57.101 │     22 │ VM      │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    2 │ myhost2    │ 192.168.56.102 │     22 │ VM      │ rootVM     │ no        │
    ╘══════╧════════════╧════════════════╧════════╧═════════╧════════════╧═══════════╛



.. note::

    use ``help`` to see all available commands. every command has help at every level, check:
    
    gc> help
    
    gc> cred -h
    
    gc> cred update -h
    
       
    
4. Connect to hosts, run os command, scan db2 infrastructure, run db2 command  

.. code-block:: bash

    gc> conn connect -Y
    successfully connected to: 192.168.57.101 using password
    successfully connected to: 192.168.56.102 using password
    myhost2 (192.168.56.102:22) says: localhost.localdomain 
    myhost1 (192.168.57.101:22) says: localhost.localdomain 
    
    gc> run os  ls -la /tmp | wc -l 
    --------myhost1 (192.168.57.101:22)--------
    
    27
    
    --------myhost2 (192.168.56.102:22)--------
    
    23
    
    gc> run scan -Y
    group: VM id: 5645848e-8cd4-5ff5-87fe-2a906d660aa0
        --host: myhost1 id: 3cd7926b-dbe7-5b70-ba27-d3a386fb5fe5
            --install: /opt/ibm/db2/V10.5 id: dc388c45-a205-5c5b-a8ec-5232d3ce3eae
                --instance: db2inst1 id: 70683dff-e5a7-54f6-b7ec-12544d0dab47
                    --db: TEST id: e1936ead-44ef-508a-942a-005bedd3cf78
                    --db: TEST2 id: af2762ee-ac69-5189-ab87-a39545f2a5e2
                --instance: cogpi id: 65c3a425-c564-5ae8-a70e-dc58d6117576
                    --db: TEST3 id: b4f128ba-4efc-58d7-99a2-41aee7e9a457
        --host: myhost2 id: e411ae67-8526-5d18-b05a-b5e57b486a6a
            --install: /opt/ibm/db2/V10.5 id: 7d1c87c7-db3d-590b-a0a9-1cc22c18b674
                --instance: db2inst1 id: d2f3792d-b148-5127-b7af-1c95d0fa1489
                    --db: TEST id: 72210296-5358-5dd5-96c1-21a4473d2a22
                    --db: TEST2 id: 4ccfe200-5ce8-5070-a904-fbc43dedf353
                --instance: cogpi id: 77e31b62-e1a4-5d82-a67e-bd6195661291
                    --db: TEST3 id: 1fa645c2-69cc-5026-8a5b-67804cee9eb9

    gc> run db2 select * from sysibm.sysdummy1
    
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ....


5. Exit program

.. code-block:: bash
    
    gc> exit


.. note::
    
    you can use **quit**, also

----------------
Credentials
----------------

.. code-block:: bash

    gc> cred
    usage: cred <command> [<args>]
    
    work with credentials
    
    positional arguments:
      {import,update,rem,purge,show,export,encrypt,decrypt}
    
    optional arguments:
      -h, --help            show this help message and exit

you can manage your credentials with ``cred`` command. 
credentials are being stored in **creds/creds.json** file by default.    

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import : import csv file with definitions of credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash

    gc> cred import -f creds/credsVM.csv

**csv file must follow format(no headers):**

**credname,username,password,path_to_key,key_password,use_password_or_key, encrypted_yes_or_no,env_var_used_to_encrypt**

.. note::

    - valid options for field **use_password_or_key** : password | key
    
    - if field, for example path_to_key, is empty, use empty string : ..,password,,,use_password_or_key..

Sample file:

.. code-block:: bash

    rootVM,root,MySuperPass,/path/to/key,key_password,password,no,GC_KEY
    usrVM,usr,MyUberPass,/path/to/key,PassToKey,key,no,GC_KEY


.. note::

    ``cred import`` uses ``upsert`` operation, so can be used as a global update.
    If given **credname** doesn't exist, will be added. 
    If does exist, all parameters will be updated for this **credname**.  

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
update : update definition of credential
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash

    gc> cred show
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    1 │ rootVM     │ root       │ ********   │ /path/to/key │ ********       │ password │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    active connections: 0 
    gc> cred update -c rootVM -p use -v key
    active connections: 0 
    gc> cred show
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤═══════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use   │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪═══════╪═════════════╪══════════════════╡
    │    1 │ rootVM     │ root       │ ********   │ /path/to/key │ ********       │ key   │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧═══════╧═════════════╧══════════════════╛

.. note::

    use ``cred show`` output headers to obtain names of parameters to change. field ``id`` is invalid, however

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
rem : remove selected credential (credname)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> cred rem -c rootVM

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
purge : purge all credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> cred purge -Y

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
show : show stored credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can hide or show passwords, reverse order of sorting, and choose sorting fields.

.. code-block:: bash
    
    gc> cred show 
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    1 │ credname   │ username   │ ********   │ /path/to/key │ ********       │ key      │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    2 │ credname2  │ username2  │ ********   │              │ ********       │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    3 │ credname3  │ username3  │ ********   │              │ ********       │ password │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    gc> cred show -e 
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    1 │ credname   │ username   │ password   │ /path/to/key │ key_password   │ key      │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    2 │ credname2  │ username2  │ password2  │              │                │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    3 │ credname3  │ username3  │ password3  │              │                │ password │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    gc> cred show -e -r
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    3 │ credname3  │ username3  │ password3  │              │                │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    2 │ credname2  │ username2  │ password2  │              │                │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    1 │ credname   │ username   │ password   │ /path/to/key │ key_password   │ key      │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    gc> cred show -e -r -f use username
    ╒══════╤════════════╤════════════╤════════════╤══════════════╤════════════════╤══════════╤═════════════╤══════════════════╕
    │   id │ credname   │ username   │ password   │ key          │ key_password   │ use      │ encrypted   │ secret_env_key   │
    ╞══════╪════════════╪════════════╪════════════╪══════════════╪════════════════╪══════════╪═════════════╪══════════════════╡
    │    3 │ credname3  │ username3  │ password3  │              │                │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    2 │ credname2  │ username2  │ password2  │              │                │ password │ no          │ GC_KEY           │
    ├──────┼────────────┼────────────┼────────────┼──────────────┼────────────────┼──────────┼─────────────┼──────────────────┤
    │    1 │ credname   │ username   │ password   │ /path/to/key │ key_password   │ key      │ no          │ GC_KEY           │
    ╘══════╧════════════╧════════════╧════════════╧══════════════╧════════════════╧══════════╧═════════════╧══════════════════╛
    
.. note::

    use output headers to obtain names of parameters to sort on. field ``id`` is invalid, however
    
    if no sorting fields, **username** is default
    
    you can change default table format in **config.ini** file, parameter ``logging_tab_fmt``
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
export : export definitions of credentials to csv file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> cred export -f creds/credsExport.csv
    successfully exported to creds/credsExport.csv

Format is the same as for ``cred import``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
encrypt : encrypt stored credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    You have to set environmental variable as a encryption/decryption master key. 
    Otherwise you will be prompted during operation to provide one.
    Default is ``GC_KEY``, use ``export GC_KEY=YourPass`` before starting GlobalConsole.
    
Example:

.. code-block:: bash

    gc> cred encrypt -Y
    secret key successfully entered using GC_KEY env variable
    ALL NOT ENCRYPTED PASSWORDS WILL BE AFFECTED, CONTINUE? [Y/n]
    answer: Y

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
decrypt : decrypt stored credentials   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> cred decrypt -Y
    ALL ENCRYPTED PASSWORDS WILL BE VISIBLE AS PLAIN TEXT, CONTINUE? [Y/n]
    answer: Y

----------------
Hosts
----------------
 
.. code-block:: bash

    gc> host 
    usage: host <command> [<args>]
    
    work with hosts
    
    positional arguments:
      {import,update,rem,purge,pick,show,export}
    
    optional arguments:
      -h, --help            show this help message and exit

you can manage your hosts with ``host`` command.     
hosts are being stored in **hosts/hosts.json** file by default.    

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import : import csv file with definitions of hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash

    gc> host import -f hosts/hosts.csv

**csv file must follow format(no headers):**

**hostname,ip/host,port,credential_name,group**

.. note::

    value of field **credential_name** should correspond to defined credentials
    

Sample file:

.. code-block:: bash

    myhost3,192.168.57.101,22,myuser,default
    myhost4,192.168.56.102,22,rootVM,default
    myhost5,192.168.56.102,2222,myuser,default
    myhost2,192.168.56.11,22,rootVM,QAL
    myhost1,192.168.56.103,22,myuser,QAA


.. note::

    ``host import`` uses ``upsert`` operation, so can be used as a global update.
    If given **hostname** doesn't exist, will be added. 
    If does exist, all parameters will be updated for this **hostname**.  
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
update : update definition of host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash

    gc> host show
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    1 │ myhost1    │ 192.168.56.103 │     22 │ QAA     │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤

    gc> host update -p port -v 33 -s myhost1

    gc> host show
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    1 │ myhost1    │ 192.168.56.103 │     33 │ QAA     │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    2 │ myhost2    │ 192.168.56.11  │     22 │ QAL     │ rootVM     │ no        │


.. note::

    use ``host show`` output headers to obtain names of parameters to change. fields ``id`` and ``indexed`` are invalid, however


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
rem : remove selected host (hostname)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> host rem -s myhost1


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
purge : purge all hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> host purge -Y
    
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pick : pick hosts 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command below prints if item is picked(can be use to connect on, or run command on it) or not. 

.. note::
    
    Use ``-c`` switch to collapse items under hosts (installations, instance and databases). It's useful using interactive mode ( ``-e`` switch ). 
    
    For long list of items use **manual** editing instead of interactive
        

Example:

.. code-block:: bash
    
    gc> host pick
    
You must use ``-e`` switch to enter interactive edit mode. use **STOP** when all changes are made.

.. code-block:: bash
    
    gc> host pick -e
    
collapse items:

.. code-block:: bash
    
    gc> host pick -e -c    
    
You must use ``-m`` switch to manually select uuids 

.. code-block:: bash
    
    gc> host pick -m faf78009-46ea-5b5b-a3d3-0578f168cdc4 ca36b1d9-4f5d-540b-a6f2-deccbf8b5b4d

collapse items:

.. code-block:: bash
    
    gc> host pick -m faf78009-46ea-5b5b-a3d3-0578f168cdc4 ca36b1d9-4f5d-540b-a6f2-deccbf8b5b4d -c

        
You must use ``-r`` switch to reset all selections

.. code-block:: bash
    
    gc> host pick -r
                
        
.. note::

    Colors describing connected/not connected can be changed in the **config.ini** file.

    Reset can select or unselect all items, this can be changed in the **config.ini** file, also.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
show : show stored hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can reverse order of sorting, and choose sorting fields.

.. code-block:: bash

    gc> host show
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    5 │ myhost1    │ 192.168.56.103 │     22 │ QAA     │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    4 │ myhost2    │ 192.168.56.11  │     22 │ QAL     │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    1 │ myhost3    │ 192.168.57.101 │     22 │ default │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    2 │ myhost4    │ 192.168.56.102 │     22 │ default │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    3 │ myhost5    │ 192.168.56.102 │   2222 │ default │ myuser     │ no        │
    ╘══════╧════════════╧════════════════╧════════╧═════════╧════════════╧═══════════╛
    gc> host show -r
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    3 │ myhost5    │ 192.168.56.102 │   2222 │ default │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    2 │ myhost4    │ 192.168.56.102 │     22 │ default │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    1 │ myhost3    │ 192.168.57.101 │     22 │ default │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    4 │ myhost2    │ 192.168.56.11  │     22 │ QAL     │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    5 │ myhost1    │ 192.168.56.103 │     22 │ QAA     │ myuser     │ no        │
    ╘══════╧════════════╧════════════════╧════════╧═════════╧════════════╧═══════════╛
    gc> host show -r -f def_cred port
    ╒══════╤════════════╤════════════════╤════════╤═════════╤════════════╤═══════════╕
    │   id │ hostname   │ host           │   port │ group   │ def_cred   │ indexed   │
    ╞══════╪════════════╪════════════════╪════════╪═════════╪════════════╪═══════════╡
    │    2 │ myhost4    │ 192.168.56.102 │     22 │ default │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    4 │ myhost2    │ 192.168.56.11  │     22 │ QAL     │ rootVM     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    3 │ myhost5    │ 192.168.56.102 │   2222 │ default │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    1 │ myhost3    │ 192.168.57.101 │     22 │ default │ myuser     │ no        │
    ├──────┼────────────┼────────────────┼────────┼─────────┼────────────┼───────────┤
    │    5 │ myhost1    │ 192.168.56.103 │     22 │ QAA     │ myuser     │ no        │
    ╘══════╧════════════╧════════════════╧════════╧═════════╧════════════╧═══════════╛

.. note::

    use ``host show`` output headers to obtain names of parameters to sort on. 
    
    if no sorting fields, **hostname** is default
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
export : export definitions of hosts to csv file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> host export -f hosts/hostsExport.csv
    successfully exported to hosts/hostsExport.csv

Format is the same as for ``host import``.

----------------
Connections
----------------


.. code-block:: bash

    gc> conn
    usage: conn <command> [<args>]
    
    work with connections
    
    positional arguments:
      {connect,close,show}
    
    optional arguments:
      -h, --help            show this help message and exit


you can manage your connections with ``conn`` command.

Connection will be being kept alive by sending a package over a number of seconds. You can change default value in **config.ini** file, parameter ``keep_alive_interval``.     


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
connect : connect to selected hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> conn connect -Y
    successfully connected to: 192.168.56.102 using password
    successfully connected to: 192.168.57.101 using password
    myhost1 (192.168.57.101:22) says: localhost.localdomain 
    myhost2 (192.168.56.102:22) says: localhost.localdomain 
    active connections: 2 


.. note::

    use ``host pick -e`` or ``host pick -m`` to select hosts
    

**You can omit** ``host pick`` **and select list of hosts directly:**

Example:

.. code-block:: bash
    
    gc> conn connect -Y myhost1 myhost2
    successfully connected to: 192.168.56.102 using password
    successfully connected to: 192.168.57.101 using password
    myhost1 (192.168.57.101:22) says: localhost.localdomain 
    myhost2 (192.168.56.102:22) says: localhost.localdomain 



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
close : close active connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> conn close -Y
    removed connection to: myhost1 (192.168.57.101:22)
    removed connection to: myhost2 (192.168.56.102:22)
    active connections: 0


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
show : show active connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: bash
    
    gc> conn show 
    group: VM  [no connected]
        --host: myhost1  [connected, ip: 192.168.57.101, port: 22]
        --host: myhost2  [connected, ip: 192.168.56.102, port: 22]
    active connections: 2 


-----------------
Variables
-----------------

.. code-block:: bash

    gc> var
    usage: var <command> [<args>]
    
    work with variables
    
    positional arguments:
      {show,edit,rem,purge}
    
    optional arguments:
      -h, --help            show this help message and exit



you can work with custom variables with ``var`` command. 

variables created as *persistent* are stored on a disc, while *session* variables are stored only in memory.  

They can speed up productivity, look at examples in the **Running commands** section below.    

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
show : show all defined variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can reverse order of sorting. Rows are sorted on *name*.

.. code-block:: bash

    gc> var show
    ╒════════╤═════════════════╤════════╕
    │ name   │ value           │ keep   │
    ╞════════╪═════════════════╪════════╡
    │ dirs   │ /opt,/tmp       │ y      │
    ├────────┼─────────────────┼────────┤
    │ files  │ myfile1,myfile2 │ y      │
    ├────────┼─────────────────┼────────┤
    │ table  │ users_tab       │ n      │
    ╘════════╧═════════════════╧════════╛
    gc> var show -r
    ╒════════╤═════════════════╤════════╕
    │ name   │ value           │ keep   │
    ╞════════╪═════════════════╪════════╡
    │ table  │ users_tab       │ n      │
    ├────────┼─────────────────┼────────┤
    │ files  │ myfile1,myfile2 │ y      │
    ├────────┼─────────────────┼────────┤
    │ dirs   │ /opt,/tmp       │ y      │
    ╘════════╧═════════════════╧════════╛



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
edit : add/edit selected variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If given **varname** doesn't exist, will be added. 
If does exist, value will be updated for this **varname**.  

.. code-block:: bash

    gc> var show
    ╒════════╤═══════════╤════════╕
    │ name   │ value     │ keep   │
    ╞════════╪═══════════╪════════╡
    │ dirs   │ /opt,/tmp │ y      │
    ╘════════╧═══════════╧════════╛
    gc> var edit -V table -v users_tab 
    added session variable: table 
    gc> var edit -V files -v myfile1,myfile2 -p
    added persistent variable: files 
    gc> var show 
    ╒════════╤═════════════════╤════════╕
    │ name   │ value           │ keep   │
    ╞════════╪═════════════════╪════════╡
    │ dirs   │ /opt,/tmp       │ y      │
    ├────────┼─────────────────┼────────┤
    │ files  │ myfile1,myfile2 │ y      │
    ├────────┼─────────────────┼────────┤
    │ table  │ users_tab       │ n      │
    ╘════════╧═════════════════╧════════╛



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
rem : remove variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> var show 
    ╒════════╤═════════════════╤════════╕
    │ name   │ value           │ keep   │
    ╞════════╪═════════════════╪════════╡
    │ dirs   │ /opt,/tmp       │ y      │
    ├────────┼─────────────────┼────────┤
    │ files  │ myfile1,myfile2 │ y      │
    ├────────┼─────────────────┼────────┤
    │ table  │ users_tab       │ n      │
    ╘════════╧═════════════════╧════════╛
    active connections: 0 
    gc> var rem -V files
    active connections: 0 
    gc> var rem -V table
    active connections: 0 
    gc> var show 
    ╒════════╤═══════════╤════════╕
    │ name   │ value     │ keep   │
    ╞════════╪═══════════╪════════╡
    │ dirs   │ /opt,/tmp │ y      │
    ╘════════╧═══════════╧════════╛




^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 purge : purge all variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    
    gc> var purge -Y


-----------------
Running commands
-----------------


.. code-block:: bash

    gc> run
    usage: run <command> [<args>]
    
    run commands
    
    positional arguments:
      {os,scp,db2,scan}
    
    optional arguments:
      -h, --help         show this help message and exit





you can run commands on connected hosts using **ssh** with ``run`` command.     

You can use **variables** and put results into **excel** or **csv** file. 
Take a look on examples of below.


.. note::

    to access help of internal ``run`` commands **os** and **db2**, you must use ``+h`` instead of ``-h``, check:
    ``run os +h``
    ``run db2 +h``

.. note::

    - variable name must be placed into {{}} construct
    
    - variables can be used with ``os``, ``db2`` and ``scp`` commands
    
    - you must specify ``spool`` parameter with valid filename mask (*.csv or *.xlsx) to generate file
    
    - generated files are being stored into **spool** directory
     
    - default one row per one output behaviour in xlsx files can be changed in **config.ini** file, parameter ``spoolxlsxline``. setting to YES will cause to generate one row for every output's line.
    
    - output will be printed as soon as it arrives. You can change this in **config.ini** file, parameter ``wait_for_all_hosts``, so result of a command will be printed when all servers will deliver
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
os : run OS commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

run as a connected user

.. code-block:: bash

    gc> run os ls -la /tmp | grep yum
    --------myhost1 (192.168.57.101:22)--------
    
    -rw-------.  1 root     root     496566 Jul 30 08:45 yum_save_tx.2018-07-30.08-45.pVxN92.yumtx
    -rw-------.  1 root     root     496566 Jul 31 06:25 yum_save_tx.2018-07-31.06-25.akMKeb.yumtx
    
    --------myhost2 (192.168.56.102:22)--------
    
    -rw-------.  1 root     root     496566 Aug  2 09:07 yum_save_tx.2018-08-02.09-07.9otbkt.yumtx
    -rw-------.  1 root     root     496566 Aug  3 06:02 yum_save_tx.2018-08-03.06-02.PbcDpc.yumtx
    -rw-------.  1 root     root     496566 Aug  6 08:01 yum_save_tx.2018-08-06.08-01.9JX9a_.yumtx

run as a root user (using sudo)

.. code-block:: bash

    gc> run os wc -l /etc/shadow +SU 
    --------myhost1 (192.168.57.101:22)--------
    
    48 /etc/shadow
    
    --------myhost2 (192.168.56.102:22)--------
    
    23 /etc/shadow

run as a db2inst1 user (using sudo), using ksh shell

.. code-block:: bash

    gc> run os ls /db2/home/db2inst1 | wc -l  +SU db2inst1 +SH /bin/ksh 
    --------myhost2 (192.168.56.102:22)--------
    
    4
    
    --------myhost1 (192.168.57.101:22)--------
    
    3


run as a connected user, put output to an excel file

.. code-block:: bash

    gc> run os df -h /opt  +spool results.xlsx
    --------myhost1 (192.168.57.101:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    --------myhost2 (192.168.56.102:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    excel file generated to: /home/user/spool/results.xlsx.. spool turned off

.. image:: img/xlsx.png
    :alt: xlsx file

.. image:: docs/img/xlsx.png


run as a connected user, put output to a csv file

.. code-block:: bash

    gc> run os du -ms /root  +spool results.csv
    --------myhost1 (192.168.57.101:22)--------
    
    407	/root
    
    --------myhost2 (192.168.56.102:22)--------
    
    378	/root
    csv file generated to: /home/user/spool/results.csv.. spool turned off

.. code-block:: bash
    
    hostname,host,instance,db,result,command
    myhost1,(192.168.57.101:22),NA,NA,407	/root,du -ms /root
    myhost2,(192.168.56.102:22),NA,NA,378	/root,du -ms /root


run as a connected user, **use variable**, put output to a csv file

.. code-block:: bash

    gc> run os du -ms {{dirs}} +spool results2.csv
    --------myhost1 (192.168.57.101:22)--------
    
    4	/tmp
    
    --------myhost2 (192.168.56.102:22)--------
    
    1110	/opt
    
    --------myhost2 (192.168.56.102:22)--------
    
    4	/tmp
    
    --------myhost1 (192.168.57.101:22)--------
    
    1110	/opt
    
    csv file generated to: /home/user/spool/results2.csv.. spool turned off

.. code-block:: bash
    
    hostname,host,instance,db,result,command
    myhost1,(192.168.57.101:22),NA,NA,4	/tmp,du -ms /tmp
    myhost2,(192.168.56.102:22),NA,NA,1110	/opt,du -ms /opt
    myhost2,(192.168.56.102:22),NA,NA,4	/tmp,du -ms /tmp
    myhost1,(192.168.57.101:22),NA,NA,1110	/opt,du -ms /opt



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
scan : scan connected hosts to get DB2 infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    ``scan`` is required to use ``db2`` command. 
    
    it scans connected servers to get DB2 infrastructure. use ``host pick`` to see newly added elements.

dry run - check output, do not save

.. code-block:: bash

    gc> run scan -Y -d

    [{'installation_checked': 'x',
      'installation_name': '/opt/ibm/db2/V10.5',
      'installation_uuid': '7d1c87c7-db3d-590b-a0a9-1cc22c18b674',
      'instances': [{'databases': [{'db_checked': 'x',
                                    'db_name': 'TEST',
                                    'db_uuid': '72210296-5358-5dd5-96c1-21a4473d2a22'},
                                   {'db_checked': 'x',
                                    'db_name': 'TEST2',
                                    'db_uuid': '4ccfe200-5ce8-5070-a904-fbc43dedf353'}],
    ...
    

scan infrastructure, store output within host definitions

.. code-block:: bash

    gc> run scan -Y
    group: VM id: 5645848e-8cd4-5ff5-87fe-2a906d660aa0
        --host: myhost1 id: 3cd7926b-dbe7-5b70-ba27-d3a386fb5fe5
            --install: /opt/ibm/db2/V10.5 id: dc388c45-a205-5c5b-a8ec-5232d3ce3eae
                --instance: db2inst1 id: 70683dff-e5a7-54f6-b7ec-12544d0dab47
                    --db: TEST id: e1936ead-44ef-508a-942a-005bedd3cf78
                    --db: TEST2
    ...


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
db2 : run DB2 specific commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

run as connected user

.. code-block:: bash

    gc> run db2 select * from sysibm.sysdummy1
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ...


run as instance owner

.. code-block:: bash

    gc> run db2 select * from sysibm.sysdummy1 +USR instance
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ...

run as connected user, os mode - db2 profile loaded, for every database

.. code-block:: bash

    gc> run db2 db2 get dbm cfg | grep buffer +OS
    
    --------myhost2 (192.168.56.102:22)--------
    
     Audit buffer size (4KB)                  (AUDIT_BUF_SZ) = 0
     No. of int. communication buffers(4KB)(FCM_NUM_BUFFERS) = AUTOMATIC(4096)
     Communication buffer exit library list (COMM_EXIT_LIST) = 
    
    --------myhost1 (192.168.57.101:22)--------
    
     Audit buffer size (4KB)                  (AUDIT_BUF_SZ) = 0
     No. of int. communication buffers(4KB)(FCM_NUM_BUFFERS) = AUTOMATIC(4096)
     Communication buffer exit library list (COMM_EXIT_LIST) = 
    ...


run as connected user, os mode - db2 profile loaded, for every instance, use instance name in a command

.. code-block:: bash

    gc> run db2 ls /db2/home/{}/myfile1.txt +OS +IN
    
    --------myhost1 (192.168.57.101:22)--------
    
    /db2/home/db2inst1/myfile1.txt
    
    --------myhost1 (192.168.57.101:22)--------
    
    /db2/home/cogpi/myfile1.txt
    
    --------myhost2 (192.168.56.102:22)--------
    
    /db2/home/db2inst1/myfile1.txt
    
    --------myhost2 (192.168.56.102:22)--------
    
    /db2/home/cogpi/myfile1.txt


run as connected user, os mode - db2 profile loaded, set env variable,  for every database

.. code-block:: bash

    gc> run db2 echo $GC +OS +ENV export GC=hello
    --------myhost2 (192.168.56.102:22)--------
    
    hello
    
    --------myhost1 (192.168.57.101:22)--------
    
    hello
    
    --------myhost1 (192.168.57.101:22)--------
    
    hello
    ...

run as connected user, os mode - db2 profile loaded, for every database, use database name in a command

.. code-block:: bash
    
    gc> run db2 db2 deactivate db  {} +OS +USR instance
    --------myhost2 (192.168.56.102:22)--------
    
    DB20000I  The DEACTIVATE DATABASE command completed successfully.
    
    --------myhost2 (192.168.56.102:22)--------
    
    DB20000I  The DEACTIVATE DATABASE command completed successfully.
    
    --------myhost2 (192.168.56.102:22)--------
    
    DB20000I  The DEACTIVATE DATABASE command completed successfully.
    ...

run as instance owner, os mode - db2 profile loaded, for every database, use database name in a command, put output to excel file

.. code-block:: bash
    
    gc> run db2 db2pd -db  {} -bufferpools +OS +USR instance +spool resultsDB.xlsx
    
    
.. image:: img/xlsxdb.png
    :alt: xlsxdb file
    
.. image:: docs/img/xlsxdb.png

run as instance owner, for every database, put output to csv file

.. code-block:: bash
    
    gc> run db2 select * from sysibm.sysdummy1 +USR instance +spool resultsDB.csv
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ...
    
.. code-block:: bash
   
    hostname,host,instance,db,result,command
    myhost2,(192.168.56.102:22),cogpi,TEST3,IBMREQD, sudo su - cogpi -c " . /db2/home/cogpi/sqllib/db2profile; db2 connect to TEST3> /dev/null; db2 select \* from sysibm.sysdummy1 ; db2 terminate > /dev/null"
    myhost2,(192.168.56.102:22),cogpi,TEST3,-------, sudo su - cogpi -c " . /db2/home/cogpi/sqllib/db2profile; db2 connect to TEST3> /dev/null; db2 select \* from sysibm.sysdummy1 ; db2 terminate > /dev/null"
    myhost2,(192.168.56.102:22),cogpi,TEST3,Y      , sudo su - cogpi -c " . /db2/home/cogpi/sqllib/db2profile; db2 connect to TEST3> /dev/null; db2 select \* from sysibm.sysdummy1 ; db2 terminate > /dev/null"
    ...
       
       
run as a connected user, **use persistent variable**

.. code-block:: bash

    gc> var edit -V table -v sysibm.sysdummy1 -p 
    gc> var show -r
    ╒════════╤══════════════════╤════════╕
    │ name   │ value            │ keep   │
    ╞════════╪══════════════════╪════════╡
    │ table  │ sysibm.sysdummy1 │ y      │
    
    gc> run db2 select * from {{table}}
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ...


run as an instance owner, **use session variable**

.. code-block:: bash

    gc> var edit -V table -v sysibm.sysdummy1
    gc> var show -r
    ╒════════╤══════════════════╤════════╕
    │ name   │ value            │ keep   │
    ╞════════╪══════════════════╪════════╡
    │ table  │ sysibm.sysdummy1 │ n      │
    ├────────┼──────────────────┼────────┤
    
    gc> run db2 select * from {{table}}
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost1 (192.168.57.101:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    ...




^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
scp : transfer files using scp 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    ``scp`` checks progress, messages like "size: 16, done: 0" show current status
    
    ``get`` will add hostname as a suffix to downloaded files to distinguish file's origin

put file to /tmp dir on connected servers 

.. code-block:: bash

    gc> run scp -m put -s upload/myfile1.txt -d /tmp 
    EXISTING FILES WILL BE OVERWRITTEN, CONTINUE? [Y/n]
    answer: Y
    scp - command mode: put, source: upload/myfile1.txt, dest: /tmp, recursive: False, host: myhost2
    scp - command mode: put, source: upload/myfile1.txt, dest: /tmp, recursive: False, host: myhost1
    object: myfile1.txt, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    object: myfile1.txt, size: 16, done: 0, server: myhost2, (192.168.56.102:22)
    object: myfile1.txt, size: 16, done: 16, server: myhost2, (192.168.56.102:22)
    object: myfile1.txt, size: 16, done: 16, server: myhost1, (192.168.57.101:22)

put directory to /tmp dir on connected servers, use recursion, don't ask for confirmation

.. code-block:: bash

    gc> run scp -m put -s upload/mydir -d /tmp -r -b
    object: file1.csv, size: 1, done: 1, server: myhost1, (192.168.57.101:22)
    object: file2.sql, size: 1, done: 1, server: myhost1, (192.168.57.101:22)
    object: file1.csv, size: 1, done: 1, server: myhost2, (192.168.56.102:22)
    object: file2.sql, size: 1, done: 1, server: myhost2, (192.168.56.102:22)

put files to /tmp dir on connected servers, **use session variable**, don't ask for confirmation

.. code-block:: bash

    gc> var edit -V files -v myfile1.txt,myfile2.txt
    added session variable: files 
    gc> var show -r
    ╒════════╤═════════════════════════╤════════╕
    │ name   │ value                   │ keep   │
    ╞════════╪═════════════════════════╪════════╡
    │ files  │ myfile1.txt,myfile2.txt │ n      │
    
    gc> run scp -m put -s upload/{{files}} -d /tmp -b
    object: myfile2.txt, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    object: myfile1.txt, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    ...
    gc> run os ls -la /tmp/myfile*
    --------myhost2 (192.168.56.102:22)--------
    
    -rw-r--r--. 1 root root 16 Aug 14 08:06 /tmp/myfile1.txt
    -rw-r--r--. 1 root root 16 Aug 14 08:06 /tmp/myfile2.txt
    
    --------myhost1 (192.168.57.101:22)--------
    
    -rw-r--r--. 1 root root 16 Aug 14 08:06 /tmp/myfile1.txt
    -rw-r--r--. 1 root root 16 Aug 14 08:06 /tmp/myfile2.txt



get file from /tmp dir on connected servers 

.. code-block:: bash

    gc> run scp -m get -s /tmp/myfile1.txt -d download/ 
    EXISTING FILES WILL BE OVERWRITTEN, CONTINUE? [Y/n]
    answer: Y
    scp - command mode: get, source: /tmp/myfile1.txt, dest: download/myfile1.txt_myhost1, recursive: False, host: myhost1
    scp - command mode: get, source: /tmp/myfile1.txt, dest: download/myfile1.txt_myhost2, recursive: False, host: myhost2
    object: download/myfile1.txt_myhost2, size: 16, done: 0, server: myhost2, (192.168.56.102:22)
    object: download/myfile1.txt_myhost1, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    object: download/myfile1.txt_myhost1, size: 16, done: 16, server: myhost1, (192.168.57.101:22)
    object: download/myfile1.txt_myhost2, size: 16, done: 16, server: myhost2, (192.168.56.102:22)
    gc> !ls -la download
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:36 myfile1.txt_myhost1
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:36 myfile1.txt_myhost2


get directory from /tmp dir on connected servers, use recursion, don't ask for confirmation

.. code-block:: bash

    gc> run scp -m get -s /tmp/mydir -d download/ -r -b
    EXISTING FILES WILL BE OVERWRITTEN, CONTINUE? [Y/n]
    scp - command mode: get, source: /tmp/mydir, dest: download/mydir_myhost1, recursive: True, host: myhost1
    scp - command mode: get, source: /tmp/mydir, dest: download/mydir_myhost2, recursive: True, host: myhost2
    object: download/mydir_myhost1/file2.sql, size: 1, done: 1, server: myhost1, (192.168.57.101:22)
    object: download/mydir_myhost1/file1.csv, size: 1, done: 1, server: myhost1, (192.168.57.101:22)
    object: download/mydir_myhost2/file2.sql, size: 1, done: 1, server: myhost2, (192.168.56.102:22)
    object: download/mydir_myhost2/file1.csv, size: 1, done: 1, server: myhost2, (192.168.56.102:22)
    gc> !ls -la download/mydir*
    download/mydir_myhost1:
    -rw-r--r--. 1 pl55227 pl55227    0 08-14 14:38 file1.csv
    -rw-r--r--. 1 pl55227 pl55227    0 08-14 14:38 file2.sql
    
    download/mydir_myhost2:
    -rw-r--r--. 1 pl55227 pl55227    0 08-14 14:38 file1.csv
    -rw-r--r--. 1 pl55227 pl55227    0 08-14 14:38 file2.sql


get files from /tmp dir on connected servers, **use persistent variable**, don't ask for confirmation

.. code-block:: bash

    gc> var edit -V files -v myfile1.txt,myfile2.txt -p
    added persistent variable: files 
    gc> var show -r
    ╒════════╤═════════════════════════╤════════╕
    │ name   │ value                   │ keep   │
    ╞════════╪═════════════════════════╪════════╡
    │ files  │ myfile1.txt,myfile2.txt │ y      │
    ├────────┼─────────────────────────┼────────┤
    gc> run scp -m get -s /tmp/{{files}} -d download/ -b
    EXISTING FILES WILL BE OVERWRITTEN, CONTINUE? [Y/n]
    scp - command mode: get, source: /tmp/myfile1.txt, dest: download/myfile1.txt_myhost1, recursive: False, host: myhost1
    scp - command mode: get, source: /tmp/myfile2.txt, dest: download/myfile2.txt_myhost1, recursive: False, host: myhost1
    scp - command mode: get, source: /tmp/myfile2.txt, dest: download/myfile2.txt_myhost2, recursive: False, host: myhost2
    scp - command mode: get, source: /tmp/myfile1.txt, dest: download/myfile1.txt_myhost2, recursive: False, host: myhost2
    object: download/myfile2.txt_myhost1, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    object: download/myfile1.txt_myhost1, size: 16, done: 0, server: myhost1, (192.168.57.101:22)
    object: download/myfile2.txt_myhost1, size: 16, done: 16, server: myhost1, (192.168.57.101:22)
    object: download/myfile2.txt_myhost2, size: 16, done: 0, server: myhost2, (192.168.56.102:22)
    object: download/myfile1.txt_myhost1, size: 16, done: 16, server: myhost1, (192.168.57.101:22)
    object: download/myfile2.txt_myhost2, size: 16, done: 16, server: myhost2, (192.168.56.102:22)
    object: download/myfile1.txt_myhost2, size: 16, done: 0, server: myhost2, (192.168.56.102:22)
    object: download/myfile1.txt_myhost2, size: 16, done: 16, server: myhost2, (192.168.56.102:22)
    gc> !ls -la download/
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:42 myfile1.txt_myhost1
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:42 myfile1.txt_myhost2
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:42 myfile2.txt_myhost1
    -rw-r--r--.  1 pl55227 pl55227   16 08-14 14:42 myfile2.txt_myhost2


-----------------
Batch & Steps
-----------------

You can create scenarios and re-run them without a need of manual typing/copying commands.

.. note::

    to create a batch file, simply put there any valid GlobalConsole command

**SCENARIO1** - basic

1. Create a file, example:

.. code-block:: bash

    conn connect -Y
    var show -r
    var edit -V table -v sysibm.sysdummy1
    var show -r
    run db2 select * from {{table}}
    conn close -Y

2. Run created batch

.. code-block:: bash

    gc> batch -f batch/db2.param
    command: conn connect -Y
    successfully connected to: 192.168.56.102 using password
    successfully connected to: 192.168.57.101 using password
    myhost1 (192.168.57.101:22) says: localhost.localdomain 
    myhost2 (192.168.56.102:22) says: localhost.localdomain 
    command: var show -r
    ╒════════╤═════════════════════════╤════════╕
    │ name   │ value                   │ keep   │
    ╞════════╪═════════════════════════╪════════╡
    │ files  │ myfile1.txt,myfile2.txt │ y      │
    ├────────┼─────────────────────────┼────────┤
    │ dirs   │ /opt,/tmp               │ y      │
    ╘════════╧═════════════════════════╧════════╛
    command: var edit -V table -v sysibm.sysdummy1
    added session variable: table 
    command: var show -r
    ╒════════╤═════════════════════════╤════════╕
    │ name   │ value                   │ keep   │
    ╞════════╪═════════════════════════╪════════╡
    │ table  │ sysibm.sysdummy1        │ n      │
    ├────────┼─────────────────────────┼────────┤
    │ files  │ myfile1.txt,myfile2.txt │ y      │
    ├────────┼─────────────────────────┼────────┤
    │ dirs   │ /opt,/tmp               │ y      │
    ╘════════╧═════════════════════════╧════════╛
    command: run db2 select * from {{table}}
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
    
    --------myhost2 (192.168.56.102:22)--------
    
    IBMREQD
    -------
    Y      
      1 record(s) selected.
      
    ....
    
    command: conn close -Y
    removed connection to: myhost1 (192.168.57.101:22)
    removed connection to: myhost2 (192.168.56.102:22)


**SCENARIO2** - advanced

When you have a long batch file, you might want abort execution if one of steps somehow fails.
You can define output checking using ``check`` command, take a look at example below.

.. note::

    use ``check set <args> -r`` to define string that should not appears in a result of command


1. Create a file, example:

.. code-block:: bash

    conn connect -Y
    #
    check set 43G  8.0G
    check show
    run os df -h /tmp
    #
    check set sda2
    check show
    run os df -h /tmp
    #
    check set /root -r
    check show
    run os pwd
    #
    run os hostname
    #
    run os whoami
    #
    conn close -Y

2. Run created batch

.. code-block:: bash

    gc> batch -f batch/my.param
    command: conn connect -Y
    successfully connected to: 192.168.56.102 using password
    successfully connected to: 192.168.57.101 using password
    myhost2 (192.168.56.102:22) says: localhost.localdomain 
    myhost1 (192.168.57.101:22) says: localhost.localdomain 
    command: check set 43G  8.0G
    command: check show
    
    --------check-------- 
    text: 
    43G 8.0G
    should be present: True
    
    command: run os df -h /tmp
    --------myhost1 (192.168.57.101:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    --------myhost2 (192.168.56.102:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    command: check set sda2
    command: check show
    
    --------check-------- 
    text: 
    sda2
    should be present: True
    
    command: run os df -h /tmp
    --------myhost1 (192.168.57.101:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    --------myhost2 (192.168.56.102:22)--------
    
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        43G  8.0G   33G  20% /
    
    command: check set /root -r
    command: check show
    
    --------check-------- 
    text: 
    /root
    should be present: False
    
    command: run os pwd
    --------myhost1 (192.168.57.101:22)--------
    
    /root
    
    --------myhost2 (192.168.56.102:22)--------
    
    /root
    
    --!--check failed on line:13, command: run os pwd


.. note::

    look at the last line - execution is terminated. 
    Line number and command causing problems is provided.  


-----------------
Shell
-----------------

You can access local shell with ``shell`` command or using ``!`` sign.

.. code-block:: bash

    gc> shell ls -la creds | wc -l
    8
    gc> ! ls -la creds | wc -l
    8
    gc> !vim tst



-----------------
History
-----------------

.. code-block:: bash

    gc> history
    usage: history <command> [<args>]
    
    work with commands history
    
    positional arguments:
      {clear,show,run,find}
    
    optional arguments:
      -h, --help        show this help message and exit


you can work with commands history with ``history`` command.     

history is **persistent**. you can configure how many recent commands should be kept in **config.ini** file.

.. note::

    ``ctrl + r`` combination can be used to reverse-search a history   


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
clear : clear saved history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> history clear -Y
    

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
show : show history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> history show
    1 cred show -e
    2 cred purge
    ..
    99 var edit -V dirs -v /root,/home
    100 exit
    101 shell pwd

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
run : re-run command from history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> history show
    1 cred show -e
    ..
    89 var show
    gc> history run -c 89
    ╒════════╤═════════════════╤════════╕
    │ name   │ value           │ keep   │
    ╞════════╪═════════════════╪════════╡
    │ dirs   │ /opt,/tmp       │ y      │
    ├────────┼─────────────────┼────────┤
    │ files  │ myfile1,myfile2 │ y      │
    ╘════════╧═════════════════╧════════╛

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
find : find command in history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    gc> history find -c conn
    1 conn show
    3 conn show
    8 conn connect -Y
    9 conn show
    13 conn close -Y
    ..

-----------------
Logging
-----------------

Look into *logs* directory to find **global_console.log** file.

Log file format is:

**date - module name - level - message**

.. code-block:: bash

    2018-08-13 11:45:41,370 - GlobalConsole.command - INFO - successfully connected to: 192.168.57.101 using password
    2018-08-13 11:45:47,124 - GlobalConsole.command - ERROR - cannot update host with scanned dat

*Logs* directory contains **gc_history** file, also. The file tracks commands' history and make this persistent.

-----------------
Config
-----------------

Look into *config* directory to find **config.ini** file. 
All configurable options can be found down there. Every item has self-explanatory description.

-----------------
Architecture 
-----------------

Looking at *Module Index* you should start with ``GcConsole`` as it's an entry point for GlobalConsole.
It's based on ``cmd`` module and it decorates all invocations with prompt. ``argparse`` is used to provide git-like experience.
Drilling down ``GcConsole`` imports from ``globalconsole`` package one can connect all dots.

-----------------
Q&A 
-----------------

- why docker is a default ?

Easy deployment and more secure - history of environmental variables, used to encrypt/decrypt passwords, is being destroyed with container.

- can I get standalone version?

Standalone is possible in future but it's not a highest priority, currently.

- what about connecting to Windows?

I would say - highly possible in next major version. I think about using ``pywinrm``

-----------------------
Help & Commands params
-----------------------

To get help you can use:
 
- this documentation

- command's own help

.. note::

    use ``help`` to see all available commands. every command has help at every level, check:
    
    gc> help
    
    gc> cred -h
    
    gc> cred update -h
    
.. note:: 
   
    use ``tab`` as autocompletion, check
    
    gc> help
    
    gc> cr<tab>
    
    gc> cred u<tab>    
        

- module's description

To print version of GlobalConsole:

.. code-block:: bash

    gc> version
    2.0.0_La_Cucaracha

    
-----------------------
Sample sessions
-----------------------

installations using venv:

.. image:: img/installVenv.gif
    :alt: installVenv file

.. image:: docs/img/installVenv.gif


installations using docker:

.. image:: img/installDocker.gif
    :alt: installDocker file

.. image:: docs/img/installDocker.gif

sample session:

.. image:: img/session.gif
    :alt: session file

.. image:: docs/img/session.gif


batch file:

.. image:: img/batch.gif
    :alt: batch file

.. image:: docs/img/batch.gif


file used:

.. code-block:: bash

    conn connect -Y
    #
    var edit -V table -v sysibm.sysdummy1
    var show -r
    run db2 select * from {{table}}
    #
    #condition: "/root" phrase should be a part of the result 
    check set /root
    check show
    run os pwd
    #this will fail
    #condition: "/root" phrase should not be a part of the result 
    check set /root -r
    check show
    run os pwd
    #
    run os whoami
    #
    conn close -Y

-----------------------
Troubleshooting
-----------------------

If you get error:

.. code-block:: bash

    Secsh channel X open FAILED: open failed: Administratively prohibited

set in **config.ini** file parameter ``max_threads`` to lower value.

If you set it to **1** everything should work, however it disables multithreading.

Root cause for this error is ``MaxSessions`` setting of sshd daemon on a destination server. 

.. note:: 
   
    this error should only occurs when working with db2, reason is openning parallel sessions to one server.


-----------------------
Contact
-----------------------

Don't hesitate to contact me:  
grzegorz.cylny [at] gmail.com