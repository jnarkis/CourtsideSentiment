#!/bin/bash

# Set up a c5d.2xlarge spot instance on EC2 for file conversion. Assumes launch specification is in a file
# called 'specifications.json' that includes information like security group, subnet, etc and that AWS
# credentials are stored in an environment file called 'environment'.

# The spot instance is requested with a private IP address of 10.0.0.5.

#Request spot instance, but don't pay too much... c5d.2xlarge price hovers around $0.13/hr 
aws ec2 request-spot-instances --spot-price "0.15" --type "one-time" --launch-specification "file://$ENVDIR/spot_specification.json"

# Establish SSH, give spot instance 3 mins to start up and do status checks
echo 'Waiting 3m for instance to start and initialize...'
sleep 3m
echo 'Attempting ssh...'
ssh-keygen -f "/home/ubuntu/.ssh/known_hosts" -R 10.0.0.5
ssh -oStrictHostKeyChecking=no ubuntu@10.0.0.5 "echo 'SSH configured on spot instance...'"

# Copy environment variables
scp $ENVDIR/environment ubuntu@10.0.0.5:/home/ubuntu

#Install relevant packages
ssh ubuntu@10.0.0.5 'bash -s' < install_converter.sh

# Modify spark config file to use python3, increase memory utilization, and reduce verbosity of spark job output
ssh ubuntu@10.0.0.5 "cp /usr/local/spark/conf/spark-env.sh.template /usr/local/spark/conf/spark-env.sh;  echo 'PYSPARK_PYTHON=python3' >> /usr/local/spark/conf/spark-env.sh"
ssh ubuntu@10.0.0.5 "cp /usr/local/spark/conf/spark-defaults.conf.template /usr/local/spark/conf/spark-defaults.conf; echo 'spark.driver.memory 2g' >> /usr/local/spark/conf/spark-defaults.conf"
ssh ubuntu@10.0.0.5 "cp /usr/local/spark/conf/log4j.properties.template /usr/local/spark/conf/log4j.properties; sed -i 's/rootCategory=INFO/rootCategory=WARN/' /usr/local/spark/conf/log4j.properties"

# Pass AWS credentials for S3 access
ssh ubuntu@10.0.0.5 'bash -s' < aws_config.sh

# Set up storage drive
ssh ubuntu@10.0.0.5 'sudo mkdir /home/ubuntu/bigdrive'
ssh ubuntu@10.0.0.5 'sudo mkfs /dev/nvme0n1'
ssh ubuntu@10.0.0.5 'sudo mount /dev/nvme0n1 /home/ubuntu/bigdrive'
ssh ubuntu@10.0.0.5 'sudo chown ubuntu /home/ubuntu/bigdrive'

# Copy python scripts needed for file conversion
scp convert_to_parquet.py ubuntu@10.0.0.5:/home/ubuntu
scp ../lib/loadschema.py ubuntu@10.0.0.5:/home/ubuntu

echo 'Spot instance has been configured at 10.0.0.5.'
