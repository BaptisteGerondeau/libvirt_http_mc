#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine, listmachines, machine_control, change_state
import cherrypy
import time

@cherrypy.expose
class Machine_State_Control(object):

    def __init__(self):
        self.state_changer = change_state.Change_State()
        self.helper = machine_control.Machine_Control()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self, machine_name):
        return self.helper.get_machine_byname(machine_name).serialize_state()

    @cherrypy.expose
    def cyclepower(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
        if machine.state == 'shut off':
            self.state_changer.power_on(machine)
        elif machine.state == 'running':
            self.state_changer.power_off(machine)
        elif machine.state == 'idle' or machine.state == 'pmsuspended':
            self.state_changer.power_off(machine)
        elif machine.state == 'dying':
            time.sleep(5)
        elif machine.state == 'crashed':
            self.state_changer.force_reset(machine)

    @cherrypy.expose
    def reboot(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
        self.state_changer.reboot(machine)

    @cherrypy.expose
    def force_reboot(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
        self.state_changer.force_reset(machine)

    @cherrypy.expose
    def force_off(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
        self.state_changer.force_off(machine)

    @cherrypy.expose
    def pxeboot(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
        while machine.state != 'shut off':
            self.cyclepower(machine)
            time.sleep(5)
            machine = self.helper.get_machine_byname(machine_name)
        self.state_changer.pxeboot(machine)
#        self.state_changer.power_on(machine)

    @cherrypy.expose
    def diskboot(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
#        if machine.state == 'running' or machine.state == 'idle' or machine.state == 'pmsuspended':
#            self.cyclepower(machine)
#            time.sleep(5)
#        elif machine.state != 'shutoff':
#            self.state_changer.reset(machine)
#            time.sleep(5)
        self.state_changer.diskboot(machine)
#        self.state_changer.power_on(machine)

    @cherrypy.expose
    def defaultboot(self, machine_name):
        machine = self.helper.get_machine_byname(machine_name)
#        if machine.state == 'running' or machine.state == 'idle' or machine.state == 'pmsuspended':
#            self.cyclepower(machine)
#            time.sleep(5)
#        elif machine.state != 'shutoff':
#            self.state_changer.reset(machine)
#            time.sleep(5)
        self.state_changer.defaultboot(machine)
#        self.state_changer.power_on(machine)
