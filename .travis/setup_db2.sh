#!/bin/bash

sudo su -c "mkdir -p /usr/local/bin"

sudo su - -c "cat > /usr/local/bin/db2ls <<EOF
echo ''
echo 'Install Path                       Level   Fix Pack   Special Install Number   Install Date                  Installer UID'
echo '---------------------------------------------------------------------------------------------------------------------'
echo '/opt/ibm/db2/V10.10               10.1.1.1        1                      1    Wed Nov 22 19:13:09 2001 UTC             0'
EOF"

sudo su - -c "chmod +x /usr/local/bin/db2ls"

sudo su - -c "mkdir -p /opt/ibm/db2/V10.10/bin/"

sudo su - -c "cat > /opt/ibm/db2/V10.10/bin/db2ilist <<EOF
echo 'testinstance'
EOF"

sudo su - -c "chmod +x /opt/ibm/db2/V10.10/bin/db2ilist"

sudo su - -c "adduser testinstance --disabled-password --gecos ''"

sudo su - -c "mkdir -p /home/testinstance/sqllib/"

sudo su - -c "touch /home/testinstance/sqllib/db2profile"

sudo su - -c "chmod +x /home/testinstance/sqllib/db2profile"

sudo su - -c "cat > /bin/db2 <<EOF
echo ''
echo ' System Database Directory'
echo ''
echo ' Number of entries in the directory = 1'
echo ''
echo 'Database 1 entry:'
echo ''
echo ' Database alias                       = TESTDB'
echo ' Database name                        = TESTDB'
echo ' Local database directory             = /opt/databases'
echo ' Database release level               = 1.1'
echo ' Comment                              ='
echo ' Directory entry type                 = Indirect'
echo ' Catalog database partition number    = 0'
echo ' Alternate server hostname            ='
echo ' Alternate server port number         ='
echo ''
EOF"

sudo su - -c "chmod +x /bin/db2"

sudo su - -c "cat > /bin/db2select <<EOF
echo ''
echo 'IBMREQD'
echo '-------'
echo 'Y      '
echo ''
echo '  1 record(s) selected.'
echo ''
echo ''
EOF"

sudo su - -c "chmod +x /bin/db2select"

