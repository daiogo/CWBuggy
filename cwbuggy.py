#!/usr/bin/env python3

import remote
import vehicle

print("Starting CWBuggy...")

# Instantiate vehicle
vehicle = vehicle.Vehicle()

# Instantiate remote controller
rc = remote.Remote(vehicle)
rc.start()

# Instantiate autopilot
#auto = autopilot.Autopilot(vehicle)
#auto.start()

print("Finishing CWBuggy...")
# Free resources
del vehicle     
del rc
print("Finished CWBuggy")
