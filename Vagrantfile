# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"

  config.vm.network 'forwarded_port', guest: 5000, host: 5000

  config.vm.provision :shell, path: "install.sh"
end
