############################################
# Thomas Lehman-Borer & Rachel Chamberlain #
#     Dungeons and Dragons Facilitator     #
#            CS 1 Final Project            #
############################################

# Notes to self:
# 1. Make sure to remove test monsters from the monst dictionary before submitting.
# 2. Include an example .txt file for the profs to test the code with.
# 3. Remove any functions that are no longer in the scope of the project.
# 4. Remove any comments to ourselves regarding changing/fixing/adding something.

import random as r

chars = {}
monst = {}


class SentientBeing:
    ### CONSTRUCTOR ###
    def __init__(self, name, experience, health, species, attacks, armor):
        self.__name = name
        self.__experience = experience
        self.__health = health  # list with two items -> [current, max]
        self.__species = species
        self.attacks = attacks
        self.__armor = armor  # integer
        self.combatDict = {'attack': self.attack,
                           'changeHealth': self.changeHealth,
                           'getHealth': self.getHealth,
                           'setMaxHealth': self.setMaxHealth,
                           'getArmor': self.getArmor,
                           'setArmor': self.setArmor,
                           'getExp': self.getExp,
                           'addExp': self.addExp,
                           'getName': self.getName(),
                           'getSpecies': self.getSpecies}

    ### GETTERS ###
    def getHealth(self):
        return self.__health

    def getArmor(self):
        return self.__armor

    def getExp(self):
        return self.__experience

    def getSpecies(self):
        return self.__species

    def getName(self):
        return self.__name

    ### SETTERS ###
    def changeHealth(self, change):
        current = self.__health[0]
        maximum = self.__health[1]
        if current + int(change) < 0:
            self.__health[0] = 0
        elif current + int(change) > maximum:
            self.__health[0] = maximum
        else:
            self.__health[0] += int(change)

    def setMaxHealth(self, val):
        self.__health[1] = int(val)
        if self.__health[0] > self.__health[1]:
            self.__health[0] = self.__health[1]

    def addExp(self, change):
        self.__experience += float(change)

    def setArmor(self, newArm):
        if newArm > 0 and newArm < 10:
            self.__armor = newArm
        else:
            print("You must enter an integer from 1 to 9")

    ### OTHERS ###
    def __str__(self):
        return self.__name

    def __bool__(self):
        if self.__health[0] == 0:
            return False
        else:
            return True

    def minForHit(self, being, attRoll):
        if isinstance(self, Character):
            dArmor = being.getArmor()

            # good for character levels 1-3; information for higher levels to come later
            # armor : minimum roll
            table = {9: 10, 8: 11, 7: 12, 6: 13, 5: 14, 4: 15, 3: 16, 2: 17}

            return table[dArmor]

        elif isinstance(self, Monster):
            dArmor = being.getArmor()

            # splitting something formatted like '3d6 + 1' into [[3,6],1]
            # works without modifier or with negative modifier
            if '+' not in attRoll and '-' not in attRoll:
                attRoll += '+0'
                attRoll = attRoll.split('+')
            elif '+' in attRoll:
                attRoll = attRoll.split('+')
            elif '-' in attRoll:
                attRoll = attRoll.split('-')
            attRoll[1] = int(attRoll[1])
            attRoll[0] = attRoll[0].split('d')
            attRoll[0][0] = int(attRoll[0][0])
            attRoll[0][1] = int(attRoll[0][1])

            numDice = attRoll[0][0]

            if numDice >= 11:
                table = {9: 0, 8: 1, 7: 2, 6: 3, 5: 4, 4: 5, 3: 6, 2: 7}
            elif numDice in [9, 10]:
                table = {9: 2, 8: 3, 7: 4, 6: 5, 5: 6, 4: 7, 3: 8, 2: 9}
            elif numDice in [7, 8]:
                table = {9: 4, 8: 5, 7: 6, 6: 7, 5: 8, 4: 9, 3: 10, 2: 11}
            elif (numDice in [5, 6]) or (numDice == 4 and attRoll[1] > 0):
                table = {9: 5, 8: 6, 7: 7, 6: 8, 5: 9, 4: 10, 3: 11, 2: 12}
            elif numDice == 4 or (numDice == 3 and attRoll[1] > 0):
                table = {9: 6, 8: 7, 7: 8, 6: 9, 5: 10, 4: 11, 3: 12, 2: 13}
            elif numDice == 3 or (numDice == 2 and attRoll[1] > 0):
                table = {9: 8, 8: 9, 7: 10, 6: 11, 5: 12, 4: 13, 3: 14, 2: 15}
            elif numDice == 2 or attRoll[1] > 1:
                table = {9: 9, 8: 10, 7: 11, 6: 12, 5: 13, 4: 14, 3: 15, 2: 16}
            else:
                table = {9: 10, 8: 11, 7: 12, 6: 13, 5: 14, 4: 15, 3: 16, 2: 17}

            return table[dArmor]

    def attack(self, being):
        if not isinstance(being, SentientBeing):
            if being in chars:
                being = chars[being]
            elif being in monst:
                being = monst[being]
            else:
                return "This is not a valid being to attack"
        print('What is the attack of choice?')
        print(self.attacks)
        possibilities = 0
        attack = input(' >> ')
        while attack not in self.attacks:
            for a in self.attacks:
                if attack in a:
                    possibilities += 1
                    fullName = a
            if possibilities == 1:
                attack = fullName
            elif possibilities > 1:
                print('Which attack did you mean?')
                attack = input(' >> ')
            else:
                print('That is not an available attack.')
                attack = input(' >> ')

        hitDie = int(input('What is the result of a 1d20 roll? '))

        if self.minForHit(being, self.attacks[attack]) <= hitDie:
            attDie = int(input('What is the result of a ' +
                               self.attacks[attack] + ' roll? '))
            being.changeHealth(-attDie)

            if being.getHealth()[0] != 0:
                print('The health of', being.getName(), 'is now', being.getHealth())
            else:
                print('You have slain', being.getName() + '.')

        elif hitDie < 10:
            print(being.getName(), 'evades the attack.')
            
        else:
            print("The attack is blocked by the defender's armor.")

