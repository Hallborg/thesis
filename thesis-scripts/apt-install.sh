apt-get update;
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common;

# set up repositories

# Java 8

echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee /etc/apt/sources.list.d/webupd8team-java.list;
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list;
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886;

# Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -;
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable";

# Cassandra
echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list;
curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -;

sudo apt-get update;
apt-get install oracle-java8-installer;
apt-get install cassandra;

apt-get install docker-ce;

apt install lxc debootstrap bridge-utils;
