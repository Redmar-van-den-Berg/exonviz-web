Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vm.hostname = "exonviz"

  config.vm.network :forwarded_port, guest: 80, host: 8000, host_ip: "127.0.0.1"

  config.vm.provider :libvirt do |libvirt|
    libvirt.memory = 500
    libvirt.cpus = 1
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.verbose = "v"
    ansible.tags = "all,never"
    ansible.vault_password_file = "vault"
  end

end
