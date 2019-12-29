# Pangolin: A Self-Contained Wireless Environment

**Status: Alpha test**

_Pangolin_ can be utilized as a collaboration environment, wifi firing range for cybersecurity exercises, and for various kinds of IoT testing.

The base functionality of _Pangolin_ consists of three features:

* A DHCP server
* A DNS server
* A web server

If you successfully configure and launch the _Pangolin_ server within the wifi environment, it will provide connecting devices with an address and the location of the DNS server. Essentially what you will see happen is that if you connect to the wifi network and launch a web browser, no matter what web site name you enter it will redirect you to the pangolin web server (which only serves HTTP, not HTTPS, by default).

Primarily this project consists of _Ansible_ scripts for configuring a VM as a server to be run in bridging mode connected to the wifi interface managed by the laptop ("host") OS. The type of wifi network and associated access controls (if any) you can create is going to be dictated by the host OS. _Be prepared for the possibility that anyone within wifi range can connect without authentication_, particularly when extending _Pangolin_: extensions should be prepared to perform their own user authentication as needed.

##### The problem with laptops (not running Linux)

I've only tested this on a _MacBook_ so far, although I expect the findings will apply to laptops running _Windows_ as well.

There's a problem getting unfettered access to the wifi transceiver particularly in _AP_ mode. That's not completely surprising, wifi operation faces different limitations in different jurisdictions, and as worldwide purveyors Apple and Microsoft probably have to exercize some control to limit liability.

Searching the internet suggests that this can be circumvented by using a USB Wifi dongle; at some point I'll probably get one and see if I can set up _hostapd_, the Linux access point manager.

### Installation

At the present time only _Debian_ is supported, although more Linux distributions are likely to follow.

The following have been tested:

* OSX + VirtualBox + Debian 9.6 (Stretch)
* Linux + KVM + Debian 10.2 (Buster)

##### Prepare a base installation

Create a VM inside of _VirtualBox_. You must create a bridged interface to the wifi device (e.g. `en0` on the _MacBook_), this is the interface which will be utilized by the server.

We recommend that you create two interfaces, as follows:

1. A "traditional" NATted interface.
1. The bridged interface.

**Only one of these interfaces should ever be enabled at a given point in time.**

Set up port forwarding on the NATted interface for SSH access.

If you do the foregoing, you can leave the bridged interface disabled and unconfigured during installation; _Pangolin_ will set it up for you.

During my testing, this consistently creates the following two network interfaces within the VM:

* `enp0s3`: the NATted interface
* `enp0s8`: the bridged interface

In particular, if the bridged interface is not `enp0s8` you will need to edit `global_vars.yml`.

Perform a base installation of _Debian 9.6_ with _SSHD_ installed and activated. Create an account for access to the VM, we're using `animal` but you can change that in `global_vars.yml`.

Verify connectivity with _SSH_, and set up passwordless _sudo_ for access account,.

##### Prepare to install _Pangolin_

Edit `hosts` and change the target host declared in the `[pangolin_server]` section to point to your target VM.

If necessary, edit `global_vars.yml`. Things you might need to change are:

* `pangolin.domain_name`: the "TLD" (equivalent to `.com`, `.net`, etc.)
* `pangolin.server_address`: the address the server will use within the virtualized environment.
* `pangolin.{subnet,network,cidr}`: these define the network.
* `pangolin.dhcp_range__{start,end}`: these define the address range to be handed out via DHCP.
* `pangolin.admin_account`: this is the account you can SSH to the VM with, and should be the same as the one you use for installation.
* `os_vars[].interface[]`: this is the name of the bridged interface.

**Python 3**: The Ansible scripts are intended to be run with _Python 3_ on the guest VM. Take a look at `host_vars/pangolin.ansible.m3047.yml`, you may need to copy or rename this file to whatever you set in `hosts` in `[pangolin_server]`. It really doesn't hurt to do this in any case.

##### Install _Pangolin_

Run the `pangolin_base_server.yml` playbook. Exactly how to do this depends on whether you set the admin account up with a public key in `known_hosts`, or with a password.

