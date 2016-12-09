############################################
# Thomas Lehman-Borer & Rachel Chamberlain #
#     Dungeons and Dragons Facilitator     #
#            CS 1 Final Project            #
############################################

from random import shuffle

chars = {}
monst = {}


class SentientBeing:
    '''This class is a parent class to Character and Monster. It holds simple methods common to both subclasses,
    such as basic getters for health and experience, and basic setters like changing health and armor. In addition,
    this class has the methods minForHit and attack, where the former is only used in the latter and thus is private.'''
    ### CONSTRUCTOR ###
    def __init__(self, name, experience, health, species, attacks, armor):
        # Initialize common attributes and create a dictionary of functions
        # that can be used in the combat function (near the end of the file).
        self.__name = name  # string
        self.__experience = experience  # float
        self.__health = health  # list with two items -> [current, max]
        self.__species = species  # string
        self.attacks = attacks  # dictionary
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
    # These are the simple getters of attributes instances of the sentient being class.
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
    # These are setter methods to modify attributes of the SentientBeing (SB) instances.
    def changeHealth(self, change):
        # This method takes the parameter change which is then added to the current health of the being.
        # To decrease the current health, simply enter a negative integer.
        current = self.__health[0]
        maximum = self.__health[1]
        # Define if/else statements to make sure the health doesn't go below zero or above the max
        if current + int(change) < 0:
            self.__health[0] = 0
        elif current + int(change) > maximum:
            self.__health[0] = maximum
        else:
            self.__health[0] += int(change)

    def setMaxHealth(self, val):
        # This method changes the max amount of health a being can have and decreases the current
        # if it becomes greater than the max when changing the max.
        self.__health[1] = int(val)
        if self.__health[0] > self.__health[1]:
            self.__health[0] = self.__health[1]

    def addExp(self, change):
        # This method adds to the experience, which is a float
        self.__experience += float(change)

    def setArmor(self, newArm):
        # This method sets the armor class of the being.
        # Note: smaller values for the armor class equates to better armor.
        if newArm > 0 and newArm < 10:
            self.__armor = newArm
        else:  # else statement to make sure the armor class is in the right range.
            print("You must enter an integer from 1 to 9")

    ### OTHERS ###
    def __str__(self):
        # Overload function so that printing the SB instance gives only the name
        # (and not a gibberish pointer).
        return self.__name

    def __bool__(self):
        # This overload is mainly for knowing when a SB instance is dead (current health = 0).
        # It is used in combat to know when to remove them from the appropriate lists/dictionary.
        if self.__health[0] == 0:
            return False
        else:
            return True

    def __minForHit(self, being, attRoll):
        # This private function determines what the minimum die roll is in order to be able to hit the
        # SB. This is its own function because we need to calculate this with armor (for all SB) and level for
        # Characters and experience for Monsters. This function starts as an if/else statement to know which
        # calculation method to use.
        if isinstance(self, Character):
            dArmor = being.getArmor()
            # good for character levels 1-3; information for higher levels to come later
            # armor : minimum roll
            table = {9: 10, 8: 11, 7: 12, 6: 13, 5: 14, 4: 15, 3: 16, 2: 17}

            return table[dArmor]  # returns the min roll value for the character

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

            return table[dArmor]  # # returns the min roll value for the monster

    def attack(self, being):
        # This method is how characters attack other characters. It takes the param of the being to be attacked
        # (being, "the target") and used attacks info from the attacker (self) to ask the user what attack to use.
        # The user gets to roll the die, but the function tells the user how they should calculate the damage
        # done by the attack and the user just tells the function what the result is. This function tells you if an
        # attack hits the target and, if it does, it deducts from the health automatically.

        # If statement to make sure that being, not an instance of a SentientBeing subclass,
        # becomes one or is labeled as not attackable. When using combat, a string is passed as being
        # so we must account for that by pulling the value from the key's respective dictionary.
        if not isinstance(being, SentientBeing):
            if being in chars:
                being = chars[being]
            elif being in monst:
                being = monst[being]
            else:
                print("This is not a valid being to attack")

        # Interact with the user by asking which attack in the attacker's (self's) attack dictionary
        # the user wants to use. We made it possible for the user to only type a partial string and
        # get the attack from there. If there are more than one attacks with the partial string, it will
        # ask the user to enter the full name.
        print('What is the attack of choice?')
        print(self.attacks)
        possibilities = 0
        attack = input(' >> ')
        while attack not in self.attacks:
            fullName = ''
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

        # The user enters the results of the hit die, or if the attack will land on the target.
        hitDie = int(input('What is the result of a 1d20 roll? '))

        # If it does, then ask what the results of the damage roll is and change the health of the
        # target accordingly.
        if self.__minForHit(being, self.attacks[attack]) <= hitDie:
            attDie = int(input('What is the result of a ' +
                               self.attacks[attack] + ' roll? '))
            being.changeHealth(-attDie)

            if being.getHealth()[0] != 0:
                print('The health of', being.getName(), 'is now', being.getHealth())
            else:
                print('You have slain', being.getName() + '.')
        # case for the target evading
        elif hitDie < 10:
            print(being.getName(), 'evades the attack.')
        # Case for the armor blocking the attack.
        else:
            print("The attack is blocked by the defender's armor.")

########################################################################################################################


