import random
import curses
from curses import wrapper
import math
import sys

T = 10
if (len(sys.argv) == 2):
    T = float(sys.argv[1])
def print_map(m):
    for i in range(0, len(m)):
        output = ""
        for j in range(0, len(m[i])):
            if (m[i][j] == -1):
                output = output + "v"
            elif (m[i][j] == 1):
                output = output + "^"
        print(output)

def get_potential(m):
    pot = 0
    for i in range(0, len(m)):
           for j in range(0, len(m[i])):
                se = m[i][j]
                if (i > 0):
                    lex = i - 1
                else:
                    lex = len(m) - 1
                if (i < len(m) - 1):
                    mex = i + 1
                else:
                    mex = 0
                if (j > 0):
                    ley = j - 1
                else:
                    ley = len(m[i]) - 1
                if (j < len(m[i]) - 1):
                    mey = j + 1
                else:
                    mey = 0
                if (se == m[lex][j]):
                    pot = pot - 2
                if (se == m[mex][j]):
                    pot = pot - 2
                if (se == m[i][ley]):
                    pot = pot - 2
                if (se == m[i][mey]):
                    pot = pot - 2
                pot = pot + 4
    return pot

def single_change_pot(m, i, j, pot):
    # Pot before is pot. We change x, y.
    # So we just need to work out the contribution of 
    # that point as it is to the potential, and then change it.
    impact_before = 0
    impact_after = 0
    
    se = m[i][j]
    if (i > 0):
        lex = i - 1
    else:
        lex = len(m) - 1
    if (i < len(m) - 1):
        mex = i + 1
    else:
        mex = 0
    if (j > 0):
        ley = j - 1
    else:
        ley = len(m[i]) - 1
    if (j < len(m[i]) - 1):
        mey = j + 1
    else:
        mey = 0



    impact_before = 4
    if (m[i][j] == m[mex][j]):
        impact_before = impact_before - 2
    if (m[i][j] == m[lex][j]):
        impact_before = impact_before - 2
    if (m[i][j] == m[i][ley]):
        impact_before = impact_before - 2
    if (m[i][j] == m[i][mey]):
        impact_before = impact_before - 2
    pot = pot - impact_before
    impact_after = -impact_before
    pot = pot + 3*impact_after
    return pot


def ising_ch(n):
    if (n == -1):
        return "^"
    return "v"

def witch(stdscr):
    stdscr.clear()
    curses.cbreak()
    stdscr.nodelay(True) # This means that when we later call getch() in the
                         # loop it won't hang.
    curses.noecho()
    stdscr.timeout(0)
    height,width = stdscr.getmaxyx()
    ising_map = []
    for i in range(0, height - 2):
        ising_map.append([])
        for j in range(0, width-1):
            ising_map[i].append((random.randint(0, 1) - 0.5)*2)
    
    for i in range(0, len(ising_map)):
        for j in range(0, len(ising_map[i])):
            stdscr.addstr(i+1, j, ising_ch(ising_map[i][j]))

    current_potential = get_potential(ising_map)
    n = 0
    c = 0
    new_potential = 0
    while(current_potential != new_potential or n < 5000):
        x = random.randint(0, len(ising_map)-1)
        y = random.randint(0, len(ising_map[x])-1)
        if (c == 0):
            n = n + 1
        else:
            n = 0
        c = 0
        new_potential = single_change_pot(ising_map, x, y, current_potential)
        if (new_potential < current_potential or random.randint(1, 10000) < 10000*math.exp(-(new_potential - current_potential)/(T))):
            c = 1
            current_potential = new_potential
            ising_map[x][y] = -ising_map[x][y]
            stdscr.addstr(0, 0, "Potential is %d" % (current_potential))
            for i in range(0, len(ising_map)):
                for j in range(0, len(ising_map[i])):
                    stdscr.addstr(i+1, j, ising_ch(ising_map[i][j]))
                    stdscr.refresh()
            s = 0
            for i in ising_map:
                for j in i:
                    s = s + j
            stdscr.addstr(0, 20, "Moment: %d" % (s))

            
        if (i == 50):
            if (current_potential != get_potential(ising_map)):
                print("Fuck")
    print("\n\n\n")
    print_map(ising_map)
    
wrapper(witch)



