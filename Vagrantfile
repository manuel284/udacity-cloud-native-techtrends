# set up the default terminal
ENV["TERM"]="linux"

Vagrant.configure("2") do |config|
  
  # set the image for the vagrant box
  ####config.vm.box = "opensuse/Leap-15.2.x86_64"
  config.vm.box = "hashicorp/bionic64"
  ## Set the image version
  # config.vm.box_version = "15.2.31.247"

  # st the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # consifure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    #### vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end
end