########################################################################################################################


class Character(SentientBeing):
    ### CONSTRUCTOR ###
    def __init__(self, name, player, level, experience, health, species, armor, money, attacks):
        self.__player = player
        self.__level = level
        self.__money = money
        super().__init__(name, experience, health, species, attacks, armor)
        self.combatDict['playerName'] = self.playerName
        self.combatDict['getLevel'] = self.getLevel
        self.combatDict['lvlUp'] = self.lvlUp

        if name not in chars:
            chars[name] = self

    ### GETTERS ###
    def getMoney(self):
        return self.__money

    def playerName(self):
        return self.__player

    def getLevel(self):
        return self.__level

    ### SETTERS ###
    def lvlUp(self):
        print('Any level-dependent attacks must be changed manually.')
        self.__level += 1

########################################################################################################################


class Monster(SentientBeing):
    ### CONSTRUCTOR ###
    def __init__(self, name, experience, health, species, attacks, armor):
        super().__init__(name, experience, health, species, attacks, armor)

        if name not in monst:
            monst[name] = self

########################################################################################################################


def dice(quantity, sides):
    dice = []
    total = 0
    for i in range(quantity):
        roll = r.randint(1, sides)
        dice.append(str(roll))
        total += roll

    print('Rolls:', ' '.join(dice))
    print('Sum:  ', total)
    return total


def newChar():
    print("Begin new character construction.\n")

    name = input('What is the character name? ')
    player = input("What is the player name? ")

    level = int(input("What level is the character? "))
    experience = float(input("How much experience does the character have? "))
    health1 = int(input("What is the character's max health? "))
    health0 = int(input("What is the character's current health? "))
    health = [health0, health1]

    species = input("What species is the character? ")
    armor = int(input("What is the character's armor class? "))

    print('How much of each of these monetary denominations does the character have?')
    plat = input('Platinum: ')
    gold = input('Gold:     ')
    silv = input('Silver:   ')
    copp = input('Copper:   ')
    elec = input('Electrum: ')
    money = [int(plat), int(gold), int(silv), int(copp), int(elec)]

    attacks = {}
    print("\nYou will need to set your attacks separately.")
    return Character(name, player, level, experience, health, species, armor, money, attacks)


