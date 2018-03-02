#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine
# Import call submodule to do external (virsh) commands
from subprocess import check_output

class ListMachines:
""" Class handling the machines' list by calling virsh.
TODO : Parsing logic could be grouped up in less functions.
"""

    def __init__(self):
        self.machine_list = self.build_machine_list()

    def serialize_machine_list(self):
        json_machine_list = []
        for machine in self.machine_list:
            json_machine_list.append(machine.serialize_machine())
        return json_machine_list

    def get_machine_list(self):
        if (self.machine_list != None):
            return self.machine_list
        else:
            self.machine_list = self.build_machine_list()
            return self.get_machine_list()

    def list_machines(self):
        virsh_list = check_output(["virsh", "list", "--all"]).decode("utf-8")
        virsh_list = virsh_list.split("-\n")[1]
        return virsh_list

    def count_machines(self):
        return self.list_machines().count('\n') -1

    def parse_virsh_list(self):
        virsh_list = self.list_machines()
        virsh_list = virsh_list.split('\n')
        parsed_list = []
        for element in virsh_list:
            element = element.split()
            parsed_list.append(element)
        return parsed_list

    def build_machine_list(self):
        parsed_virsh_list = self.parse_virsh_list()
        machine_list = []
        for i in range(0,self.count_machines()):
            if parsed_virsh_list[i][2] == "shut" and len(parsed_virsh_list[i])== 4:
                machine_list.append(machine.Machine(parsed_virsh_list[i][0],
                                            parsed_virsh_list[i][1],
                                            parsed_virsh_list[i][2]+" "+parsed_virsh_list[i][3]))
            else:
                machine_list.append(machine.Machine(parsed_virsh_list[i][0],
                                            parsed_virsh_list[i][1],
                                            parsed_virsh_list[i][2]))
        return machine_list
