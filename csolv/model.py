import math
from dataclasses import dataclass
from functools import reduce

from csolv.items import Equipment


@dataclass
class CrafterLike(object):
    """
    don't actually instantiate; this is just interface documentation
    """
    level: int

    def craftsmanship(self) -> int:
        pass

    def control(self) -> int:
        pass

    def cp(self) -> int:
        pass

    def crafter_level(self) -> int:
        return _LEVEL_TABLE.get(self.level, self.level)


@dataclass
class Recipe:
    name: str
    difficulty: int
    durability: int
    max_quality: int
    base_level: int
    level: int
    progress_divider: int
    progress_modifier: int
    quality_divider: int
    quality_modifier: int

    def base_quality(self, crafter: CrafterLike):
        base = (crafter.control() * 10) / self.quality_divider + 35
        if crafter.crafter_level() <= self.level:
            if self.quality_modifier is None:
                return base
            else:
                return math.floor((base * self.quality_modifier) / 100)
        else:
            return base

    def base_progress(self, crafter: CrafterLike):
        base = (crafter.craftsmanship() * 10) / self.progress_divider + 2
        if crafter.crafter_level() <= self.level:
            if self.progress_modifier is None:
                return base
            else:
                return math.floor((base * self.progress_modifier) / 100)
        else:
            return base


@dataclass
class Crafter(CrafterLike):
    gear: list[Equipment]
    bonus_craftsmanship: int
    bonus_control: int
    bonus_cp: int

    def __init__(self):
        self._craftsmanship = None
        self._control = None
        self._cp = None

    def craftsmanship(self) -> int:
        if self._craftsmanship is None:
            self._craftsmanship = reduce(
                lambda l, r: l + r.effective_craftsmanship(), self.gear, 0)
            self._craftsmanship += self.bonus_craftsmanship

        return self._craftsmanship

    def control(self) -> int:
        if self._control is None:
            self._control = reduce(lambda l, r: l + r.effective_control(),
                                   self.gear, 0)
            self._control += self.bonus_control

        return self._control

    def cp(self) -> int:
        if self._cp is None:
            self._cp = reduce(lambda l, r: l + r.effective_cp(),
                              self.gear, 0)
            self._cp += self.bonus_cp

        return self._cp


@dataclass
class SimpleCrafter(CrafterLike):
    level: int
    _craftsmanship: int
    _control: int
    _cp: int

    def craftsmanship(self) -> int:
        return self._craftsmanship

    def control(self) -> int:
        return self._control

    def cp(self) -> int:
        return self._cp


@dataclass
class Synthesis:
    crafter: CrafterLike
    first_step: bool = True
    invalid: bool = False
    progress_multiplier: float = 0.0
    quality_multiplier: float = 0.0
    inner_quiet: int = 0
    manipulation: int = 0
    muscle_memory: int = 0
    waste_not: int = 0
    durability: int = 0

    def advance(self, synthesis_action=False, quality_action=False):
        if quality_action:
            self.inner_quiet += 1

        if self.manipulation > 0:
            self.manipulation -= 1

        if self.waste_not > 0:
            self.waste_not -= 1

        if synthesis_action:
            self.muscle_memory = 0
        elif self.muscle_memory > 0:
            self.muscle_memory -= 1

        self.first_step = False


@dataclass
class Action:
    name: str
    progress: float
    quality: float
    durability_cost: int

    def get_progress(self, base_progress, synthesis: Synthesis) -> float:
        return math.floor(self.progress * base_progress * synthesis.progress_multiplier)

    def get_quality(self, base_quality, synthesis: Synthesis) -> float:
        return math.floor(self.quality * base_quality * synthesis.quality_multiplier)

    def get_durability_cost(self, synthesis: Synthesis) -> int:
        if synthesis.waste_not > 0:
            return math.floor(self.durability_cost / 2)
        else:
            return self.durability_cost

    def advance(self, base_progress, base_quality, synthesis: Synthesis):
        if synthesis.invalid is True:
            return [-1, -1, -1000]

        result = [
            self.get_progress(base_progress, synthesis),
            self.get_quality(base_quality, synthesis),
            -1 * self.get_durability_cost(synthesis)
        ]

        if synthesis.manipulation > 0:
            result.append(5)

        synthesis.advance(self.progress > 0, self.quality > 0)

        return result


@dataclass
class MuscleMemoryAction(Action):

    def advance(self, base_progress, base_quality, synthesis: Synthesis):
        if synthesis.first_step:
            synthesis.muscle_memory = 5
        else:
            synthesis.invalid = True

        return super().advance(base_progress, base_quality, synthesis)


@dataclass
class GroundworkAction(Action):

    def get_progress(self, base_progress, synthesis: Synthesis) -> float:

        return super().get_progress(base_progress, synthesis)


@dataclass
class SynthAndActions:
    synthesis: Synthesis
    actions: list[Action]


_LEVEL_TABLE = {
    51: 120,
    52: 125,
    53: 130,
    54: 133,
    55: 136,
    56: 139,
    57: 142,
    58: 145,
    59: 148,
    60: 150,
    61: 260,
    62: 265,
    63: 270,
    64: 273,
    65: 276,
    66: 279,
    67: 282,
    68: 285,
    69: 288,
    70: 290,
    71: 390,
    72: 395,
    73: 400,
    74: 403,
    75: 406,
    76: 409,
    77: 412,
    78: 415,
    79: 418,
    80: 420,
    81: 517,
    82: 520,
    83: 525,
    84: 530,
    85: 535,
    86: 540,
    87: 545,
    88: 550,
    89: 555,
    90: 560,
}
