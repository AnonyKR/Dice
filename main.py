import random

# 4 turns per round (fourth turn is a boss) and finish 5 rounds to win
# each round you have 4 chances to play and 4 chances to reroll to get the score

def skipSpace(inputValue,counter):
    try:
        tempCount = counter
        while True:
            if inputValue[tempCount] != " ":
                return tempCount
            tempCount += 1
    except IndexError:
        return tempCount - 1
    
def inputReconize(inputValue):
    command = ""
    counter = skipSpace(inputValue, 0)
    if counter == len(inputValue):
        return [False,None,None]
    while True:
        if inputValue[counter] == " ":
            break
        command += inputValue[counter]
        counter += 1
        if len(inputValue) == counter:
            counter -= 1
            break
    perameter = []
    while True:
        counter = skipSpace(inputValue, counter)
        tempParameter = ""
        while True:
            if inputValue[counter] == " ":
                perameter.append(tempParameter)
                break
            tempParameter += inputValue[counter]
            if counter + 1 == len(inputValue):
                perameter.append(tempParameter)
                break
            counter += 1
        if counter + 1 == len(inputValue):
            break
    return [True, command, perameter]

class die():
    def __init__(self):
        self.eyes = [1,2,3,4,5,6]
        self.type = "normal"
        self.shown = None
        #types possible : normal, multi, buff

    def roll(self):
        self.shown = random.choice(self.eyes)
        return [self.shown,self.type]
    
    def reset(self):
        self.eyes = [1,2,3,4,5,6]
        self.type = "normal"
        self.shown = None

    def newRound(self):
        self.shown = None

    def newType(self,type):
        self.type = type

    def newEyes(self,eyes):
        self.eyes = eyes

    def showEye(self):
        #for display
        return self.shown
    
    def giveNumber(self):
        return self.shown
    
    def calculate(self, list):
        #list is [normal, multi, buff]
        if self.type == "normal":
            list[0] += self.shown
            print("[ +" + str(self.shown) + " X 0 ]")
        elif self.type == "multi":
            list[1] += self.shown
            print("[ 0 X +"+ str(self.shown) +" ] ")
        else:
            print("X" + str(self.shown) + "! (at the end)")
        return list
    
    def description(self):
        dieDescription = ""
        if self.type == "normal":
            dieDescription += "Normal Die: "
        elif self.type == "multi":
            dieDescription += "Multi Die : "
        else:
            dieDescription += "Buff Die  : "
        dieDescription += "D" + str(len(self.eyes)) + "  " + str(self.eyes)
        return dieDescription



