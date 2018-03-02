#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine, listmachines

class Machine_Control(object):
"""Class used to fetch and check for the called machine's existence.
The virsh logic is handled by ListMachines class
"""
    def get_machine_byname(self, machine_name):
        machine_list = listmachines.ListMachines()
        for machine in machine_list.get_machine_list():
            if machine.name == machine_name:
                return machine
        raise FileNotFoundError('Machine %s is unknown' % machine_name)

    def check_machine_existence(self, machine_name):
        try :
            self.get_machine_byname(machine_name)
        except FileNotFoundError as e:
            return False
        return True


