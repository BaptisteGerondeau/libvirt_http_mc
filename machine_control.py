#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine, listmachines

class Machine_Control(object):

    def __init__(self):
        self.machine_list = listmachines.ListMachines()

    def get_machine_byname(self, machine_name):
        for machine in self.machine_list.get_machine_list():
            if machine.name == machine_name:
                return machine
        raise FileNotFoundError('Machine %s is unknown' % machine_name)

    def check_machine_existence(self, machine_name):
        try :
            self.get_machine_byname(machine_name)
        except FileNotFoundError as e:
            return False
        return True