def newMonster():
    print("Begin new monster construction.\n")
    name = input('What shall we call the monster? ')
    species = input("What is the species of this monster? ")
    experience = float(input("What is the experience of this monster? "))
    health1 = int(input("What is the max health of this monster? "))
    health0 = health1
    health = [health0, health1]
    armor = int(input("What armor class does the monster have? "))
    attacks = {}
    print("\nYou will need to set the monsters attacks separately.")
    return Monster(name, experience, health, species, attacks, armor)


def save(chars):
    filename = input('Filename: ')
    fh = open(filename, 'w')

    fh.write('CHARS\n')
    for char in chars.values():
        attackKeys = ''
        attackVals = ''
        for key in char.attacks:
            attackKeys += key + ','
            attackVals += char.attacks[key] + ','
        attacks = attackKeys[:-1] + ';' + attackVals[:-1]

        attributes = [str(char), char.playerName(), str(char.getLevel()),
                      str(char.getExp()), str(char.getHealth())[1:-1],
                      char.getSpecies(), str(char.getArmor()),
                      str(char.getMoney())[1:-1], attacks]
        fh.write(':'.join(attributes) + '\n')

    fh.write('ENDCHARS\n')

    fh.close()
    print('Character data saved.')


def load():
    """This function reads in from a save file and returns a list of character
objects. For ease of use, user should say 'chars = load()'."""
    characters = {}

    filename = input('Filename: ')
    fh = open(filename, 'r')

    line = fh.readline()  # first line of file(CHARS)

    line = fh.readline().strip("\n")  # first character
    while 'ENDCHARS' not in line:  # for each character

        # formatting into desired types
        args = line.split(':')
        args[2] = int(args[2])  # level
        args[3] = float(args[3])  # experience

        args[4] = args[4].split(',')  # health
        for i in range(len(args[4])):
            args[4][i] = int(args[4][i])

        args[6] = int(args[6])  # armor

        args[7] = args[7].split(',')  # $
        for i in range(len(args[7])):
            args[7][i] = int(args[7][i])

        attacks = args[8].split(';')
        attackKeys = attacks[0].split(',')
        attackVals = attacks[1].split(',')
        args[8] = dict(zip(attackKeys, attackVals))

        if '' in args[8]:
            del args[8]['']

        characters[args[0]] = Character(*args)
        line = fh.readline().strip("\n")

    fh.close()
    return characters


def combat(Chars, Monst):
    charList = list(Chars.values())
    monsList = list(Monst.values())

    combatants = charList + monsList

    r.shuffle(combatants)

    print("\nThe order is:")
    for com in combatants:
        print('\t' + str(com))

    while monsList != [] and charList != []:
        for com in combatants:
            print('\n' + str(com).upper())

            continuing = True
            while continuing:
                action = input("What does the combatant do? When done with turn, type 'next' to continue.\n >> ")
                functs = action.split()
                if functs[0] == 'next':
                    continuing = False
                elif functs[0] not in com.combatDict:
                    print("This is not a valid action.")
                elif len(functs) > 1:
                    com.combatDict[functs[0]](*functs[1:])
                else:  # if len(functs) == 1
                    if 'get' == functs[0][:3]:
                        print(com.combatDict[functs[0]]())
                    else:
                        com.combatDict[functs[0]]()

            # When something dies in combat, it's off the list.
            for char in combatants:
                if not bool(char):
                    combatants.remove(char)
                if char in charList:
                    charList.remove(char)
                    del chars[char.getName()]
                elif char in monsList:
                    monsList.remove(char)
                    del monst[char.getName()]

    if charList == []:
        print("Battle is over. The winner is the monsters.")
    elif monsList == []:
        print("Battle is over. The winner is the characters.")