class save():
    def __init__(self,comboIn):
        self.dice = []
        for x in range(0,5):
            self.dice.append(die())
        self.money = 0
        self.total = 0
        self.roundValue = 0
        self.round = 0
        self.roundGoal = 60
        self.play = 4
        self.rerollChances = 4
        self.comboIn = comboIn

    def newRound(self):
        self.play = 4
        self.rerollChances = 4
        self.roundValue = 0
        self.round += 1
        self.roundGoal *= 2

    def rollAll(self):
        for x in self.dice:
            x.roll()
    
    def showAllDice(self):
        self.temp = []
        for x in self.dice:
            self.temp.append(str(x.showEye()))
        return self.temp
    
    def collectNumbers(self):
        numbers = []
        for x in self.dice:
            numbers.append(x.giveNumber())
        return numbers
    
    def calculate(self):
        numbers = []
        for x in self.dice:
            numbers.append(x.giveNumber())
        base = self.comboIn.getBaseValue(self.comboIn.getCombo(numbers))
        print("[ "+str(base[0])+" X "+str(base[1])+" ]")
        self.value = [base[0],base[1],1]
        for x in self.dice:
            self.value = x.calculate(self.value)
        self.roundValue += self.value[0] * self.value[1] * self.value[2]
        print("[ " + str(self.value[0]) + " X " + str(self.value[1]) + " ] = " + str(self.value[0] * self.value[1]))
        if self.value[2] != 1:
            print("X" + str(self.value[2]))
            print(self.value[0] * self.value[1] * self.value[2])
        self.play -= 1
        return self.roundValue
    
    def reroll(self, list):
        #the list should be list of ints to reroll for
        tempList = []
        try:
            for x in list:
                tempList.append(int(x) - 1)
        except ValueError:
            return False
        if self.rerollChances <= 0:
            return False
        self.rerollChances -= 1
        for x in tempList:
            if x > len(self.dice) - 1:
                tempList.pop(tempList.index(x))
        for x in tempList:
            self.dice[x].roll()
        return True
    
    def getDieDescription(self):
        descriptionList = []
        for x in self.dice:
            descriptionList.append(x.description())
        return descriptionList
    
    def roundInfo(self):
        return ["Round " + str(self.round), "Goal " + str(self.roundGoal) + " : Current " + str(self.roundValue), "Play " + str(self.play) + "/ Reroll " + str(self.rerollChances)]

    def playAll(self):
        self.roundValue += self.calculate()
        if self.roundValue > self.roundGoal:
            return True
        if self.play == 1:
            return False
        self.rollAll()
        return None
    
    def getComboInfo(self):
        numbers = []
        for x in self.dice:
            numbers.append(x.giveNumber())
        return self.comboIn.currentSetInfo(self.comboIn.getCombo(numbers))
    
    def getRound(self):
        return self.round


"""
combo stregh
0.5 of a kind
1.4 of a kind
2.straight
3.full house
4.two pair
5.triple
6.pair
7.high
"""
class combo():
    def __init__(self):
        self.comboLv = [0,0,0,0,0,0,0,0]
        self.comboBaseValue = {
            0: [5, 1],
            1: [10, 2],
            2: [20, 2], 
            3: [30, 3],
            4: [30, 4],
            5: [35, 4],
            6: [40, 4],
            7: [60, 7],
        }
        self.comboName = ["Five of a Kind", "Four of a Kind", "Straight", "Full House", " Two Pairs", "Triple", "Pair", "High Die"]

    def reset(self):
        #used later when combo can be upgraded
        self.comboLv = [0,0,0,0,0,0,0,0]
        self.comboBaseValue = {
            0: [5, 1],
            1: [5, 2],
            2: [10, 2], 
            3: [10, 3],
            4: [15, 3],
            5: [20, 4],
            6: [30, 4],
            7: [40, 5],
        }

    def getCombo(self,numberList):
        sortedList = sorted(numberList)
        if sortedList.count(sortedList[2]) == 5:
            return 0
        elif sortedList.count(sortedList[2]) == 4:
            return 1
        elif sortedList.count(sortedList[2]) == 3:
            if sortedList[3] == sortedList[4] and sortedList[0] == sortedList[1]:
                return 3
            else:
                return 5
        elif sortedList[0] == sortedList[1]:
            if sortedList.count(sortedList[3]) == 2:
                return 4
            return 6
        elif sortedList[1] == sortedList[2]:
            if sortedList[3] == sortedList[4]:
                return 4
            return 6
        elif sortedList[2] == sortedList[3] or sortedList[3] == sortedList[4]:
            return 6
        elif sortedList[0] + 4 == sortedList[4]:
            return 2
        return 7
        
    def getBaseValue(self,comboNumber):
        base = self.comboBaseValue[7-comboNumber]
        base[0] += self.comboLv[comboNumber] * 2
        base[1] += self.comboLv[comboNumber]
        return base
    
    def currentSetInfo(self,comboNumber):
        return "Lv." + str(self.comboLv[comboNumber] + 1) + " " + str(self.comboBaseValue[7 - comboNumber][0]) + " X " + str(self.comboBaseValue[7 - comboNumber][1]) + " " + self.comboName[comboNumber]

    def getLvList(self):
        return self.comboLv
    
    def comboUpgrade(self,comboNumber):
        self.comboLv[comboNumber] += 1


