"""."""

from datetime import datetime as dt


class SCPI(object):
    """SCPI helper functions."""
    
    @property
    def SCPI_OPT(self):
        return self.query(':SYSTem:OPTions?').strip('"').split(',')
    
    @property
    def SystemErrorQueue(self):
        """Get System Error Queue.

        :returns: List of errors
        """
        responces = []

        i, s = self.inst.query_ascii_values(':SYSTem:ERRor?', converter='s')
        responce = [int(i), s.strip('"')]

        while responce[0] != 0:
            responces.append(responce)
            i, s = self.inst.query_ascii_values(':SYSTem:ERRor?', converter='s')
            responce = [int(i), s.strip('"')]

        if len(responces) == 0:
            return None
        else:
            return responces

    
    def SCPI_local(self):
        """Go To Local."""
        return self.query_float(':SYSTem:COMMunicate:GTLocal?')
    
    def clock_update(self):
        now = dt.now()
        
        self.write(f':SYSTem:DATE {now.year},{now.month},{now.day}')
        self.write(f':SYSTem:TIME {now.hour},{now.minute},{now.second}')