import numpy as np
from matplotlib import pyplot as plt

# TODO : implement move()
def move(world, ps, d):
    pass

def measure(world, ps):
    # likelihood of p being true position 
    return p # more likely as p gets 

def wheel(ps,ws): # resampling wheel
    # return resampled p
    N = len(ps)
    idx = np.random.choice(N) # initial starting index
    beta = 0.
    maxws = 2.*max(ws)

    ps_new = []
    for _ in range(N):
        beta += np.random.random() * maxws
        while beta > ws[idx]:
            beta -= ws[idx]
            idx = (idx+1) % N
        ps_new.append(ps[idx])
    return ps_new

def main():
    N = 10

    ps = np.random.uniform(size=N) # randomly selected particles over world
    ws = [None for _ in range(N)] # equal probability (not strictly true)

    for _ in range(1000): # iterations
        ps = move(ps)
        ws = [measure(p) for p in ps] # reevaluate weights
        ps = wheel(ps,ws)

    plt.plot(ps)
    plt.show()

if __name__ == "__main__":
    main()