class display():
    def __init__(self, saveIn):
        self.status = "round"
        self.saveIn = saveIn

    def displayRound(self):
        #List names of buffs here
        print()
        for x in self.saveIn.roundInfo():
            print(x)
        print()
        print(self.saveIn.getComboInfo())
        print()
        eyeList = self.saveIn.showAllDice()
        for x in eyeList:
            print("[" + x + "]", end=" ")
        print()
        print()
        #Print List of Commands
        print("List of commands:")
        print("info")
        print("reroll (ints)")
        print("play")

    def info(self):
        #List of buffs
        print()
        for x in range(0,8):
            print(self.saveIn.comboIn.currentSetInfo(x))
        print()
        descriptions = self.saveIn.getDieDescription()
        for x in descriptions:
            print(x)

    def shop(self):
        print("Choose 1 Upgrade to Discard")
        print("1: Dice")
        print("2: Buff")
        print("3: Combo")
        print()
        print("Commands:")
        print("info")
        print("dice")
        print("buff")
        print("combo")


class round():
    def __init__(self, show):
        self.display = show

    def run(self):
        while True:
            self.display.displayRound()
            answer = inputReconize(input(">>> "))
            print(answer)
            if answer[0] is True:
                if answer[1] == "r" or answer[1] == "reroll":
                    self.display.saveIn.reroll(answer[2])
                elif answer[1] == "p" or answer[1] == "play":
                    returnValue = self.display.saveIn.playAll()
                    if returnValue is True:
                        print("Win!")
                        return True
                    elif returnValue is False:
                        print("Lost")
                        return False
                elif answer[1] == "i" or answer[1] == "info":
                    self.display.info()
                    input(">>> ")

class shop():
    def __init__(self,show):
        self.display = show
    
    def printOptions(self, optionList):
        i = 0
        for x in optionList:
            i += 1
            print(str(i) + ": " + x)

    def run(self):
        while True:
            self.display.shop()
            answer = inputReconize(input(">>> "))
            if answer[1] == "i" or answer[1] == "info":
                self.display.info()
                input(">>> ")
            elif answer[1] == "c" or answer[1] == "combo" or answer[1] == "3" or answer[1] == "1" or answer[1] == "2" or answer[1] == "b" or answer[1] == "buff" or answer[1] == "dice" or answer[1] == "d":
                if answer[1] != "c" and answer[1] != "combo" and answer[1] != "3":

                    self.checkList = [random.randint(0,7)]
                    while len(self.checkList) != 5:
                        newOption = random.randint(0,7)
                        poss = True
                        for x in self.checkList:
                            if newOption == x:
                                poss = False
                                break
                        if poss:
                            self.checkList.append(newOption)
                    optionList = []
                    for x in self.checkList:
                        optionList.append(self.display.saveIn.comboIn.currentSetInfo(x))
                    while True:
                        print("Choose up to 3. ex)type 'choose 1 2 3'")
                        self.printOptions(optionList)
                        print()
                        answer = inputReconize(input(">>> "))
                        if answer[1] == "c" or answer[1] == "choose":
                            if len(answer[2]) <= 3:
                                break
                    final = []
                    for x in answer[2]:
                        if int(x)-1 <= 4 and int(x)-1 >= 0:
                            self.display.saveIn.comboIn.comboUpgrade(int(x))
                #work on the dice upgrade and buffs upgrades later
                break


# z = combo()
# a = save(z)
# a.rollAll()
# b = display(a)
# b.displayRound()
# c = round(b)
# c.run()
# d = shop(b)
# d.run()

comboMain = combo()
main_save = save(comboMain)
mainDisplay = display(main_save)
main_Round = round(mainDisplay)
main_shop = shop(mainDisplay)

while main_save.getRound() <= 12:
    main_save.newRound()
    main_save.rollAll()
    result = main_Round.run()
    if result is False:
        print("You Lost")
        break
    if main_save.getRound() == 12:
        print("You win!")
        break
    main_shop.run()

