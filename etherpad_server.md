# Etherpad Server in the Pangolin Environment

Etherpad is a collaborative web-based text editing and chat environment. For more information
see https://etherpad.org/ or https://github.com/ether/etherpad-lite

This is accomplished in two steps:

1. Run the `pangolin_base_server.yml` playbook.
1. Run the `etherpad_server.yml` playbook.

If you start the _Pangolin_ environment at that point the `http://world.pangolin/` home page will
have a link to _Etherpad_ at http://etherpad.pangolin:9001/

##### How do I know if it's working?

One way to see if all of the required services are running is with `systemctl list-dependencies pangolin.target`.
The bullets should show green for running services.

### Before you run the playbooks

Copy `global_vars.yml.sample` to `global_vars.yml` and make any required changes. By default it is planning to
own the entirety of `10.0.0.0/8`; if that's not to your liking, you should do something about it.

Replace the entry under `[pangolin_server]` in the `hosts` file with your build target.

Download distributions of _NodeJS_ ("Linux Binaries" `.tar.xz` from https://nodejs.org/en/download/)
and _Etherpad_ ("Linux/Mac" `.zip` from https://etherpad.org/) and store them somewhere where your _Ansible_ server can
find them. (`/opt/downloads/` is shown in the sample `global_vars`) *The script expects those two archive formats,
respectively.* If you want to do something else you'll have to change how the script handles unpacking them.

### While the playbook is running, or if it fails for a random reason

If one of the scripts fails to run because of an error, then you need to fix it; you may even need to restart
with a freshly paved VM. However because of connectivity issues or other sorts of random events either or both
of the scripts may fail to complete successfully the first time through.

The `pangolin_base_server` playbook is more or less idempotent; if for some reason it fails to install something
because it can't reach the archive, then wait a while and run it again. It should skip anything that's already been
done.

In the `etherpad_server` playbook there are two places where something can go wrong. The first is during installation
of dependencies at the beginning, in which case just restart. When you get to the point where it's unpacking the
distributions, it may be idempotent but it's not guaranteed; hopefully failure is not likely at this point.

The second place where failure is likely is quite close to the end when it's running the Etherpad application for
the first time. It's necessary to do this because _Node_ pulls in quite a lot of stuff and it needs to do this
before the application can be run successfully offline. If the script fails at this point, log into the box and
see if it's still running; if so, consider just letting it run until it answers on port 9001. You can manually
shut it down with `systemctl stop etherpad.service`.

##### Hangs while running the Etherpad application for the first time

No, really hangs. Nothing is happening. Did you set the sudo access for the privileged account as
`ALL = (ALL) NOPASSWD: ALL`? It needs to sudo to the `etherpad` account for this step.

### After running the playbooks

The `pangolin.target` exists as a way to manage the components collectively with `systemctl`.

As already mentioned, `systemctl list-dependencies pangolin.target` will show you the status of the required services.
`systemctl start pangolin.target` will start all of them.

By default `pangolin.target` is left _enabled_ which means that `systemctl stop pangolin.target` will stop all of
them, but it also means that starting one of the individually (e.g. `apache` or `etherpad`) will start them all. If
you want to be able to start them individually then _disable_ `pangolin.target` by running `systemctl disable pangolin.target`.
