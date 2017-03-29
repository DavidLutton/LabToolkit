import random

def cf():
    while True:
        val = yield
        print(val),

def pf(c):
    while True:
        val = random.randint(1,10)
        c.send({ x : 8,})
        yield

if __name__ == '__main__':
    c = cf()
    c.send(None)
    print(c)
    p = pf(c)

    for wow in range(10):
        o = next(p)

'''def f():
    while True:
         val = yield
         yield val*10

g = f()

print(next(g))
g.send(1)

print(next(g))
g.send(10)

print(next(g))
g.send(0.5)
print(next(g))
print(next(g))
'''
