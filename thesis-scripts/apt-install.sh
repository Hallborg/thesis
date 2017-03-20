apt-get update -y;
apt-get install -y \
    apt-transport-https -y \
    ca-certificates -y \
    curl -y \
    software-properties-common -y;

# set up repositories

# Java 8

echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee /etc/apt/sources.list.d/webupd8team-java.list;
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list;
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886;
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections;

# Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -;
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable";

# Cassandra
echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list;
curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -;

apt-get update -y;
apt-get install oracle-java8-installer -y;
apt-get install cassandra -y;

apt-get install docker-ce -y;

apt install lxc debootstrap bridge-utils -y;

# Second phase of installation (lxc)

echo "lxc.network.type = none" > /etc/lxc/default.conf;

service lxc reload;
lxc-create -t download -n $(hostname)-lxc -- -d debian -r jessie -a amd64;
lxc-start -n $(hostname)-lxc -d;
sleep 30;

cat lxc-setup | lxc-attach -n $(hostname)-lxc;