If you use a password you will also have to disable `host_key_checking` in `ansible.cfg`. If you use a password, the command line might look like:

```
ansible-playbook -u animal --ask-pass --ssh-extra-args '-p 2222' --sftp-extra-args '-P 2222' pangolin_base_server.yml
```

The script is intended to be idempotent: you should be able to re-run it if it fails during execution (due to network connectivity or other issues).

##### Running the Pangolin Server

Shut the VM down, and edit the network settings:

* disable the NATted interface
* enable the bridged interface

Use appropriate host operating system fu to create a wifi network.

Launch the VM.

Connect to it from the host system. It should be listening for SSH connections on port 22, at the address given in `pangolin.server_address` and have the name `world.pangolin` (although this doesn't matter at this point because DNS is going rewrite everything to that address).

The default server address is `10.30.47.1`. If you try to SSH to it (instead of using the console), be aware that since DHCP is not yet running, your host OS needs a fixed address in `10.0.0.0/8` when connected to the network (I recommend `10.30.47.2`).

**Issue with setting the DNS server on OSX** I've encountered the situation where the host OS doesn't consistently "see" that it should use Pangolin's DNS server, even when manually configured; I suspect an issue with the "tap" interface that bridging interfaces are based on. I've resorted to adding `world.pangolin` (at `10.30.47.1`)  to the laptop's `/etc/hosts` file.

Once connected (assuming you set up passwordless =sudo= for the admin user):

```
sudo systemctl start pangolin.target
```

##### Invite your friends!

At this point, configure another laptop to use DHCP, and then connect it to the _Pangolin_ wifi network. Launch a web browser, and if all goes according to plan you should see the "Pangolin" splash page. If that doesn't work, try http://world.pangolin/ before assuming something is wrong.

Note that it only uses HTTP, so if you try to connect with HTTPS it will fail.

### The purpose of `pangolin.target`

The reason for having `pangolin.target` is to be able to start and stop all of the component services at a
single shot.

Due to limitations of `systemctl`, if you leave it _enabled_ at all times then starting one of its
component services will start them all; and you have to leave it _enabled_ so that if you shut it down it will
shut down the component services.

Regardless of whether you leave `pangolin.target` enabled or disabled (described in the following sections)
you can always query `pangolin.target` to see the status of component services:

```
# systemctl list-dependencies pangolin.target
pangolin.target
● ├─apache2.service
● ├─bind9.service
● └─isc-dhcp-server.service
```

The cut & paste doesn't do it justice, in a terminal window the bullets are different colors depending on whether
the service is running (green) or not (black).

##### Leaving `pangolin.target` enabled

When _Pangolin_ sets up, `pangolin.target` is stopped but enabled; because nothing in the boot process depends
on it (or its component services) it's for all practical purposes not running. If you execute
```
# systemctl start pangolin.target
```
that will start all of the component services.

To shut them all down:
```
# systemctl stop pangolin.target
```

As noted above, due to limitations of `systemctl`, the following will also happen:

* If you start a component service, they will all be started.
* You can still stop a single component manually.

##### I just want to be able to run a single service

If this is the case, then disable the `pangolin.target`:
```
# systemctl disable pangolin.target
```

Now you can individually control one of the component services:
```
# systemctl start apache2.service
# systemctl list-dependencies pangolin.target
# systemctl stp apache2.service
# systemctl list-dependencies pangolin.target
```

##### I just want to be able to stop them all with `pangolin.target`

If this is the case, then disable the `pangolin.target`:
```
# systemctl disable pangolin.target
```
You can start all of the services by starting `pangolin.target` if you wish, or you can start
individual services:
```
# systemctl start apache2.service bind9.service
```

To stop them all, you need to run the following sequence of commands (or put them in a script):
```
# systemctl enable pangolin.target
# systemctl stop pangolin.target
# systemctl disable pangolin.target
```

### Future Work

##### Additional OSes

Additional OSes (host and guest server) and targeted instructions. This will require community help.

##### Collaboration Tools

We anticipate that various software packages will be layered on top of the base server for specific purposes.

One of the first ones I'll be developing will involve some web-based collaboration tools.
