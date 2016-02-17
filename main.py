#! /usr/bin/python
# -*- coding: utf-8 -*-

import random

HEIGHT = 50
WIDTH = 50

AGENTSIZE = 1000

PROB_INFECTION = 10

map = [[[] for i in range(HEIGHT)] for j in range(WIDTH)]

def isOnMap(x, y):
    if x < 0: return False
    if y < 0: return False
    if x >= WIDTH: return False
    if y >= HEIGHT: return False
    return True

def uniform(a, b):
    return random.uniform(a, b)

def randint(a, b):
    return random.randint(a, b)

def bit():
    return random.randint(0, 1)

def bool():
    if bit() == 0: return True
    else: return False

def sign():
    if bool(): return -1
    else: return 1

def probability( prob ):
    if uniform(0, 100) < prob: return True
    else: return False

class agent(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.has_immunity = False
        self.is_infection = False
        self.randomset()

        self.infection_term = 0

    def gainX( self, dis ):
        self.x += dis
    def gainY( self, dis ):
        self.y += dis
    def move(self):
        if bool(): self.gainX( sign() )
        if bool(): self.gainY( sign() )

    def randomset(self):
        self.x = randint(0, WIDTH-1)
        self.y = randint(0, HEIGHT-1)

    def neighbors(self):
        ret = []
        for jx in [self.x,self.x-1,self.x+1]:
            for iy in [self.y,self.y-1,self.y+1]:
                if isOnMap(jx,iy) == False: continue
                for a in map[iy][jx]:
                    if a == self: continue
                    ret.append(a)
        return ret

    def isInfection(self):
        return self.is_infection
    def hasImmunity(self):
        return self.has_immunity

    def infect(self):
        if self.has_immunity == True: return
        self.is_infection = True

    def proceed(self):
        if self.isInfection():
            self.infection_term += 1
        if self.infection_term > 20:
            self.has_immunity = True
            self.is_infection = False

if __name__ == "__main__":
    agents = []

    # initialize
    for i in range(AGENTSIZE):
        agents.append( agent() )
    for a in agents:
        map[a.y][a.x].append(a)

    # initiate infection
    agents[0].infect()

    foinfection = file('infection.txt', 'w')
    foimmunity = file('immunity.txt', 'w')
    for i in range( 100 ):

        # move
        for a in agents:
            a.move()

        # infect
        for a in agents:
            if a.isInfection():
                for n in a.neighbors():
                    if probability( PROB_INFECTION ):
                        n.infect()

        for a in agents:
            a.proceed()

        # output
        infection_size = 0
        immunity_size = 0
        for a in agents:
            if a.isInfection(): infection_size += 1
            if a.hasImmunity(): immunity_size += 1
        print i, infection_size

        foinfection.write('%d %d\n' % (i, infection_size))
        foimmunity.write('%d %d\n' % (i, immunity_size))
