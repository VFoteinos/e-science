#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reproduces the experiment that is stored in a yaml file
"""

import os, sys
import yaml

def main(argv):

    # load the experiment
    with open(argv[1], 'r') as f:
        doc = yaml.load(f)

    # Create the cluster
    create_cluster_command = ("orka create" + " " + doc["cluster"]["name"] + " " 
    + str(doc["cluster"]["cluster_size"]) + " " + str(doc["cluster"]["cpu_master"]) + " " 
    + str(doc["cluster"]["ram_master"]) + " " + str(doc["cluster"]["disk_master"]) + " " 
    + str(doc["cluster"]["cpu_slave"]) + " " + str(doc["cluster"]["ram_slave"]) + " "  
    + str(doc["cluster"]["disk_slave"]) + " " + doc["cluster"]["disk_template"] + " " 
    + doc["cluster"]["project_name"] + " --image=" + doc["cluster"]["image"] 
    + " --replication_factor=" + str(doc["cluster"]["replication_factor"])
    + " --dfs_blocksize=" + str(doc["cluster"]["dfs_blocksize"]))
     
    exit_status = os.system(create_cluster_command)
    if exit_status != 0:
        msg = 'Cluster (re-)creation failed with exit status %d' % exit_status
        raise RuntimeError(msg, exit_status)

    # Run actions
    
if __name__ == "__main__":
    main(sys.argv)