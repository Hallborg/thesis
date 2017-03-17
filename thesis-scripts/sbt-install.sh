apt-get update;

apt-get install openjdk-8-jre;

echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list;

curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -;
sudo apt-get update;
apt-get install cassandra;

apt-get install docker-ce;

apt install lxc debootstrap bridge-utils;
