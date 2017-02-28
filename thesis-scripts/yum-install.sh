#!/bin/bash
#update before doing anything!
yum -y update;

# Docker
yum install -y yum-utils;
yum-config-manager \
    --add-repo \
    https://docs.docker.com/engine/installation/linux/repo_files/centos/docker.repo;
yum makecache fast;
systemctl start docker;

# Linux containers
yum install epel-release -y;
yum install debootstrap perl libvirt -y;
yum install lxc lxc-templates -y;


# Cassandra
yum install java -y;
echo -e "[datastax]\nname = DataStax Repo for Apache Cassandra\nbaseurl = http://rpm.datastax.com/community\nenabled = 1\ngpgcheck = 0" > /etc/yum.repos.d/datastax.repo;
yum install dsc30 -y;
yum install cassandra30-tools -y;


# Use systemctl to start, stop and monitor status of :
# docker,
# lxc.service and
# libvirtd

# use service to start and stop cassandra.
