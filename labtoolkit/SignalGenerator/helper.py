class SignalGenerator():
    """."""

    def __init__(self):
        self._amplitudelimit = 0.0

    def safe(self):
        """Make safe the SignalGenerator."""
        self.output = False
        self.amplitude = min(self._amplitudes)
        self.frequency = min(self._frequencies)

    def state(self):
        """Report basic paramaters."""
        print(f"Amplitude: {self.amplitude}")
        print(f"Frequency: {self.frequency}")
        print(f"Output: {self.output}")

    def start(self, lvl=-50):
        """."""
        self.amplitude = lvl

    '''def ampsetter(self, targetlevel):
        if (self.amplitude - 10) <= targetlevel <= (self.amplitude + 3):
            self.amp(targetlevel)
        else:
            before = str(self.amplitude)  # self.log.warn("on " + self.IDN + " amp change limits, set" + str(self.amplitude))
            if (self.amplitude - 10) >= targetlevel:
                self.amp((self.amplitude - 10))
            if (self.amplitude + 3) <= targetlevel:
                self.amp((self.amplitude + 3))
            self.log.warn("on " + self.IDN + " amp change limits, set " + str(self.amplitude) + " from " + before)

    def freqsetter(self, freq):
        if self.frequency != freq:  # prevent resubmitting request to set the same frequency

            self.write(freq)
            self.frequency = freq
            time.sleep(.3)  # after retuneing wait time for settling
    '''


class amplitudelimiter():
    """Class to limit upper amplitude value applied to a SignalGenerator.

    Applied by decorator @amplitudelimiter
    """

    def __init__(self, f, *args, **kwargs):
        """If there are no decorator arguments, the function to be decorated is passed to the constructor."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")
        self.f = f

    def __call__(self, f, *args, **kwargs):
        """The __call__ method is not called until the decorated function is called."""
        # print(f)  # object
        # print(*args)  # set point
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint > f._amplitudelimit:
            # f.log.warn
            print(f"Amplitude limit ({f._amplitudelimit}) reached with setpoint ({setpoint}) on {f.inst}")
            # self.f(f, f._amplitudelimit)  # set amplitude to _amplitudelimit
            f.amplitude = f._amplitudelimit
        else:
            self.f(f, *args)
        # print("After self.f(*args)")
