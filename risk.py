#Duncan Brown 12/29/2020
#Version 1.0
#Risk simulator

#TODO:
#   add option for turning off graph
#   add histogram functionality
#   make actual value of percents more clear (histogram might be the solution)
#   feature to discover extreme cases (find winning case in 100 v 50)

import random
import sys
from matplotlib import pyplot as plt
import seaborn as sns

#evaluates a blitz, returns remaining troops for both sides
#does not account for the 1 troop needed to garrison attacker's province
def blitz(nAtt, nDef, capital = False, verbose = False):
    if verbose:
        print("Attacking with " + str(nAtt) + " into " + str(nDef) + " (capital: " + str(capital) + ")")
    defMax = 2
    if capital:
        defMax = 3
    
    while nAtt > 0 and nDef > 0:
        if verbose:
            print("\t" + str(nAtt) + "(att) vs " + str(nDef) + "(def):")
        losses = battle(min(nAtt, 3), min(nDef, defMax), verbose)
        nAtt -= losses[0]
        nDef -= losses[1]
    
    if verbose:
        if nAtt == 0:
            print("\tDefenders victorious")
        else:
            print("\tAttackers victorious")
    
    return [nAtt, nDef]

#evaluates a single battle with any number of dice on either side, returns both side's losses
def battle(nAtt, nDef, verbose = False):
    #rolling dice & sorting rolls
    attRolls = [0] * nAtt
    defRolls = [0] * nDef
    
    for x in range(nAtt):
        attRolls[x] = random.randint(1, 6)
        
    for x in range(nDef):
        defRolls[x] = random.randint(1, 6)
        
    attRolls.sort(reverse = True)
    defRolls.sort(reverse = True)
    
    #comparing rolls (losses = [attLosses, defLosses])
    losses = [0, 0]
    
    for x in range(min(nAtt, nDef)):
        if attRolls[x] > defRolls[x]:
            losses[1] += 1
        else:
            losses[0] += 1
    
    if verbose:
        print("\t\tAttacker:\t" + str(attRolls))
        print("\t\tDefender:\t" + str(defRolls))
    
    return losses

#simulates a blitz <trials> number of times and returns a list of outcomes
def simulate(nAtt, nDef, trials, capital = False, verbose = False):
    results = [None] * trials
    
    for x in range(trials):
        if verbose:
            print("TRIAL " + str(x+1)+ ":")

        #progress bar
        elif x == (trials - 1):
            print("\rRunning simulation - Done  ")
        else:
            print("\rRunning simulation - " + "{0:.3}".format((x/trials)*100) + "%", end = "")

        results[x] = blitz(nAtt, nDef, capital, verbose)
    
    return results

#helper method designed to reorder the list of outcomes by attacker or defender rather than trial number
def restructure(ls):
    print("Restructuring data...", end = "")

    attL = [None] * len(ls)
    defL = [None] * len(ls)
    
    for x in range(len(ls)):
        attL[x] = ls[x][0]
        defL[x] = ls[x][1]

    attL.sort(reverse = True)
    defL.sort(reverse = True)
    
    print("Done.")
    
    return [attL, defL]

#main method
def main():
    capital = False
    verbose = False
    attP = 0.0
    defP = 0.0

    #input validation and help info
    if len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print("SYNTAX:\n\tpy risk.py <attacker> <defender> <trials> <options>\n\nIMPORTANT NOTE:\n\tThis program does not account for the fact that the attacker can only\n\tattack with one less troop than is in a stack.\n\t(If you are simulating 10 into 3, input 9 and 3 instead)\n\nOPTIONS:\n\tTo use options, simply string the letters to the corresponding options\n\tin any order and in either case as the 4th argument.\n\tExample using \'c\' and \'v\':\n\t\tpy risk.py 10 3 1000 cv\n\nOPTIONS LIST:\n\t\'c\' - gives the defender the extra die roll advantage\n\t\trecieved from being in a capital\n\t\'v\' - runs the program in verbose mode")
        return

    if len(sys.argv) < 4 or (not sys.argv[1].isdigit()) or (not sys.argv[2].isdigit()) or (not sys.argv[3].isdigit()) or len(sys.argv) > 5:
        print("Bad input. Try \'py risk.py help\' for more info")
        return
    
    if len(sys.argv) > 4:
        for c in sys.argv[4]:
            char = c.lower()
            if char == 'c':
                capital = True
                print("Succesfully set \'capital\' to True")
            elif char == 'v':
                verbose = True
                print("Successfully running in verbose mode")
            else:
                print("Unknown option \'" + char + "\'. Try \'py risk.py help\' for a list of options.")
                return

    #runs simulation
    nAtt = int(sys.argv[1])
    nDef = int(sys.argv[2])
    trials = int(sys.argv[3])

    results = restructure(simulate(nAtt, nDef, trials, capital, verbose))
    t = 0
    
    #computes percentages and truncates datasets to exclude losses
    for x in range(len(results[0])):
        t = x
        
        if results[0][x] == 0:
            break

    attP = (t/trials) * 100
    defP = ((trials - t)/trials) * 100
    
    results[0] = results[0][:t]
    results[1] = results[1][:(trials - t)]
    
    #plotting data with matplotlib and seaborn
    #density (kde) plot is used, other potential candidates include histograms or rugplots
    sns.set_style("whitegrid")
    sns.kdeplot(results[0], bw_method = 'scott', bw_adjust = 2, label = "Attackers")
    sns.kdeplot(results[1], bw_method = 'scott', bw_adjust = 2, label = "Defenders")
    plt.xlim(1, max(nAtt, nDef))
    plt.legend()
    
    plt.title("Attacking with " + str(nAtt) + " into " + str(nDef) + " (capital: " + str(capital) + ")\nAttacker victory percentage: " + "{0:.3}".format(attP) + "%\nDefender victory percentage: " + "{0:.3}".format(defP) + "%")
    plt.xlabel("Troops remaining")
    plt.ylabel("Density")
    
    plt.show()
    

if __name__ == "__main__":
    main()
