----------------
GlobalConsole
----------------

[![Build Status](https://travis-ci.com/grzegorzcode/GlobalConsole.svg?branch=v3.0_beta)](https://travis-ci.com/grzegorzcode/GlobalConsole) 

GlobalConsole is a tool designed to run commands on many Linux/Unix machines at the same time.
What distinguishes GlobalConsole from similar software is ability to handle DB2 database environments.
You can:

- run os commands
- run db2 specific commands
- use scp over connected servers 

It's worth to mention, also:

- **multithreaded** by design
- stored passwords can be encrypted
- output of command can be saved within **excel** or **csv** file
- hosts can be picked up using visual editor
- local shell commands are supported
- history of invoked commands is persistent over sessions
- custom variables can be set to improve productivity
- batch mode with checking output's results is available
- docker scripts to build and run GlobalConsole are provided


----------------
Documentation
----------------

Please take a look into ``docs`` directory. You will find everything you need. 
Online version:

[https://grzegorzcode.github.io/GlobalConsole](https://grzegorzcode.github.io/GlobalConsole) 

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

- rootVM : name of a credential. **it has to be a valid credential's name**, please take a look on step 1 for more details

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
                --instance: db2inst3 id: 65c3a425-c564-5ae8-a70e-dc58d6117576
                    --db: TEST4 id: b4f128ba-4efc-58d7-99a2-41aee7e9a457
        --host: myhost2 id: e411ae67-8526-5d18-b05a-b5e57b486a6a
            --install: /opt/ibm/db2/V10.5 id: 7d1c87c7-db3d-590b-a0a9-1cc22c18b674
                --instance: db2inst1 id: d2f3792d-b148-5127-b7af-1c95d0fa1489
                    --db: TEST id: 72210296-5358-5dd5-96c1-21a4473d2a22
                    --db: TEST2 id: 4ccfe200-5ce8-5070-a904-fbc43dedf353
                --instance: db2inst2 id: 77e31b62-e1a4-5d82-a67e-bd6195661291
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



