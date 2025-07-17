from __future__ import annotations
from typing import TYPE_CHECKING
from Engine.Program import Program
import inspect


class ScriptObject:
    """A base class for scriptable objects."""

    def __init__(self, parent) -> None:
        assert parent is not None, "Parent cannot be None"
        assert hasattr(parent, "scripts"), "Parent must have a 'scripts' attribute"

        self.parent = parent
        parent.scripts.append(self)

    def update(self, _, delta: float) -> None:
        """Update method to be overridden by subclasses."""
        pass


class DeltaValue(ScriptObject):
    """A class to represent a delta affected value.

    Attributes:
        value (float): The value of the delta.
        is_delta (bool): A flag indicating if the value is a delta.
    """

    def __init__(self, parent, value: float) -> None:
        super().__init__(parent)
        self._value = value
        self.delta_value = 0.0
        self.delta = 0.0

        game = Program()
        game.scripts.append(self)

    def get(self) -> float:
        """Get the value of the delta."""
        return self.delta_value

    def update(self, _, delta: float, tick) -> None:
        """Update the delta value."""
        self.delta = delta
        self.delta_value = self._value * self.delta

        # print("Reactive delta value:", self.delta_value)

    def __float__(self) -> float:
        """Return the delta value when the object is used as a float."""
        return self.delta_value

    def __int__(self) -> int:
        """Return the delta value as an integer when the object is used as an int."""
        return int(self.delta_value)

    def __repr__(self) -> str:
        """Return a string representation of the DeltaValue object."""
        return f"DeltaValue(delta_value={self.delta_value}, true_value={self._value})"

    def __eq__(self, other: float) -> bool:
        """Check equality with another value."""
        return self.delta_value == other

    def __ne__(self, other: float) -> bool:
        """Check inequality with another value."""
        return self.delta_value != other

    def __lt__(self, other: float) -> bool:
        """Check if less than another value."""
        return self.delta_value < other

    def __le__(self, other: float) -> bool:
        """Check if less than or equal to another value."""
        return self.delta_value <= other

    def __gt__(self, other: float) -> bool:
        """Check if greater than another value."""
        return self.delta_value > other

    def __ge__(self, other: float) -> bool:
        """Check if greater than or equal to another value."""
        return self.delta_value >= other

    @property
    def true_value(self) -> float:
        """Get the true value of the delta."""
        return self._value

    @true_value.setter
    def true_value(self, value: float) -> None:
        """Set the true value of the delta."""
        self._value = value

    def set(self, value: float) -> None:
        """Set the delta value."""
        self._value = value

    def __add__(self, other: float) -> float:
        return self.delta_value + other

    def __sub__(self, other: float) -> float:
        return self.delta_value - other

    def __rsub__(self, other: float) -> float:
        return other - self.delta_value

    def __radd__(self, other: float) -> float:
        return other + self.delta_value

    def __mul__(self, other: float) -> float:
        return self.delta_value * other

    def __truediv__(self, other: float) -> float:
        print("Dividing delta value:", self.delta_value, "by", other)
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return self.delta_value / other

    def __rmul__(self, other: float) -> float:
        print("Multiplying delta value:", self.delta_value, "with", other)
        return self.delta_value * other

    def __floordiv__(self, other: float) -> float:
        print("Floor dividing delta value:", self.delta_value, "by", other)
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return self.delta_value // other
