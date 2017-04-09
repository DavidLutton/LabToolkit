#!/usr/bin/env python3
import time
import logging


class GenericInstrument(object):

    def __repr__(self):
        return("{}, {}".format(__class__, self.instrument))

    def __init__(self, instrument):
        self.instrument = instrument
        self.log = logging.getLogger("RCI")

        self.IDN = self.instrument.query('*IDN?')
        self.options = self.query("*OPT?").strip().split(',')

    def query(self, query):
        self.log.debug("Query {}: {}".format(self.instrument.resource_name, query))
        response = self.instrument.query(query)
        self.log.debug("Respo {}: {} \t {}".format(self.instrument.resource_name, query, response))
        return(response)

    def write(self, query):
        self.log.debug("Write {}: {}".format(self.instrument.resource_name, query))
        return(self.instrument.write(query))
