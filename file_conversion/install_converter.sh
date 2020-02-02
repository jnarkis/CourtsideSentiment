#!/bin/bash

# Install relevant packages
sudo apt-get update
sudo apt-get install awscli -y
# If installation didn't work, try again
command -v aws > /dev/null 2>&1 || { echo 'aws did not install correctly, trying apt-get update again.'; sudo apt-get update; }
# If it didn't work this time, something failed. Check EC2 console
command -v aws > /dev/null 2>&1 || { echo 'aws did not install correctly again, check instance status.'; exit 1; }

sudo apt-get install openjdk-8-jre-headless -y
sudo apt-get install python -y #python3 is installed by default, install python 2 just in case
sudo apt-get install python3-pip -y
sudo apt-get install pbzip2
sudo apt-get install zstd

#Download and install spark
curl "http://mirrors.ibiblio.org/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz" -o spark-2.4.4-bin-hadoop2.7.tgz
echo 'Spark downloaded.'
tar xf spark-2.4.4-bin-hadoop2.7.tgz
if [ -d /usr/local/spark ]
then
  sudo rm -r /usr/local/spark
fi
sudo mv spark-2.4.4-bin-hadoop2.7 /usr/local/spark
