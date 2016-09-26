import numpy as np
from matplotlib import pyplot as plt

WHITE = (255,255,255)
BLACK = (0,0,0)

def noise(v):
    return np.random.randn(*v.shape)

def colvec(*args):
    return np.atleast_2d(args).T

def dot(*args):
    lhs = args[0]
    for rhs in args[1:]:
        lhs = np.dot(lhs,rhs)
    return lhs

dt = 0.3 # delta time

F = np.identity(4)

F[0][2] = F[1][3] = dt # px += vx*dt, py += vy*dt
F[2][2] = F[3][3] = 0.99 # Velocity decreases

G = np.asarray([ # Converts acceleration Commands
            [0.,0.],
            [0.,0.],
            [dt,0.],
            [0.,dt]
            ])

H = np.atleast_2d([[0., 0.,1.,0.],[0.,0.,0.,1.]]) # measurement function --> measures vx, vy

# def F(x):
#     global dt
#     x_2 = x.copy()
#     x_2[0] += dt * x_2[2] # px += vx
#     x_2[0] += dt * x_2[3] # py += vy
#     return x_2
# 
#    return lhs
# 

def predict(x,P,u):
    global F, G
    # F = Next State Function
    # x = system input
    # G = system processing
    # u = commands (velocity input), external motion
    # P = Confidence (probability)
    # Q = Noise Covariance
    x = dot(F,x) + dot(G,u) 
    P = dot(F,P,F.T) # + Q

    return x,P

def update(x,P,y):
    global H
    # W = measurement uncertainty covariance
    # R = "WEIGHT" of sensor estimate belief
    # y = measurement

    v = y - dot(H,x) # error
    print v
    S = dot(H,P,H.T) # + W
    R = dot(P,H.T,np.linalg.pinv(S))
    x = x + dot(R,v)
    P = P - dot(R,H,P)

    return x,P


import pygame
from pygame.locals import *

def draw(screen, pos):
    screen.fill(WHITE)
    pygame.draw.rect(screen,BLACK,(pos[0,0],pos[1,0],5,5))

def get_command():
    u = colvec(0,0)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if key[K_DOWN]:
                u[1,0] = 1.0 # Y-accel
            elif key[K_UP]:
                u[1,0] = -1.0
            elif key[K_LEFT]:
                u[0,0] = -1.0 # X-accel
            elif key[K_RIGHT]:
                u[0,0] = 1.0
    return u

def main():
    x = colvec(100.,100.,0.,0.) # initially at (0,0) with velocity (0,0)
    x_real = colvec(100.,100.,0.,0.) # real x

    P = 1000 * np.identity(4) # Uncertainty, error covariance matrix

    W = 200
    H = 200

    u = colvec(0,0) #command: acceleration

    y = colvec(0,0) #measurement: velocity

    ## RUNNING

    pygame.init()
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption('EKF Demo')

    while True:
        #y = x[2:].copy()
        x,P = update(x,P,y) # y = measurement -- measures velocity

        u = get_command() 

        x,P = predict(x,P,u) # u = command -- commands acceleration

        draw(screen, x)
        pygame.display.update()
        pygame.time.wait(50) # wait 500 ms

if __name__ == "__main__":
    main()
