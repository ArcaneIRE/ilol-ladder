import logging
from enum import Enum

logger = logging.getLogger(__name__)


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
    I = 4  # noqa: E741

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
        logger.info(f"Rank created: {self}")

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            result = (self.tier < other.tier) or (self.tier == other.tier and self.division < other.division) or (self.tier == other.tier and self.division == other.division and self.lp < other.lp)
            logger.debug(f"Comparing {self} < {other}: {result}")
            return result
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            result = (self.tier > other.tier) or (self.tier == other.tier and self.division > other.division) or (self.tier == other.tier and self.division == other.division and self.lp > other.lp)
            logger.debug(f"Comparing {self} > {other}: {result}")
            return result
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            result = self.tier == other.tier and self.division == other.division and self.lp == other.lp
            logger.debug(f"Comparing {self} == {other}: {result}")
            return result
        return NotImplemented

    def __str__(self):
        return self.tier.name + ' ' + self.division.name + ' ' + str(self.lp) + 'LP'
