from ..IEEE488 import IEEE488


class VoltechPM1000P(IEEE488):

    # inst = rm.open_resource('GPIB1::13::INSTR', read_termination='\n', write_termination='\n')  # , , **kwargs)
    def get(self):
        Hz = float(inst.query(':FNC:FRQ?'))
        V = float(inst.query(':FNC:VLT?'))
        return v, Hz
