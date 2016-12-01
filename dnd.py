from random import randint

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


class character(SentientBeing):
    '''Constructor'''

    def __init__(self, player, level, experience, health, species, armor, money, attacks):
        self.__player = player
        self.__level = level
        self.__money = money
        super().__init__(experience, health, species, attacks, armor)


    ### GETTERS ###
    def chrSheet(self):
        pass
        # print out a character sheet nicely (centered name, etc.)

        # Can we just do this as a __str__ method? I feel like it would be a
        # little more user-friendly

    def getMoney(self):
        pass

    def playerName(self):
        return self.__player

    def getLevel(self):
        pass

    ### SETTERS ###

    def lvlUp(self):
        self.__level += 1

    def addAttack(self):
        pass


class monster(SentientBeing):
    
    ### CONSTRUCTOR ###
    def __init__(self,experience, health, species, attacks, armor):
        super().__init__(experience, health, species, attacks, armor)


def dice(quantity, sides):
    # look into making functions of 1 or 2 parameters
    # in this case, it would assume 1 die if there were 1 parameter given
    dice = []
    total = 0

    for i in range(quantity):
        roll = randint(1, sides)
        dice.append(str(roll))
        total += roll

    print('Rolls:', ' '.join(dice))
    print('Sum:', total)
    return total


def newChar():
    # The input function always returns a string, so we will need to convert all of
    # the variables to the desired types. Also, I think experience is a float.
    print("Begin new character construction.\n")

    player = input("What is the player name? (enter a string) ")
    level = input("What level is the character? (enter an integer)" )
    experience = input("How much experience does the character have? (enter an integer)")
    health = input("How much base health does the character have? (enter an integer) ")
    species = input("What species is the character? (enter a string) ")

    armor = 9
    aCont = y
    while aCont == y:
        armor = input("What armor does the character have? (enter armor class (integer 2 - 9)) ")
        if armor >= 2 and armor <= 9:
            aCont = n

    money = input("How much money does your character have? (enter an integer) ")

    attacks = {}
    print("You will need to set your attacks separately using addAttack() .")
    print('Append the character to charList so that it is saved.')
    return character(player, level, experience, health, species, armor, money, attacks)

def save():
    """Disclaimer: I wrote this in github and did not test the code"""
    filename = input('Filename: ')
    fh = open(filename,'w')
    
    fh.write('CHARS\n')
    for char in charList:
        attacks = ''
        for key in char.getAttacks():
            attacks += key + ',' + char.getAttacks()[key] + ';'
        attacks = attacks[:-1]

        #Rachel, I think this was the order of things you wanted. Can you verify?
        attributes = [char.playerName(), str(char.getLevel()), str(char.getExp()),
                      str(char.getHealth())[1:-1], char.getSpecies(),
                      str(char.getArmor()), str(char.getMoney())[1:-1], attacks]
        fh.write(':'.join(attributes)+'\n')
        
    fh.write('ENDCHARS\n')
    
    fh.close()

def load():
    filename = input('Filename: ')
    fh = open(filename, 'r')
    
    line = fh.readline() #should say CHARS
    while True:
        line = fh.readline()
        if 'ENDCHARS' in line: break #I think saying while 'END' not in line would be off by 1

        #dict making examples: https://docs.python.org/3/library/stdtypes.html#dict
    
    fh.close()

def newMonster():
    # experience, health, species, attacks, armor
    pass

def combat(characters, monsters):
    pass
