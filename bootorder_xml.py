#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

class Bootorder(object):
"""Class handling bootorder representation for manipulation.
"""
    def __init__(self):
        self.bootorder = []
        self.original_bootorder = []

    def add_dev(self, xmlelement, device_type, device_subtype, order):
        bootdev = [xmlelement, device_type, device_subtype, order]
        self.bootorder.append(bootdev)

    def set_original_bootorder(self):
        self.original_bootorder = self.bootorder

    def set_sort_list(self, device_type):
        sort_dict = []
        sorted_original = self.sort_bootorder(self.original_bootorder)
        for i in range(0, len(sorted_original)):
            if sorted_original[i][1] == device_type:
                sort_dict.append(sorted_original[i][0])
        return sort_dict

    @staticmethod
    def sort_bootorder(bootorder):
        return sorted(bootorder, key=lambda bootdev: bootdev[3])

    @staticmethod
    def nb_specifictype_bootdev(bootorder, bootdev_type):
        nb_bootdev_type = 0
        for dev in bootorder:
            if dev[1] == bootdev_type:
                nb_bootdev_type += 1
        return nb_bootdev_type

class Bootorder_XML(object):
"""Class handling bootorder parsing and rearrangment via XML parsing.
Note that the sorting is made so that it preserves initial order of the boot
devices per subtype : i.e. if NIC1 is above NIC2 in the original bootorder, it
will also be in the PXEboot, and in the diskboot bootorder as well.
It requires that you activate each device in the bootorder menu of
virt-manager, as else the boot entry in the XML will not be there
"""
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.xmltree = etree.parse(xmlfile)
        self.bootorder = Bootorder()
        self.get_current_bootorder(original=True)

    def get_current_bootorder(self, original=False):
        root = self.xmltree.getroot()
        for dev in root.find('devices'):
            boot = dev.find('boot')
            if boot is not None:
                if dev.get('device') is not None:
                    subtype = dev.get('device')
                elif dev.find('source').get('network') is not None:
                    subtype = dev.find('source').get('network')
                else:
                    print('Unsupported boot device')
                self.bootorder.add_dev(
                    dev,
                    dev.tag,
                    subtype,
                    boot.get('order'))
        if original:
            self.bootorder.set_original_bootorder()

    def write_bootorder(self, bootorder):
        for bootentry in bootorder:
            bootdev = bootentry[0]
            if bootdev.find('boot') is not None:
                bootdev.find('boot').set('order', str(bootentry[3]))
            else:
                print("Bootorder is bad and contains non bootable devices")
        self.xmltree.write(self.xmlfile)

    def set_new_bootorder(self, bootorder_type):
        sort_list_netdev = self.bootorder.set_sort_list('interface')
        sort_list_diskdev = self.bootorder.set_sort_list('disk')
        nb_netdev = Bootorder.nb_specifictype_bootdev(self.bootorder.bootorder,
                                                                       'interface')
        nb_diskdev = Bootorder.nb_specifictype_bootdev(self.bootorder.bootorder, 'disk')
        if bootorder_type == 'pxe':
            new_order = self.bootorder.bootorder
            for i in range(0, len(new_order)):
                if new_order[i][1] == 'interface':
                    new_order[i][3] = sort_list_netdev.index(new_order[i][0])+1
                if new_order[i][1] == 'disk':
                    new_order[i][3] = sort_list_diskdev.index(new_order[i][0])
                    new_order[i][3] += 1+nb_netdev
            self.write_bootorder(new_order)
        elif bootorder_type == 'disk':
            new_order = self.bootorder.bootorder
            for i in range(0, len(new_order)):
                if new_order[i][1] == 'interface':
                    new_order[i][3] = sort_list_netdev.index(new_order[i][0])
                    new_order[i][3] += 1+nb_diskdev
                if new_order[i][1] == 'disk':
                    new_order[i][3] = sort_list_diskdev.index(new_order[i][0])+1
            self.write_bootorder(new_order)
        elif not bootorder_type in ['pxe', 'disk', 'default']:
            print("Incorrect boot type")
