
class HeraeusVotsch(object):

    def __post__(self):
        self.inst.read_termination='\r\n'
        self.inst.write_termination='\r\n'
        # self.inst.timeout = 6000

    def write(self, string):
        # self.inst.write(string)
        print(string)

    def query(self, string):
        return self.inst.query(string)
        # return 'U1 = 0618 mV  U2 = 0000 mV  ERR = 4'

    @property
    def state(self):  # 'U1 = 0618 mV  U2 = 0000 mV  ERR = 4'
        resp = self.query('?').replace('  ', ',').split(',')
        state = {}
        for each in resp:
            if each.startswith('U1') and each.endswith('mV'):
                U1mV = int(each.split(' ')[2])
                state['U1'] = round((U1mV/10)-50, 1)
            if each.startswith('ERR'):
                state['ERR'] = int(each.split(' ')[2])
        return state

    @property
    def temperature(self):
        """."""
        return self.state['U1']

    @temperature.setter
    def temperature(self, temperature):
        mV = int((temperature+50)*10)
        self.write('U1 = {:04d} mV'.format(mV))  # U1 = 1234 mV

    @property
    def enable(self):
        if self.state['ERR'] == 0:
            return True
        else:  # ERR == 4 is not enabled state
            return False

    @enable.setter
    def enable(self, state=False):
        if state is False:
            self.write('R00000000')  # Disable
        elif state is True:
            self.write('R00000001')  # Enable


# rm = visa.ResourceManager('')

# oven = HeraeusVotsch(rm, 'GPIB1::15::INSTR')
'''

print(oven.state)
print(oven.temperature)
print(oven.enable)

setpoint = -20
oven.enable = True
oven.temperature = setpoint

# Get to temperature and stay there for 1 hour
while abs(oven.temperature - setpoint) > 1:
    print(f'Currently {oven.temperature} degC, with setpoint {setpoint}')
    time.sleep(10)
finally:
    time.sleep(3600)
    oven.enable = False
'''
# Task 208
'''
(name "convert to mV")
(expr 1 "(A+50)*10"))

(name "convert to deg C")
(expr 1 "(A/10)-50"))

(name "newInstrument2 (unknown @ 715)")
(transactions 3 "WRITE TEXT \"U1 = \"" "WRITE TEXT a" "WRITE TEXT \" mV\" EOL"))

(name "newInstrument2 (unknown @ 715)")
(transactions 3 "WRITE TEXT \"?\" EOL" "WAIT INTERVAL:0.1" "READ TEXT x STR"))


1. After switch on check RDY and ON LEDs solid on.
2. Ensure IEC bus switch is on (depressed). This is the one with the 'whirlwind' symbol. When on, the whirlwind green LED should flash.
3. Ensure tempering switch is on (depressed). This is the switch on the LHS; thermometer with circular arrows around it.
4.
    Not sure if the fixed value switch, looks like 5 fingers or a rake, position matters.
    You can read current temperature (U1) by sending talk command '?' and reading the string sent back.
    You can switch the temperature ramp on by sending 'R00000001', which turns the 1st relay on.
    The whirlwind LED should go solid as well as the other applicable controller status LEDs.
    You can then change temperature setting by writing U1 = xxxx mV
    0mV is -50deg C; 700mV is +20deg C; 3000mV is +250deg C.
    I.e. 10mV per deg C from -50
    For cooling check M1 LED lit, for heating check E2 LED lit.
'''
