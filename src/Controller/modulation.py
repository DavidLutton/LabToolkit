class Modulation():

    # Modulation('AM', rate=1000, depth=80)
    # Modulation('FM', deviation=5e3, rate=1e3)
    # Modulation('Pulse', rate=217)

    def __init__(self, modulation, *, rate, depth=None, deviation=None, on_time=None, off_time=None, shape=None, enable=None, dontpresetmodulation=None):
        if modulation is None:
            raise Exception('Modulation must not be None')
        else:
            self.modulation = modulation

        self.dontpresetmodulation = dontpresetmodulation

        if enable is None:
            self.enable = True
        else:
            self.enable = enable

        if modulation == 'AM':
            if depth is None or rate is None:
                raise Exception('depth or rate must not be None')

            self.depth = depth
            self.rate = rate
            if shape is None:
                self.shape = 'Sine'

        if modulation == 'FM':
            if deviation is None or rate is None:
                raise Exception('deviation or rate must not be None')

            self.deviation = deviation
            self.rate = rate
            if shape is None:
                self.shape = 'Sine'

        if modulation == 'Pulse':
            if rate is None:
                raise Exception('rate must not be None')
            if rate is not None:
                self.rate = rate
                self.shape = 'Square'

                # on_time / off_time

    def __repr__(self):
        if self.modulation == 'AM':
            return f'AM Depth {self.depth}%, Audio {self.rate}Hz, Shape {self.shape}'
        elif self.modulation == 'FM':
            return f'FM Deviation {self.deviation}Hz, Audio {self.rate}Hz, Shape {self.shape}'
        elif self.modulation == 'Pulse':
            return f'Pulse Rate {self.rate}Hz, Shape {self.shape}'

# sg.modulation = Modulation('AM', rate=1000, depth=80)
# sg.modulation = Modulation('FM', deviation=100e3, rate=1e3)