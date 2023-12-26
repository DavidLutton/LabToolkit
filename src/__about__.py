
from datetime import datetime as dt
from datetime import timedelta as td 

now = dt.now() - td(days=365*2024)

__version__ = f"{now:%Y.%m%d.%H%M%S}"