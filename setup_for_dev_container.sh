#!/bin/bash

# Update package lists
apt-get update

# Install Python3
apt-get install python3 -y

# Install pip3
apt-get install python3-pip -y

# Add aliases to .bashrc
echo "alias python='/usr/bin/python3.$(python3 --version | awk '{print $2}' | cut -c 1-3)'" >> ~/.bashrc
echo "alias pip='/usr/bin/pip3'" >> ~/.bashrc

# Reload .bashrc
source ~/.bashrc
