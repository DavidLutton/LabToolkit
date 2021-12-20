import abc
import logging

from pyvisa.constants import VI_GPIB_REN_ADDRESS_GTL


class Instrument(metaclass=abc.ABCMeta):
    """Wrap an instrument resource with some utility functions."""

    def __repr__(self):
        return f'{self.__module__} on {self.inst.resource_name}'

    def __init__(self, instrument):
        self.inst = instrument
        self.logger = logging.getLogger(f'{self.__module__}')
        # The instrument __module__ name is used, rather than Instrument

        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        # self. = self.inst.
        self.__post__()
        
    def __post__(self):  
        # https://discuss.python.org/t/add-a-post-method-equivalent-to-the-new-method-but-called-after-init/5449/2
        None
    
    def write(self, *args, **kwargs):
        """Wrap write to log it.."""
        self.logger.info(*args)
        return self.inst.write(*args, **kwargs)

    def query(self, *args, **kwargs):
        """Wrap query to log it."""
        self.logger.info(*args)
        responce = self.inst.query(*args, **kwargs)
        self.logger.info(f'Read {responce}')
        return responce
    
    def query_ascii_values(self, *args, **kwargs):
        """Wrap query_ascii_values to log it."""
        self.logger.info(*args)
        return self.inst.query_ascii_values(*args, **kwargs)
        # self.logger.info(f'{responce}')
        # return responce
    
    def query_binary_values(self, *args, **kwargs):
        """Wrap query_binary_values to log it."""
        self.logger.info(*args)
        return self.inst.query_binary_values(*args, **kwargs)
        # self.logger.info(f'{responce}')
        # return responce
        
    def write_binary_values(self, *args, **kwargs):
        """Wrap write_binary_values to log it."""
        self.logger.info(f'Write binary {args[0]}')
        return self.inst.write_binary_values(*args, **kwargs)

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
