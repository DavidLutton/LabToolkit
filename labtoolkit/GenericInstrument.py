#!/usr/bin/env python3
"""."""
import time
import logging


class GenericInstrument(object):

    def __repr__(self):
        return(f"{__class__}, {self.instrument}")

    def __init__(self, instrument):
        self.instrument = instrument
        self.log = logging.getLogger("RCI")

        # self.IDNs = self.instrument.query('*IDN?')
        # self.options = self.query("*OPT?").strip().split(',')

    def query(self, query):
        self.log.debug(f"Query {self.instrument.resource_name}: {query}")
        response = self.instrument.query(query)
        self.log.debug(f"Respo {self.instrument.resource_name}: {query} \t {response}")
        return(response)

    def write(self, query):
        self.log.debug(f"Write {self.instrument.resource_name}: {query}")
        return(self.instrument.write(query))

    '''def preset(self):
        return NotImplemented
    '''
