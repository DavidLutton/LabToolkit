from ..IEEE488 import IEEE488


class VoltechPM1000P(IEEE488):

    # inst = rm.open_resource('GPIB1::13::INSTR', read_termination='\n', write_termination='\n')  # , , **kwargs)
    def Measurement(self):
        Hz = float(self.query(':FNC:FRQ?'))
        V = float(self.query(':FNC:VLT?'))
        return V, Hz
