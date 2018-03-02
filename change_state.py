#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import machine

import bootorder_xml
# Import call submodule to do external (virsh) commands
from subprocess import check_output, call
from subprocess import CalledProcessError
from datetime import date
from shutil import copy2

class Change_State(object):
    """This class handles all calls to virsh specific to a machine.
    """
    def get_xmlpath(self, machine):
        xmlname = machine.name + '.xml'
        return os.path.join(os.path.dirname(__file__), xmlname)

    def power_on(self, machine):
        try:
            virsh_output = check_output(['virsh', 'start', machine.name])
        except CalledProcessError as e:
            print("Failed to start machine : %s" % e.output)

    def power_off(self, machine):
        try:
            virsh_output = check_output(['virsh', 'shutdown', machine.name])
        except CalledProcessError as e:
            print("Failed to shutdown machine : %s" % e.output)

    def reboot(self, machine):
        try:
            virsh_output = check_output(['virsh', 'reboot', machine.name])
        except CalledProcessError as e:
            print("Failed to reboot machine : %s" % e.output)

    def force_reset(self, machine):
        try:
            virsh_output = check_output(['virsh', 'reset', machine.name])
        except CalledProcessError as e:
            print("Failed to reset machine : %s" % e.output)

    def force_off(self, machine, graceful=True):
        """This function performs a hard shutdown i.e. SIGTERM or SIGKILL to
        the process. Note that SIGKILL will be employed if the graceful flag is
        not put to True. For the moment this is not used.
        """
        if graceful:
            try:
                virsh_output = check_output(['virsh', 'destroy', '--graceful', machine.name])
            except CalledProcessError as e:
                print("Failed to reset machine : %s" % e.output)
        else:
            try:
                virsh_output = check_output(['virsh', 'destroy', machine.name])
            except CalledProcessError as e:
                print("Failed to reset machine : %s" % e.output)

    def pxeboot(self, machine):
        self.dumpxml(machine, True)
        new_bootorder_setter = bootorder_xml.Bootorder_XML(self.get_xmlpath(machine))
        new_bootorder_setter.set_new_bootorder('pxe')
        self.restore_fromxml(machine)

    def diskboot(self, machine):
        self.dumpxml(machine, True)
        new_bootorder_setter = bootorder_xml.Bootorder_XML(self.get_xmlpath(machine))
        new_bootorder_setter.set_new_bootorder('disk')
        self.restore_fromxml(machine)

    def defaultboot(self, machine):
        pass

    def dumpxml(self, machine, backup=False):
        try:
            fp = open(self.get_xmlpath(machine), 'w+')
        except IOError as e:
            print(e.errno)
            print(e.strerror)
        try:
            virsh_output = call(['virsh', 'dumpxml', '--inactive',
                                         machine.name], stdout=fp)
        except CalledProcessError as e:
            print('Failed to dumpxml : %s' % e.output)
        fp.close()
        if backup:
            today = date.today().strftime('%d%m%Y')
            backup_name = str(self.get_xmlpath(machine) + today + '.backup')
            copy2(self.get_xmlpath(machine), backup_name)

    def restore_fromxml(self, machine):
        """This function does bootup the machine when called after having
        (re)created the VM following the xml specs.
        """
        try:
            virsh_output = check_output(['virsh', 'create', self.get_xmlpath(machine)])
        except CalledProcessError as e:
            print("Failed to restore (create) machine from xml : %s" %
                  e.output)
