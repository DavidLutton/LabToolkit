from ..Instrument import Instrument
from time import sleep


class VDIPM5B(Instrument):

    def __post__(self):
        inst.read_termination = ''
        inst.write_termination = ''
        inst.query_delay = 0.05
        
    def command_padding(self, cmd):
        nulls = b'\x00'
        end = b'\x0d'
        pads = 7 - len(cmd) 
        command = cmd.encode() + nulls * pads + end
        return command

    def query(self, cmd):
        self.inst.write_raw(self.command_padding(cmd))
        sleep(self.inst.query_delay)
        match cmd:
            case '?D1':
                he = self.inst.read_bytes(7)
            case _:
                he = self.inst.read_bytes(1)
        # print(he.hex())
        return he 