#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reproduces the experiment that is stored in a yaml file
"""

import os, sys
import yaml
import subprocess
FNULL = open(os.devnull, 'w')

def create_cluster(script):

    # create the appropriate command based on the given info
    create_cluster_command = ("orka create")
    
    if script["cluster"].get("name") is not None:
        create_cluster_command += (" " + script["cluster"]["name"])

    if script["cluster"].get("cluster_size") is not None:
        create_cluster_command += (" " + str(script["cluster"]["cluster_size"]))  

    if script["cluster"].get("flavor_master") is not None:
        master_flavor_string = script["cluster"].get("flavor_master").strip('()')
        master_flavors = master_flavor_string.split(',')
        create_cluster_command += (" " + master_flavors[0])
        create_cluster_command += (" " + master_flavors[1])
        create_cluster_command += (" " + master_flavors[2])

    if script["cluster"].get("flavor_slave") is not None:
        slave_flavor_string = script["cluster"].get("flavor_slave").strip('()')
        slave_flavors = slave_flavor_string.split(',')
        create_cluster_command += (" " + slave_flavors[0])
        create_cluster_command += (" " + slave_flavors[1])
        create_cluster_command += (" " + slave_flavors[2])

    if script["cluster"].get("disk_template") is not None:
        create_cluster_command += (" " + script["cluster"]["disk_template"])

    if script["cluster"].get("project_name") is not None:
        create_cluster_command += (" " + script["cluster"]["project_name"])        

    if script["cluster"].get("image") is not None:
        create_cluster_command += (" --image=" + script["cluster"]["image"])

    if script.get("configuration") is not None:
        if script["configuration"].get("replication_factor") is not None:
            create_cluster_command += (" --replication_factor=" 
                                   + str(script["configuration"]["replication_factor"]))
        if script["configuration"].get("dfs_blocksize") is not None:
            create_cluster_command += (" --dfs_blocksize=" 
                                   + str(script["configuration"]["dfs_blocksize"]))

    # temp file to store cluster details
    create_cluster_command += (" >_tmp.txt")
 
    # create cluster
    print create_cluster_command
    exit_status = os.system(create_cluster_command)
    if exit_status != 0:
        print 'Cluster (re-)creation failed with exit status %d' % exit_status
        sys.exit(0)

    # retrieve cluster id and master IP
    with open('_tmp.txt', 'r') as f:
        cluster_id = f.readline().strip().split(': ')[1]    
        master_IP = f.readline().strip().split(': ')[1]
        root_pass = f.readline().strip().split(': ')[1]

    # copy ssh keys to master
    copy_ssh_keys(master_IP, root_pass)
    
    return cluster_id, master_IP


def copy_ssh_keys(master_IP, root_pass):

    response = subprocess.call( "ssh-keygen -R " + master_IP, stderr=FNULL, shell=True)
    response = subprocess.call( "ssh-keyscan -H " + master_IP + " ~/.ssh/known_hosts", stderr=FNULL, shell=True)

    print ("cat ~/.ssh/id_rsa.pub | sshpass -p " + root_pass 
                                + " ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@" + 
                                master_IP + " \'" + "cat >> ~/.ssh/authorized_keys" + "\'")
    response = subprocess.call( "cat ~/.ssh/id_rsa.pub | sshpass -p " + root_pass 
                                + " ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@" + 
                                master_IP + " \'" + "cat >> ~/.ssh/authorized_keys" + "\'"
                                , stderr=FNULL, shell=True)

    print ("sshpass -p " + root_pass + " ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " 
                                + "root@" + master_IP + " \'" + "cp ~/.ssh/authorized_keys /home/hduser/.ssh/authorized_keys" + "\'")
    response = subprocess.call( "sshpass -p " + root_pass + " ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " 
                                + "root@" + master_IP + " \'" + "cp ~/.ssh/authorized_keys /home/hduser/.ssh/authorized_keys" + "\'"
                                , stderr=FNULL, shell=True)


def enforce_actions(script, cluster_id, master_IP):

    # Enforce actions
    for action in script["actions"]:
        if action in ["start", "stop", "format"]:
            print ("orka hadoop " + action + " " + str(cluster_id))
            os.system("orka hadoop " + action + " " + str(cluster_id))
        if action.startswith("put"):
            params_string = action.strip('put')
            params = params_string.strip(' ()')
            action_params = params.split(',')
            print ("orka file put " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
            os.system("orka file put " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
        if action.startswith("get"):
            params_string = action.strip('get')
            params = params_string.strip(' ()')
            action_params = params.split(',')
            print ("orka file get " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
            os.system("orka file get " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
        if action.startswith("run_job"):
            run_job(action, master_IP)
            
def run_job(action, master_IP):

    # retrieve user and job
    params_string = action.strip('run_job')
    params = params_string.strip(' ()')
    action_params = params.split(',')
    user = action_params[0]
    job = action_params[1].strip('\" ')

    # ssh and run job
    print ("ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " 
                                + user + "@" + master_IP + " \'" 
                                + job + "\'")
    response = subprocess.call( "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " 
                                + user + "@" + master_IP + " \'" 
                                + job + "\'"
                                , stderr=FNULL, shell=True)


def main(argv):

    # load the experiment
    with open(argv[1], 'r') as f:
        script = yaml.load(f)

    # check if cluster info is given (this is mandatory)
    if script.get("cluster") is None:
        print "Cluster information is missing."
        return
    
    # check if the cluster will be created (no cluster id is given)
    # find the correct cluster id / master IP to be used later for actions
    if script["cluster"].get("cluster_id") is None:
        cluster_id, master_IP = create_cluster(script)
    else:
        cluster_id = script["cluster"].get("cluster_id")
        master_IP = script["cluster"].get("master_IP")
    
    # proceed to the list of actions
    if script.get("actions") is not None:
        enforce_actions(script, cluster_id, master_IP)


if __name__ == "__main__":
    main(sys.argv)