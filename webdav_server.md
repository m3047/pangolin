# WebDAV Server in the Pangolin Environment

_Distributed Authoring and Versioning (DAV)_ is a standard for HTTP-based collaborative content sharing and editing;
the simple example is file sharing, including editing/publishing. File sharing capability with _DAV_ is
part of _Apache Core_ (`mod_dav` and `mod_dav_fs`).

When _DAV_ is installed, _apache_ presents as a file server using the _DAV_ protocol. Your operating system will
provide a mechanism to connect to the server located at http://webdav.pangolin/ or dav://webdav.pangolin/.
You will connect as a guest, with no authentication; there will be no password or key, and you will be able to
upload / download content from the web server as though you were accessing a file share.

Direct editing of files on the _DAV_ server is not recommended.

A simple convention for use when there is one primary editor for a selection of content is:

1. Create a folder locally for the content.
1. Compose your work in the local folder.
1. Upload the local folder to the _DAV_ server.
1. Continue to edit locally and copy / update to the server as needed.

If you must edit a single file from the server:

1. Copy the file from the _DAV_ server to a local folder.
1. Edit the local copy.
1. Upload the changed / updated copy of the file back to the _DAV_ server.

##### No muffler, no plates...

From the foregoing I hope you took note that __there is no authentication, and you can write files on the server__.

IT SHOULD BLOODY WELL GO WITHOUT SAYING THAT YOU SHOULD NEVER NEVER SET THIS UP ON A VM WHICH IS GOING TO BE
EXPOSED TO THE ACTUAL INTERNET. Child porn, Edward Snowden, 4chan... need I say more?

Anybody within fifty feet of the wifi antenna is a different situation than anyone on the entire internet; use
your best risk management assessment and plan accordingly. _DAV_ is restricted to a specific folder hierarchy and
it's running as the web server user (not `root`); the rest is up to you.

### Basic installation

Generally speaking a given playbook should only be run (successfully) once. If it's been run and it's called
out somewhere, consider that a met dependency.

1. Run the `pangolin_base_server.yml` playbook.
2. Run the `dav_server.yml` playbook.

After this, the page at http://world.pangolin/ will contain a link to the _WebDAV_ environment.

### Before or While Running the playbooks

No special considerations apply, _DAV_ is part of _Apache Core_ it only needs to be enabled and configured.

### After running the playbooks

If _Apache_ is running then _DAV_ is running. As previously noted, BE CAREFUL ABOUT CHOOSING THE SURROUNDING
PHYSICAL ENVIRONMENT WHEN YOU RUN THIS.
