#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reproduces the experiment that is stored in a yaml file
"""

import os, sys
import yaml

def create_cluster(script):

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

    print create_cluster_command
#    exit_status = os.system(create_cluster_command)
#    if exit_status != 0:
#        print 'Cluster (re-)creation failed with exit status %d' % exit_status
#        sys.exit(0)

    # retrieve cluster id
    with open('_tmp.txt', 'r') as f:
        cluster_id = f.readline().strip().split(': ')[1]    

    return cluster_id


def enforce_actions(script, cluster_id):

    # Enforce actions
    for action in script["actions"]:
        if action == "start":
            print ("orka hadoop start " + str(cluster_id))
            #os.system("orka hadoop start " + str(cluster_id))
        if action == "stop":
            print ("orka hadoop stop " + str(cluster_id))
            #os.system("orka hadoop stop " + str(cluster_id))
        if action == "format":
            print ("orka hadoop format " + str(cluster_id))
            #os.system("orka hadoop format " + str(cluster_id))
        if action == "run_job":
            run_job(script, cluster_id)
        if action.startswith("put"):
            params_string = action.strip('put')
            params = params_string.strip(' ()')
            action_params = params.split(',')
            print ("orka file put " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
            #os.system("orka file put " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
        if action.startswith("get"):
            params_string = action.strip('get')
            params = params_string.strip(' ()')
            action_params = params.split(',')
            print ("orka file get " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])
            #os.system("orka file get " + str(cluster_id) + " " + action_params[0] + " " + action_params[1])

def run_job(script, cluster_id):
    print "run job"
    



def main(argv):

    # load the experiment
    with open(argv[1], 'r') as f:
        script = yaml.load(f)

    # check if cluster info is given (this is mandatory)
    if script.get("cluster") is None:
        print "Cluster information is missing."
        return
    
    # check if the cluster will be created (no cluster id is given)
    # find the correct cluster id to be used later for actions
    if script["cluster"].get("cluster_id") is None:
        cluster_id = create_cluster(script)
    else:
        cluster_id = script["cluster"].get("cluster_id")

    # proceed to the list of actions
    if script.get("actions") is not None:
        enforce_actions(script, cluster_id)


if __name__ == "__main__":
    main(sys.argv)