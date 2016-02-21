#! /usr/bin/python
# -*- coding: utf-8 -*-

import random
import os
import shutil

HEIGHT = 100
WIDTH = 100

OVERLAP = 5

ALLWIDTH = WIDTH*2-OVERLAP
ALLHEIGHT = HEIGHT*2-OVERLAP

AGENTSIZE = 3000

PROB_INFECTION = 80

INFECTION_TERM = 10

map = [[[] for i in range(ALLHEIGHT+1)] for j in range(ALLWIDTH+1)]

def isOnMap(x, y):
    if x < 0: return False
    if y < 0: return False
    if x > ALLWIDTH: return False
    if y > ALLHEIGHT: return False
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
    if prob == 0: return False
    if uniform(0, 100) <= prob: return True
    else: return False


# @class agent
class agent(object):
    """ Agent class """
    def __init__(self, originx, originy):
        self.x = 0
        self.y = 0
        self.has_immunity = False
        self.is_infection = False

        self.infection_term = 0

        self.originx = originx
        self.originy = originy

        self.randomset()

    def isInRegion(self, x, y):
        if x < self.originx: return False
        if y < self.originy: return False
        if x > WIDTH+self.originx: return False
        if y > HEIGHT+self.originy: return False
        return True

    def gainX( self, dis ):
        self.x += dis
    def gainY( self, dis ):
        self.y += dis

    def move(self):
        destx = self.x
        desty = self.y

        if bool(): destx += sign()
        if bool(): desty += sign()

        if self.isInRegion(destx, desty):
            self.setPoint(destx, desty)

    def setPoint(self, x, y):
        map[self.y][self.x].remove(self)
        self.x = x
        self.y = y
        map[self.y][self.x].append(self)


    def randomset(self):
        self.x = randint(0, WIDTH-1)
        self.y = randint(0, HEIGHT-1)
        self.gainX( self.originx )
        self.gainY( self.originy )

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
        if self.infection_term > INFECTION_TERM:
            self.has_immunity = True
            self.is_infection = False

if __name__ == "__main__":
    agents = []

    # initialize
    for i in range(AGENTSIZE):
        agents.append( agent(0, 0) )
    for i in range(AGENTSIZE):
        agents.append( agent(0, HEIGHT-OVERLAP) )
    for i in range(AGENTSIZE):
        agents.append( agent(WIDTH-OVERLAP, HEIGHT-OVERLAP) )
    for i in range(AGENTSIZE):
        agents.append( agent(WIDTH-OVERLAP, 0) )

    for a in agents:
        map[a.y][a.x].append(a)

    # initiate infection
    initiate = False
    for iy in range(HEIGHT):
        if initiate == True: break
        for jx in range(WIDTH):
            a = map[iy][jx]
            if len(a) > 0:
                a[0].infect()
                initiate = True
                break

    if os.path.exists('data'):
        shutil.rmtree('data')
    os.mkdir('data')
    foinfection = file('data/infection.txt', 'w')
    foimmunity = file('data/immunity.txt', 'w')
    fosusceptible = file('data/susceptible.txt', 'w')

    step = 0
    while(True):
        step += 1
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

        foinfection.write('%d %d\n' % (step, infection_size))
        foimmunity.write('%d %d\n' % (step, immunity_size))
        fosusceptible.write('%d %d\n' % (step, len(agents)-infection_size-immunity_size))

        fomap = file('data/map-%d.txt'%step, 'w')
        for y in range(ALLHEIGHT):
            for x in range(ALLWIDTH):
                fomap.write('%d %d %d\n'%(x, y, len(map[y][x])))
            fomap.write('\n')

        fomap = file('data/infection-map-%d.txt'%step, 'w')
        for y in range(ALLHEIGHT):
            for x in range(ALLWIDTH):
                infsize = 0
                for a in map[y][x]:
                    if a.isInfection(): infsize += 1
                fomap.write('%d %d %d\n'%(x, y, infsize))
            fomap.write('\n')


        print step, infection_size, immunity_size

        if infection_size == 0:
            break;
