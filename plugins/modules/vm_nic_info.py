#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: vm_nic_info

author:
  - Domen Dobnikar (@domen_dobnikar)
short_description: Returns info about nic.
description:
  - Returns info about all or specific nic on a selected virtual device.
version_added: 0.0.1
extends_documentation_fragment:
  - scale_computing.hypercore.cluster_instance
seealso: []
options:
  vm_name:
    description:
      - Virtual machine name
      - Used to identify selected virtual machine by name
    type: str
  vm_uuid:
    description:
      - Virtual machine uniquie identifier
      - Used to identify selected virtual machine by uuid
    type: str
  vlan:
    description:
      - Vlan on which network interface is operating on
      - Used to identify specific network interface
      - If included only network interface with the specified vlan will be returned
    type: int
"""

EXAMPLES = r"""
- name: Retrieve all VMs
  scale_computing.hypercore.sample_vm_info:
  register: result

- name: Retrieve all VMs with specific name
  scale_computing.hypercore.sample_vm_info:
    vm_name: vm-a
  register: result
"""

RETURN = r"""
vms:
  description:
    - A list of VMs records.
  returned: success
  type: list
  sample:
    - vm_name: "vm-name"
      uuid: "1234-0001"
      state: "running"
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, errors
from ..module_utils.client import Client
from ..module_utils.vm import VM
from ..module_utils.utils import validate_uuid


def check_parameters(module):
    if module.params["vm_uuid"]:
        validate_uuid(module.params["vm_uuid"])


def create_vm_object(
    module, client
):  # if we decide to use name and vm_uuid across all playbooks we can add this to .get method in VM class
    if module.params["vm_uuid"]:
        virtual_machine_list = VM.get_legacy(client, uuid=module.params["vm_uuid"])
        if not virtual_machine_list:
            raise errors.VMNotFound(module.params["vm_uuid"])
        virtual_machine_dict = virtual_machine_list[0]
    else:
        virtual_machine_list = VM.get_legacy(client, name=module.params["vm_name"])
        if not virtual_machine_list:
            raise errors.VMNotFound(module.params["vm_name"])
        virtual_machine_dict = virtual_machine_list[0]
    return VM.from_hypercore(vm_dict=virtual_machine_dict)


def create_output(records):
    return False, records


def run(module, client):
    check_parameters(module)
    if module.params["vlan"]:
        virtual_machine = create_vm_object(module, client)
        records = [
            virtual_machine.find_nic(module.params["vlan"]).data_to_ansible()
        ]  # Consistency with output []
    else:  # No vlan, we output all NICs for specified VM
        virtual_machine = create_vm_object(module, client)
        records = [nic.data_to_ansible() for nic in virtual_machine.nic_list]
    return create_output(records)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            vm_name=dict(
                type="str",
            ),
            vm_uuid=dict(
                type="str",
            ),
            vlan=dict(
                type="int",
            ),
        ),
        mutually_exclusive=[
            ("vm_name", "vm_uuid"),
        ],
        required_one_of=[("vm_name", "vm_uuid")],
    )

    try:
        host = module.params["cluster_instance"]["host"]
        username = module.params["cluster_instance"]["username"]
        password = module.params["cluster_instance"]["password"]

        client = Client(host, username, password)
        changed, records = run(module, client)
        module.exit_json(changed=changed, records=records)
    except errors.ScaleComputingError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
