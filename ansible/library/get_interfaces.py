#!/usr/bin/python3
# Copyright (c) 2019 Fred Morris Tacoma WA USA m3047-pangolin-g3n@m3047.net
#
# This file is part of Pangolin
#
# Pangolin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pangolin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pangolin.  If not, see <http://www.gnu.org/licenses/>.

import ipaddress
import netifaces

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: get_interface

short_description: Get the name of the interface we're connected with.

author:
    - Fred Morris (pangolin3047ag@m3047.net)
'''

EXAMPLES = '''
# Get the interface name.
- name: Get the interface
  get-interfaces:
  register: result
- debug:
    msg: "Interface: {{ result.interfaces[0] }}
'''

RETURN = '''
interface:
    description: The name of the interface we're connected with.
    type: str
    returned: always
'''

LOOPBACK = ipaddress.IPv4Network('127.0.0.0/8')

from ansible.module_utils.basic import AnsibleModule

def main():
    module_args = dict()

    result = dict(
        changed=False,
        interfaces=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
        
    ifaces = set()

    for iface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(iface)
        if netifaces.AF_INET not in addresses:
            continue
        for address in addresses[netifaces.AF_INET]:
            try:
                addr = ipaddress.IPv4Address(address['addr'])
                if addr in LOOPBACK:
                    continue
                ifaces.add(iface)
            except ipaddress.AddressValueError:
                continue
    result['interfaces'] = list(ifaces)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
