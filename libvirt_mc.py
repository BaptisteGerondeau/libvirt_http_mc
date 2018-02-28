#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Libvirt Management Controller class
This is a webapp to control virtual machines run by libvirt via an RESTlike
API.
"""

import os.path

import machine, listmachines, machine_control, machine_state_control
# Import call submodule to do external (virsh) commands
from subprocess import check_output
# Import CherryPy global namespace
import cherrypy
import json

class Root(object):
    def __init__(self):
        self.service = MCGeneratorWebService()

    @cherrypy.expose
    def index(self):
        return 'man page'

@cherrypy.expose
@cherrypy.popargs('machine_name')
class MCGeneratorWebService(object):

    def __init__(self):
        self.controller = machine_control.Machine_Control()
        self.state_controller = machine_state_control.Machine_State_Control()

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, machine_name):
        if machine_name == 'machines':
            return json.dumps(self.controller.machine_list.serialize_machine_list())
        else:
            if self.controller.check_machine_existence(machine_name):
                return json.dumps(self.controller.get_machine_byname(machine_name).serialize_machine())
            else:
                return 'FAILURE'

mcconf = os.path.join(os.path.dirname(__file__), 'libvirtmc.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(Root(), config=mcconf)
