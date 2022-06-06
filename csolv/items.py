from dataclasses import dataclass
from enum import Enum, unique, auto


@dataclass(eq=True, frozen=True)
class Materia:
    """integer grade of the materia"""
    grade: int
    """flag indicating whether it can only fit the first overmeld slot"""
    advanced: bool


@dataclass(eq=True, frozen=True)
class CraftsmanshipMateria(Materia):
    craftsmanship: int


@dataclass(eq=True, frozen=True)
class ControlMateria(Materia):
    control: int


@dataclass(eq=True, frozen=True)
class CpMateria(Materia):
    cp: int


@unique
class GearSlot(Enum):
    MAINHAND = auto()
    OFFHAND = auto()
    HEAD = auto()
    BODY = auto()
    HANDS = auto()
    LEGS = auto()
    FEET = auto()
    ACCESSORY = auto()
    RING = auto()


@dataclass
class Equipment:
    ilvl: int
    slot: GearSlot
    craftsmanship: int
    max_craftsmanship: int
    control: int
    max_control: int
    cp: int
    max_cp: int
    advanced_melds: int
    melds: list[Materia]

    # def __init__(self):
    #     self._craftsmanship = None
    #     self._control = None
    #     self._cp = None

    def effective_craftsmanship(self) -> int:
        if self._craftsmanship is None:
            self._craftsmanship = 0

        return self._craftsmanship

    def effective_control(self) -> int:
        if self._control is None:
            self._control = 0

        return self._control

    def effective_cp(self) -> int:
        if self._cp is None:
            self._cp = 0

        return self._control


body = {
    'AR-Caean Velvet Work Shirt of Crafting': Equipment(560, GearSlot.BODY, 842, 990, 326, 363, 6, 7, 2, list()),
    'Pactmaker\'s Vest of Crafting': Equipment(590, GearSlot.BODY, 949, 1116, 356, 419, 6, 7, 2, list())
}

CRAFTSMANSHIP_X = CraftsmanshipMateria(10, True, 27)
CRAFTSMANSHIP_IX = CraftsmanshipMateria(9, False, 18)

CRAFTSMANSHIP_MATERIA = {CRAFTSMANSHIP_X, CRAFTSMANSHIP_IX}

CONTROL_X = ControlMateria(10, True, 18)
CONTROL_IX = ControlMateria(9, False, 12)
CONTROL_VIII = ControlMateria(8, True, 13)

CONTROL_MATERIA = {CONTROL_X, CONTROL_IX, CONTROL_VIII}

CP_X = CpMateria(10, True, 10)
CP_IX = CpMateria(9, False, 8)
CP_VII = CpMateria(7, False, 7)

CP_MATERIA = {CP_X, CP_IX, CP_VII}