class Character(SentientBeing):
    '''This is a subclass of SentientBeing which adds attributes and methods which aren't used in Monster.
    It all the methods of its parent class and adds attributes and getters/setters for money and level
    and now the character has a player name.'''
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
    # the basic getters for the subclass
    def getMoney(self):
        # returns the list of the money to the terminal
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
    '''This is a subclass of SentientBeing and has no unique attributes but it's easier to keep track of being types 
    with the additonal subclass. Future plans include subclasses of Monster.'''
    ### CONSTRUCTOR ###
    def __init__(self, name, experience, health, species, attacks, armor):
        super().__init__(name, experience, health, species, attacks, armor)

        if name not in monst:
            monst[name] = self

########################################################################################################################


def newChar():
    '''newChar is a function to make a new character in the game. If asks you step-by-step for attributes and
    constructs the Character object based on responses. Attacks will be added directly the attacks dictionary
    for the Character. This function returns the Character object, so use [name] = newChar() to get
    your new character, where [name] is replaced with the actual name of the character.'''
    print("Begin new character construction.\n")

    name = input('What is the character name? ').replace(" ", "")
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
    '''This function is very similar to newChar only it makes Monster objects. It is designed and used in the 
    same way (user input for each attribute and the function constructs and returns the Monster object.'''
    print("Begin new monster construction.\n")
    name = input('What shall we call the monster? ').replace(" ", "")
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
    '''This function saves current Character data to a .txt file. It writes one Character object per line
    and separates the attributes with a colon (':'). The load function below reads the save file format.'''
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
    """This function reads in from a save file (.txt) and returns a dictionary of character
    objects. For ease of use, user should say 'chars = load()'. Once the file is loaded, the user will have
    to set each character object to a variable(ie: >>> bernie = chars['Bernie'])"""
    characters = {}

    filename = input('Filename: ')
    fh = open(filename, 'r')

    fh.readline()  # first line of file(CHARS)

    line = fh.readline().strip("\n")  # reads rhe first character and constructs it in the while loop
    while 'ENDCHARS' not in line:  # for each character
        # formatting into desired types
        args = line.split(':')
        args[2] = int(args[2])  # level
        args[3] = float(args[3])  # experience

        args[4] = args[4].split(',')  # health
        for i in range(len(args[4])):
            args[4][i] = int(args[4][i])

        args[6] = int(args[6])  # armor

        args[7] = args[7].split(',')  # money
        for i in range(len(args[7])):
            args[7][i] = int(args[7][i])

        attacks = args[8].split(';')  # attacks dictionary
        attackKeys = attacks[0].split(',')
        attackVals = attacks[1].split(',')
        args[8] = dict(zip(attackKeys, attackVals))

        # remove the occasional extra empty key
        if '' in args[8]:
            del args[8]['']

        # add the Character name to the dictionary as the key and the Character object as rhe value.
        characters[args[0]] = Character(*args)
        # Read the next line to either add another character to the dictionary or stop the while loop
        # if the line is "ENDCHARS"
        line = fh.readline().strip("\n")

    fh.close()
    return characters  # return the dictionary


def combat(Chars, Monst):
    '''This function was the biggest pain in the butt. It takes the parameters of the character list chars 
    and the monster list monst and randomly makes an order in which the combatants get their turn.
    During their turn, they can choose from a number of functions in the combatDict defined in SB.
    type "next" to end the turn and otherwise type the function you want to execute. If the function
    takes parameters, just type a space between the funciton and the parameter and the combat function interprets.
    Current note: even if one side is totally dead, because of the for loop, it must finish going through the
    combatants before a winner is declared. (Maybe not still the case??)'''
    charList = list(Chars.values())
    monsList = list(Monst.values())

    combatants = charList + monsList

    shuffle(combatants)  # shuffle the list for a random order

    print("\nThe order is:")
    for com in combatants:
        print('\t' + str(com))  # print the order of the turns

    # Make a while loop to keep going until one list (monsList or charList) is empty.
    while monsList != [] and charList != []:
        for com in combatants:  # use a for loop to go through each SB instance in the combatants list.
            print('\n' + str(com).upper())

            continuing = True
            while continuing:  # make a while loop to keep the user's turn going until they type 'next'
                action = input("What does the combatant do? When done with turn, type 'next' to continue.\n >> ")
                functs = action.split()
                if functs[0] == 'next':
                    continuing = False
                elif functs[0] not in com.combatDict:
                    print("This is not a valid action.")
                elif len(functs) > 1:
                    com.combatDict[functs[0]](*functs[1:])  # execute the function with parameters
                else:  # if len(functs) == 1
                    if 'get' == functs[0][:3]:  # execute the getter functions without parameters and print the return
                        print(com.combatDict[functs[0]]())
                    else:
                        com.combatDict[functs[0]]()  # execute the functions without parameters.

                # When something dies in combat, it's off all lists.
                for char in combatants:
                    if not bool(char):
                        combatants.remove(char)
                        if char in charList:
                            charList.remove(char)
                            del chars[char.getName()]
                        elif char in monsList:
                            monsList.remove(char)
                            del monst[char.getName()]

        # when one list is empty, it declared a winner.
        if charList == []:
            print("Battle is over. The winner is the monsters.")
        elif monsList == []:
            print("Battle is over. The winner is the characters.")
