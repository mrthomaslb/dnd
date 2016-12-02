import random as r

charList = []


class SentientBeing:
    ### CONSTRUCTOR ###
    def __init__(self, experience, health, species, attacks, armor):
        self.__experience = experience
        self.__health = health  # list with two items -> [current, max]
        self.__species = species
        self.__attacks = attacks
        self.__armor = armor  # integer

    ### GETTERS ###

    def getHealth(self):
        return self.__health

    def getArmor(self):
        return self.__armor

    def getAttacks(self):
        return self.__attacks

    def getExp(self):
        return self.__experience

    def getSpecies(self):
        return self.__species

    ### SETTERS ###
    def changeHealth(self, change):
        current = self.__health[0]
        max = self.__health[1]
        if current + change < 0:
            self.___health[0] = 0
        elif current + change > max:
            self.__health[0] = max
        else:
            self.__health[0] = self.__health[0] + change

    def setMaxHealth(self, val):
        self.__health[1] = val
        if self.__health[0] > self.__health[1]:
            self.__health[0] = self.__health[1]

    ### OTHERS ###
    def attack(self, being):
        pass


class Character(SentientBeing):
    '''Constructor'''

    def __init__(self, name, player, level, experience, health, species, armor, money, attacks):
        self.__name = name
        self.__player = player
        self.__level = level
        self.__money = money
        super().__init__(experience, health, species, attacks, armor)

    ### GETTERS ###
    def chrSheet(self):
        pass
        # print out a character sheet nicely (centered name, etc.)

    def getName(self):
        return self.__name

    def getMoney(self):
        # Possibly change this to print it nicely later
        return self.__money

    def playerName(self):
        return self.__player

    def getLevel(self):
        return self.__level

    ### SETTERS ###

    def lvlUp(self):
        self.__level += 1
        for key in self.__attacks:
            val = self.__attacks.get(key)
            calc = val[1:]
            self.__attacks[key] = str(self.getLevel()) + calc

    def addAttack(self):
        name = input("What is the name of the weapon? ")
        calc = input("How is the damage calculated? (ex: d6 + 1) ")
        self.__attacks[name] = str(self.getLevel()) + calc
        print(name, " has been added to known attacks for ", self.__name)

    ### OTHERS ###

    def __str__(self):
        return self.__name


class Monster(SentientBeing):
    ### CONSTRUCTOR ###
    def __init__(self, experience, health, species, attacks, armor):
        super().__init__(experience, health, species, attacks, armor)

    def addAttack(self):
        pass


def dice(quantity, sides):
    # look into making functions of 1 or 2 parameters
    # in this case, it would assume 1 die if there were 1 parameter given
    dice = []
    total = 0

    for i in range(quantity):
        roll = r.randint(1, sides)
        dice.append(str(roll))
        total += roll

    print('Rolls:', ' '.join(dice))
    print('Sum:', total)
    return total


def newChar():
    # The input function always returns a string, so we will need to convert all of
    # the variables to the desired types. Also, I think experience is a float.
    print("Begin new character construction.\n")

    name = input('What is the character name? ')
    player = input("What is the player name? ")
    level = int(input("What level is the character?"))
    experience = float(input("How much experience does the character have? "))

    health1 = int(input("What is the character's max health? "))
    health0 = int(input("What is the character's current health? "))
    health = [health0, health1]

    species = input("What species is the character? ")
    armor = int(input("What is the character's armor class? "))

    print('How much of each of these monetary denominations does the character have?')
    plat = input('Platinum: ')
    gold = input('Gold: ')
    silv = input('Silver: ')
    copp = input('Copper: ')
    elec = input('Electrum: ')
    money = [int(plat), int(gold), int(silv), int(copp), int(elec)]

    attacks = {}
    print("\nYou will need to set your attacks separately using addAttack() .")
    print('Append the character to charList so that it is saved.')
    return Character(name, player, level, experience, health, species, armor, money, attacks)


def newMonster():
    # experience, health, species, attacks, armor
    print("Begin new monster construction.\n")
    species = input("What is the species of this monster? ")
    experience = float(input("What is the experience of this monster? "))
    health1 = int(input("What is the max health of this monster? "))
    health0 = health1
    health = [health0, health1]
    armor = input("What armor class does the monster have? ")
    attacks = {}
    print("\nou will need to set the monsters attacks separately using  addAttack() .")
    return Monster(experience, health, species, attacks, armor)


def save(charList):
    filename = input('Filename: ')
    fh = open(filename,'w')
    
    fh.write('CHARS\n')
    for char in charList:
        attackKeys = ''
        attackVals = ''
        for key in char.getAttacks():
            attackKeys += key + ','
            attackVals += char.getAttacks()[key] + ','
        attacks = attackKeys[:-1] + ';' + attackVals[:-1]

        attributes = [char.getName(), char.playerName(), str(char.getLevel()),
                      str(char.getExp()), str(char.getHealth())[1:-1],
                      char.getSpecies(), str(char.getArmor()),
                      str(char.getMoney())[1:-1], attacks]
        fh.write(':'.join(attributes)+'\n')
        
    fh.write('ENDCHARS\n')
    
    fh.close()
    print('Character data saved.')

def load():
    """This function reads in from a save file and returns a list of character
objects. For ease of use, user should say 'charList = load()'."""
    characters = []

    filename = input('Filename: ')
    fh = open(filename, 'r')
    
    line = fh.readline() #should say CHARS

    while True: #for each character
        line = fh.readline()

        if 'ENDCHARS' in line: break
        #I think saying while 'END' not in line would be off by 1

        #formatting into desired types
        args = line.split(':')
        args[2] = int(args[2]) #level
        args[3] = float(args[3]) #experience
        args[4] = args[4].split(',') #health
        args[6] = int(args[6]) #armor
        args[7] = args[7].split(',') #$
        
        attacks    = args[8].split(';')
        attackKeys = attacks[0].split(',')
        attackVals = attacks[1].split(',')
        args[8] = dict(zip(attackKeys,attackVals))

        characters.append(Character(*args))

    fh.close()
    return characters
