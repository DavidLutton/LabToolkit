def steps(points):
    for step in points:
        yield(step)

listofsteps = [100e3, 300e3, 1e6, 3e6, 10e6, 30e6, 50e6, 100e6]

numberofsteps = len(listofsteps)
print(numberofsteps)
print()

stepper = steps(listofsteps)

step = next(stepper)  # First step
print(step)  # 100000.0
print()

step = next(stepper)  # Second step
print(step)  # 300000.0
print()


for step in stepper:  # Remaining steps
    print(step)
