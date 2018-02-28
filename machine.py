#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Machine(object):

    def __init__(self, id, name, state):
        self.name = name
        self.id = id
        self.state = state

    def serialize_machine(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'state' : self.state, }

    def serialize_state(self):
        return { 'state' : self.state }
