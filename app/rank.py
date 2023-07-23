from enum import Enum


class Tiers(Enum):
    IRON = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    PLATINUM = 5
    EMERALD = 6
    DIAMOND = 7
    MASTER = 8
    GRANDMASTER = 9
    CHALLENGER = 10

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return (self.value < other.value) or (self.value == other.value)
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return (self.value > other.value) or (self.value == other.value)
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class Divisions(Enum):
    IV = 1
    III = 2
    II = 3
    I = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return (self.value < other.value) or (self.value == other.value)
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return (self.value > other.value) or (self.value == other.value)
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class Rank:
    def __init__(self, tier, division, lp):
        self.tier = Tiers[tier]
        self.division = Divisions[division]
        self.lp = lp

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.tier < other.tier:
                return True
            elif self.tier == other.tier:
                if self.division < other.division:
                    return True
                elif self.division == other.division:
                    if self.lp < other.lp:
                        return True
            return False
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            if self.tier > other.tier:
                return True
            elif self.tier == other.tier:
                if self.division > other.division:
                    return True
                elif self.division == other.division:
                    if self.lp > other.lp:
                        return True
            return False
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if self.tier == other.tier:
                if self.division == other.division:
                    if self.lp == other.lp:
                        return True
            return False
        return NotImplemented

    def __str__(self):
        return self.tier.name + ' ' + self.division.name + ' ' + str(self.lp) + 'LP'
