
# from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488


class HP437B(IEEE488):
    """HP 437B.

    .. figure::  images/PowerMeter/HP437B.jpg
    """

    def __init__(self, inst):
        super().__init__(inst)
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        # self.__preset__()

    def preset(self):
        """."""
        # self.message("")
        # self.log.info(f"Get {self.engineering_project.resource_name} to known state")
        self.correctionfactor(100.0)
        self.rangeauto()
        self.unitslog()  # Log units dBM/dB
        # self.rangehold(self):  # RH Range hold
        # self.rangemanual(self, ranger)
        # self.write("RM{}".format(ranger))

        # self.lin():  # Linear units (Watts/%)
        self.zero()

    def discover(self):
        """."""
        decodeTHISARRAY = self.query("LP2")  # TODO

    def measure(self):
        """."""
        measure = float(self.query("?"))
        if measure is not 9e40 and measure is not 9.0036e40:
            return measure

    def message(self, message=None):
        """."""
        if message is not None and len(message) <= 12:
            self.write("DU" + message.rjust(12))
        else:
            self.write("DE")

    def displayread(self):
        """."""
        pass  # OD

    def key(self, key):
        """."""
        dispatch = {
            "Up": "UP",  # Up arrow key
            "Down": "DN",  # Down arrow key
            "Left": "LT",  # Left arrow key
            "Right": "RT",  # Right arrow key
            "Enter": "EN",  # Enter key
            "Exit": "EX",  # exit function
            "Preset": "PR",
            "Special": "SP",
            "Zero": "ZE",
        }
        # print(dispatch[key])  # PowerMeter[0].key("Left")
        self.write(dispatch[key])

    # def display(self, key):
    # DD display disable
    #    DE display enable
    #    DF display enable
    #    DU display user message

    # print(dispatch[key])  # PowerMeter[0].key("Left")
    # self.engineering_project.write(dispatch[key])

    def zero(self):
        """."""
        self.write("CS;ZE")

    def calibrate(self, factor=100.0):
        """."""
        self.write(f"CS;CL{factor}EN")

    def correctionfactor(self, factor=100.0):
        """."""
        self.write(f"KB{factor}EN")  # KB enter measurement cal factor

    def statusmessage(self):
        """."""
        status = self.query("SM")
        #  $Message[5,6] = “06” Wait until zero completes (06 means zeroing)
        #  $Message[5,6] = ! Wait until cal completes (08 means calibrating
        return(status)

    def rangeauto(self):
        """."""
        self.write("RA")

    def rangehold(self):  # RH Range hold
        """."""
        self.write("RH")

    def rangemanual(self, range):
        """."""
        self.write("RM")

    def lin(self):  # Linear units (Watts/%)
        """."""
        self.write("LN")
        self.units = "W"

    def unitslog(self):  # Log units dBM/dB
        """."""
        self.write("LG")
        self.units = "dBm"


'''
*CLS Clear all status registers
CS clear the status byte
CT clear sensor type
DA All display segments on
DC0 Duty cycle off
DC1 Duty cycle on

DY enter duty cycle
ERR? Device error query
*ESR? Event status register query
*ESE Set event status register mask
*ESE? event status register mask query
ET Edit sensor table
FA automatic filter selection
FH filter hold
FM Manual filter selection
FR enter measurement frequency
GT0 ignore GET bus command
GT1 Trigger immediate response to get
GT2 Trigger with delay response to get
GZ Gigaherz
HZ Hertz

KZ kilohertz
LH enter high Limit
LL Enter low Limit
LM0 disable limits checking
LM1 enable limits checking

LP2 learn mode
MZ megahertz
OC0 reference oscillator off
OC1 reference oscillator on
OD output display
OF0 offset off
OF1 offset on
OS offset Value
PCT Percent

RA Auto range
RC recall instrument configuration
RE Set display resolution
RF Enter sensor table reference alibration factor
RL0 exit from relative mode
RL1 Enter relative mode (take new reference)
RL2 Enter relative mode (use last reference)
RM Set measurement range
*RST reset
RV Read service request mask
SE Select sensor calibration table
SM  Status message
SN Enter sensor identification/serial number

*SRE Set the service request mask
*SRE? Service request mask query
ST Store (save) power meter configuration
*STB? Read status byte
TR0 trigger hold
TR1 trigger immediate
TR2 trigger with delay
*TST? self test query

@1 Prefix for status mask
@2 Learn mode prefix
% Percent
'''