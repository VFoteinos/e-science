Orka
=====


Overview
--------

orka is an interactive command-line tool, and also a
client development library for creating and deleting Hadoop-Yarn clusters of virtual machines
in ~okeanos.

Setup user environment to run orka
--------------------------------
    sudo apt-get update
    sudo apt-get install -y git
    sudo apt-get install -y python python-dev python-pip

Important info    
--------------
    
User should open ~/.kamakirc and add these two lines :
    
[orka]                                                              
base_url = **< e-science -IP- or -url address- >**

Virtual environment
-------


Optional but highly recommended is to install and use the orka package in a virtual environment:
 
    sudo pip install virtualenv
    mkdir .virtualenvs
    cd .virtualenvs
    virtualenv --system-site-packages orkaenv
    . ../.virtualenvs/orkaenv/bin/activate
    (with deactivate from command line you exit the virtual env)
    
Following commands are common for installation in virtual environment or not:

    [sudo if not using virtualenv] pip install ansible==1.7.2
    cd
    git clone <escience git repo> <project_name> 
    cd to <project_name>/orka
    [sudo if not using virtualenv] python setup.py install
 
  Now orka commands are usable from anywhere .







How to run orka commands
------------------------
orka [command] "arguments"

"create" command
-----------

Required positional arguments for create command:
         
    name="name of the cluster" 
    cluster_size="total VMs, including master node" 
    cpu_master="master node: number of CPU cores" 
    ram_master="master node: memory in MB",
    disk_master="master node: hard drive in GB",
    cpu_slave="each slave node: number of CPU cores",
    ram_slave="each slave node: memory in MB",
    disk_slave="each slave node: hard drive in GB",
    disk_template= "Standard or Archipelago"
    token="an ~okeanos token",
    project_name="name of a ~okeanos project, to pull resources from"
    
Optional arguments for create command:

    --image="Operating System (Default Value=Debian Base)",
    --auth_url="authentication url (Default Value=https://accounts.okeanos.grnet.gr/identity/v2.0)",
    --use_hadoop_image="name of a hadoop image. Overrides image value (Default value=HadoopImage)"

Install from a pre-configured image
----------------------------------

Using the --use_hadoop_image argument creates the Hadoop cluster much faster because it utilises a specially
created ~okeanos VM image with Java and YARN pre-installed. Omitting this argument ensures that the latest
stable YARN version will be installed (but at the cost of lower speed).

Command {orka create} examples
---------------------------

example for create cluster with default optionals (not hadoop_image):

    orka create Yarn_Test 2 2 2048 10 2 1024 10 Archipelago <~okeanos_token> <project_name>

example for create cluster with default optionals (with default hadoop image):

    orka create Yarn_Test 2 2 2048 10 2 1024 10 Archipelago <~okeanos_token> <project_name> --use_hadoop_image

example for create cluster with a different hadoop image and logging level:

    orka create Yarn_Test 2 2 2048 10 2 1024 10 Archipelago <~okeanos_token> <project_name> --use_hadoop_image=hadoop_image_name

"list" command
----------------

Required positional arguments for list command :

    token="an ~okeanos token"

Optional arguments for list command:

    --status="3 cluster status:ACTIVE, PENDING, DESTROYED (case insensitive,shows only clusters of that status)"
    --verbose (outputs full cluster details. Default off)
    
Command {orka list} example
---------------------------    

example for list user clusters:

    orka list <~okeanos_token> --status=active --verbose
    

"destroy" command
----------------

Required positional arguments for destroy command :

    cluster_id="Cluster id in e-science database" 
    token="an ~okeanos token"
(cluster_id is given by **orka list** command)


Command {orka destroy} example
---------------------------

example for destroy cluster:

    orka destroy <cluster_id> <~okeanos_token>

Also, with

    orka -h
    orka create -h
    orka destroy -h
    orka list -h

helpful information about the orka CLI is depicted and

    orka -V
    orka --version
    
prints current version.

Miscellaneous info
----------------

- The public ip of the orka web server in ~okeanos must be in ~/.kamakirc. It is required for the orka CLI.
