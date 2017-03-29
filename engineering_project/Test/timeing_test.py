#!/usr/bin/env python3

from timeit import default_timer as timer

import time
import ETA


EstimatedTime = ETA.estimatedtime(10)
# EstimatedTime.append(10)
# EstimatedTime.append(19)


# start = timer()
# time.sleep(1)  # Settling time
# EstimatedTime.append(timer() - start)  # end - start
EstimatedTime.append(3)
EstimatedTime.append(3)
EstimatedTime.append(3)
EstimatedTime.append(2)
EstimatedTime.append(2)
print("ETA: " + str(EstimatedTime.ETA()) + " s")
