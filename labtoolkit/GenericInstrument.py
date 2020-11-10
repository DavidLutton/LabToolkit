from time import sleep
import logging
from logging.handlers import SocketHandler


log = logging.getLogger('lt')
log.setLevel(1)
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)


class GenericInstrument(object):
    """Wrap instrument with some utility functions."""

    def __init__(self, inst):
        """."""
        self.inst = inst

        # self.logger = logging.getLogger(__name__)
        self.logger = log.getChild(f'{type(self).__name__} on {self.inst.resource_name}')
        # self.logger.setLevel(1)  # to send all records to cutelog
        # socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
        # self.logger.addHandler(socket_handler)
        # self.logger.info('Hello world!')

        self.query_binary_values = self.inst.query_binary_values
        self.write_binary_values = self.inst.write_binary_values

    def __repr__(self):
        """."""
        return f"{type(self).__name__} on {self.inst.resource_name}"

    def write(self, *args, **kwargs):
        """Wrap write to log what is sent."""
        # print(*args)
        self.logger.info(*args)
        return self.inst.write(*args, **kwargs)

    def query(self, *args, **kwargs):
        """Wrap query to log what is sent & recieved."""
        # print(*args)
        self.logger.info(*args)
        resp = self.inst.query(*args, **kwargs)
        self.logger.debug(resp)
        return resp

    def query_float(self, *args, **kwargs):
        """Suitable for querys to instruments that return a single value float.

        Returns:
            float: float.
        """
        return float(self.query(*args, **kwargs))

    def query_int(self, *args, **kwargs):
        """Suitable for querys to instruments that return a single value int.

        Returns:
            int: integer.
        """
        return int(self.query(*args, **kwargs))

    def query_bool(self, *args, **kwargs):
        """Suitable for querys to instruments that return a '0' or '1' or '+1'.

        Returns:
            bool: True or False, via int.
        """
        return bool(int(self.query(*args, **kwargs)))

    def write_list(self, commands, **kwargs):
        """Write a list of commands to the instrument.

        Args:
            commands (list): list of commands.
                eg: ['command1', 'command2', '...']

        """
        for command in commands:
            self.write(command, **kwargs)

    @property
    def _listcommands(self):
        """List commands that the driver provides."""
        system = [
            'inst', 'query', 'write',
            'query_float', 'query_int',
            'query_binary_values',
            'write_binary_values',
            'CLS', 'ESE', 'ESR', 'IDN', 'OPC',
            'OPT', 'PSC', 'RCL', 'RST', 'SAV',
            'SRE', 'STB', 'TRG', 'TST', 'WAI'
        ]
        return [x for x in dir(self) if not x.startswith('_') and x not in system]
