"""."""

class AmplitudeLimiter(object):
    """."""

    def __init__(self, f, *args, **kwargs):
        """If thereareno decorator args the function tobe decorated is passed to the constructor."""
        # print(f)
        # print(*args)
        # print(**kwargs)
        # print("Inside __init__()")

        self.f = f

    def __call__(self, f, *args, **kwargs):
        """The __call__ method is not called until the decorated function is called."""
        # print(f)
        print(*args)
        # print(**kwargs)
        # print("Inside __call__()")
        setpoint = float(*args)
        if setpoint > f.amplimit:
            f.log.warn(
                "Amplimit ({}) reached with setpoint ({}) on {}"
                .format(f.amplimit, setpoint, f.instrument))
        else:
            self.f(f, *args)
        # print("After self.f(*args)")
