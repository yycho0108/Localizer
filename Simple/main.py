#!/usr/bin/python

import cv2
import numpy as np

## KEY DEFINITIONS

LEFT = 65361
UP = 65362
RIGHT = 65363
DOWN = 65364

## PROBABILITY DEFINITIONS

move_success = 0.7

#sensor_accurate = 0.8 -- ??

## BUILD MAP

#W = 128
#H = 128
#world = np.reshape((np.random.rand(3*W*H)*256).astype(np.uint8),(H,W,3))
#world[world > 255] = 255

## LOAD MAP

world = cv2.imread('images/map.png')
world = cv2.resize(world,(128,128))
H,W = world.shape[:-1]

## PLACE ROBOT
p = np.full((H,W),1./(W*H),dtype=np.float64)

X,Y = np.random.choice(range(W)), np.random.choice(range(H))

cv2.namedWindow('world')
cv2.namedWindow('prob')

cv2.moveWindow('world',128 + 0, 128 + 0)
cv2.moveWindow('prob',128 + 256, 128 + 0)

cv2.imshow('world', cv2.resize(world,(256,256)))
cv2.imshow('prob',cv2.resize(p,(256,256)))


def dot3(a,b):
    res = 0.
    for aa,bb in zip(a,b):
        res += float(aa)*float(bb)
    return res / np.linalg.norm(a)/np.linalg.norm(b)

def shift(p,dx,dy):
    dx = -dx
    dy = -dy
    p = np.hstack((p[:,dx:],p[:,:dx]))
    return np.vstack((p[dy:,:],p[:dy,:]))

def localize(m_color,dx,dy):
    # m_color = measured color
    global p,world
    # move
    p = (1.0 - move_success) * p + move_success * shift(p,dx,dy)
    # sense - calculate similarity

    for idx in np.ndindex(p.shape):
        p[idx] *= dot3(world[idx],m_color)

    #s = [[dot3(w_color,m_color) for w_color in row] for row in world]
    #p *= s
    # normalize
    p /= np.sum(p)


while True:
    key = cv2.waitKey(3)
    if key == 27:
        break
    elif key == -1:
        continue
    dx,dy = (key == RIGHT) - (key == LEFT), (key == DOWN) - (key == UP)

    if dx==0 and dy==0: # disallow not moving
        continue

    if(np.random.random() < move_success):
        X += dx
        Y += dy
        X %= W
        Y %= H

    img = cv2.circle(world.copy(),(X,Y),3,(255,255,255),thickness=-1)
    localize(world[Y,X],dx,dy) 
    guess = np.unravel_index(p.argmax(),p.shape)

    print "GUESS : " ,guess, p[guess]
    print "COR : " ,(Y,X), p[Y,X]

    p_img = p / p[guess]
    #p_img = cv2.circle(p.copy(),(guess[1],guess[0]),3,(255,255,255),thickness=-1)
    #p_img = p.copy()

    cv2.imshow('world', cv2.resize(img,(256,256)))
    cv2.imshow('prob', cv2.resize(p_img,(256,256)))
