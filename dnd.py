##### BRAINSTORM #####
# colored output, look into termcolor module?
# monster class
# --probably similar to characters, but don't need nearly as much detail
# --health, armor, attacks, maybe something else?
# weapon class
# supplies in dictionary where value is quantity
# easier commands (such as >>>2d4 instead of >>>dice(2,4)
# read in campaigns from encrypted files (via DM's password) w/ checksum
# extensive help pages & explanations
# combat function/class?
# --rolling for initiative for all characters & monsters
# --giving characters selection of weapons to use, via arrow key selection?
# --allow characters to fight each other
# --need to consider position in dungeon/when monsters enter combat?
# keep track of in-game date & time, announce when characters must eat/rest
# keep track of real life date & time to tag notes & name save files
####################

from random import randint


class SentientBeing:
    '''Constructor'''
    def __init__(self, health, weapon, armor):
        self.__health = health
        self.__weapon = weapon
        self.__armor = armor

    '''Getters'''
    def getHealth(self):
        return self.__health

    def getArmor(self):
        return self.__armor

    def getWeapon(self):
        return self.__weapon

    '''Setters?'''
    def attack(self, being):
        wDam = self.__weapon.getDamage()
        bArm = being.getArmor()
        if wDam > bArm:
            being.__health = being.__health - wDam + bArm
            # this is assuming armor only blocks a set amount of damage
        elif wDam <= bArm:
            pass
            # basically it does no damage but you don't want to add health like above


class character(SentientBeing):
    '''Constructor'''
    def __init__(self):
        # make a variable for the name?
        self.__Class = input("What creature class is your character?")
        self.__level = input("What level is your character?")
        self.__health = input("How much health does your character have?")
        self.__armor = input("What armor does your character have?")
        self.__weapon = input("What weapon does your character have?")  # weapon should be a weapon class object

        super().__init__(self.__health, self.__weapon, self.__armor)

        # everything else on a character sheet: alignment, 6 physical attributes,
        # experience (linked to lvlUp), health, $ (in different denominations),
        # abilities and magic, supplies, armor class, character notes, species

    '''Getters'''
    def chrSheet(self):
        pass
        # print out a character sheet nicely (centered name, etc.)

    '''Setters'''
    def lvlUp(self):
        self.__level += 1


class monster(SentientBeing):
    '''Constructor'''
    def __init__(self, health, weapon, armor):
        super().__init__(health, weapon, armor)


class weapon:
    '''Constructor'''
    def __init__(self, attacks, damage):
        self.__attacks = attacks
        self.__damage = damage

    '''Getters'''
    def getAttacks(self):
        return self.__attacks

    def getDamage(self):
        return self.__damage


# class armor(self, )


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
