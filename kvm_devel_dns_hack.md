# DNS Hacks for KVM Development Environments

28-Dec-2019 Fred Morris

You may not always have a spare wifi antenna (or want one). In a lot of cases you may want to keep your development
environment contained to a single desktop or laptop. If you run your own local DNS with a vanity (private) TLD and
you're using _KVM_ you're in luck! Otherwise there's always the `/etc/hosts` file.

### KVM's virbr Devices

When you set up a `virbr` device under _KVM_ you give it some address space and routing is set up on host and other
magic happens and so you can connect directly from your host machine to the VM's ip address within the `virbr` device's network.

### Common Scenario: Testing with software running natively on the host OS

A common example would be a web browser, and on the _Pangolin_ web server at `world.pangolin` you've set up named
virtual hosting (maybe you've got `chat.pangolin` on there too).

##### /etc/hosts

You could put `world.pangolin` in `/etc/hosts` and point it at the VM's ip address. That will work so that the
browser gets the correct address.

##### DNS

Using a DNS entry within your vanity domain and given that your vanity domain
(`example` without the `.com`) is in your _domain search list_, things
should also resolve correctly:

1. `world.pangolin` doesn't resolve.
1. `.example` is appended and `world.pangolin.example` resolves to the VM's address.
1. The web browser doesn't care and still sends just `world.pangolin` as the hostname.
