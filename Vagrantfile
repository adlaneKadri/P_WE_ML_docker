# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :
# Box / OS
#VAGRANT_BOX = 'ubuntu/trusty64'
VAGRANT_BOX = "ubuntu/groovy64"
# Memorable name for your
VM_NAME = 'kadri'
# VM User — 'vagrant' by default
VM_USER = 'vagrant'
# Username on your Mac
MAC_USER = 'adlan'
# Host folder to sync
#HOST_PATH = '/users/' + MAC_USER + '/' + VM_NAME
HOST_PATH = '/home/adlan/Music/university/paris8/docker_project/P_WE_ML_docker/vagrant'
# Where to sync to on Guest — 'vagrant' is the default user name
GUEST_PATH = '/home/' + VM_USER + '/' + VM_NAME
#GUEST_PATH = '/home/adlan/Music/university/paris8/docker_project/P_WE_ML_docker/docker_compose'
# # VM Port — uncomment this to use NAT instead of DHCP
# VM_PORT = 8080
Vagrant.configure(2) do |config|
  # Vagrant box from Hashicorp
  config.vm.box = VAGRANT_BOX
  config.vm.hostname = VM_NAME

  
  config.vm.provider "virtualbox" do |v|
    v.name = VM_NAME
    v.cpus = 3
    v.memory = 2048
  end

  config.vm.network "forwarded_port", guest: 80, host: 8080
  # Sync folder
  config.vm.synced_folder HOST_PATH, GUEST_PATH
  # Disable default Vagrant folder, use a unique path per project
  #config.vm.synced_folder '.', '/home/'+VM_USER+'', disabled: true

  # Installation docker 
  # a.vm.provider "docker" do |d|
  #     d.build_dir = "."
  #     d.build_args = ["-t=vertxdev"]
  #     d.ports = ["8080:8080"]
  #     d.name = "vertxdev"
  #     d.remains_running = true
  #     d.cmd = ["vertx", "run", "vertx-examples/src/raw/java/httphelloworld/HelloWorldServer.java"]
  #     d.volumes = ["/src/vertx/:/usr/local/src"]
  #   end

  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"

  #install docker 
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y git
  #   apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  #   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  #   sudo apt-key fingerprint 0EBFCD88
  #   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)    stable"
  #   apt-get update
  #   apt-get upgrade -y
  #   apt-get install docker-ce docker-ce-cli containerd.io
  #   sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  #   sudo chmod +x /usr/local/bin/docker-compose

  # SHELL

  # Install Git, Node.js 6.x.x, Latest npm
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git
    snap install docker
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    apt-get install -y nodejs
    apt-get install -y build-essential
    npm install -g npm
    apt-get update
    apt-get upgrade -y
    apt-get autoremove -y
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    sudo docker-compse -up 
  SHELL

end