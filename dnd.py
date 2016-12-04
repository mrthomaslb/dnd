import random as r

charList = []
monsList = []

class SentientBeing:

    ### CONSTRUCTOR ###
    def __init__(self, experience, health, species, attacks, armor):
        self.__experience = experience
        self.__health = health  # list with two items -> [current, max]
        self.__species = species
        self.attacks = attacks
        self.__armor = armor  # integer
        if isinstance(self, Character) == True:
            if self not in charList:
                self.__appTo(charList)
        elif isinstance(self, Monster) == True:
            if self not in monsList:
                self.__appTo(monsList)

    ### GETTERS ###
    def getHealth(self):
        return self.__health

    def getArmor(self):
        return self.__armor
    
    def getExp(self):
        return self.__experience

    def getSpecies(self):
        return self.__species

    ### SETTERS ###
    def changeHealth(self, change):
        current = self.__health[0]
        maximum = self.__health[1]
        if current + change < 0:
            self.__health[0] = 0
        elif current + change > maximum:
            self.__health[0] = maximum
        else:
            self.__health[0] = self.__health[0] + change
            
    def __appTo(self, ls):
        ls.append(self)

    def setMaxHealth(self, val):
        self.__health[1] = val
        if self.__health[0] > self.__health[1]:
            self.__health[0] = self.__health[1]

    def addExp(self, change):
        pass

    def setArmor(self, newArm):
        pass

    ### OTHERS ###
    def attack(self, being):
        #probably don't need this
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
        print('Any level-dependent attacks must be changed manually.')
        self.__level += 1

    ### OTHERS ###

    def __str__(self):
        return self.__name


class Monster(SentientBeing):
    ### CONSTRUCTOR ###
    def __init__(self, experience, health, species, attacks, armor):
        super().__init__(experience, health, species, attacks, armor)

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
    print('Append the character to charList so that it is saved.')
    return Character(name, player, level, experience, health, species, armor, money, attacks)


def newMonster():
    print("Begin new monster construction.\n")
    species = input("What is the species of this monster? ")
    experience = float(input("What is the experience of this monster? "))
    health1 = int(input("What is the max health of this monster? "))
    health0 = health1
    health = [health0, health1]
    armor = input("What armor class does the monster have? ")
    attacks = {}
    print("\nYou will need to set the monsters attacks separately.")
    return Monster(experience, health, species, attacks, armor)


def save(charList):
    filename = input('Filename: ')
    fh = open(filename,'w')
    
    fh.write('CHARS\n')
    for char in charList:
        attackKeys = ''
        attackVals = ''
        for key in char.attacks:
            attackKeys += key + ','
            attackVals += char.attacks[key] + ','
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

    line = fh.readline()  # first line of file(CHARS)

    line = fh.readline()  # first character
    while 'ENDCHARS' not in line:  # for each character
        # print(line)

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

        characters.append(Character(*args))
        line = fh.readline()

    fh.close()
    return characters

#not accepting chars list right
def combat():
    chars = eval(input("Input the characters involved as a list []: "))
    monst = eval(input("Input the monsters involved as a list []: "))

    combatants = chars + monst
    r.shuffle(combatants)

    print("The order is : ", combatants)

    while monst != [] and chars != []:
        for com in combatants:
            print("It is the turn for ", com)
            action = input("What does the character do? When done with turn, type 'next' to continue.")
            while action.lower() != "next":
                eval(com.action)

            for char in combatants:
                if com.getHeatlh() == 0:
                    combatants.remove(char)
    if chars == []:
        print("Battle is over. The winner is the monsters.")
    elif monst == []:
        print("Battle is over. The winner is the characters.")
