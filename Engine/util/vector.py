from typing import overload
import pygame

pygame.Vector2.__truediv__


class Vector2(pygame.Vector2):
    """
    A superset of pygame.Vector2 with additional functionality.
    """

    def toDict(self):
        """Convert the vector to a dictionary."""
        return {"x": self.x, "y": self.y}

    def toList(self):
        """Convert the vector to a list."""
        return [self.x, self.y]

    def toTuple(self):
        """Convert the vector to a tuple."""
        return (self.x, self.y)

    def toSet(self):
        """Convert the vector to a set."""
        return {self.x, self.y}

    def __truediv__(self, value: any) -> "Vector2":
        """Divide the vector by a scalar value."""

        if isinstance(value, pygame.Vector2):
            return Vector2(self.x / value.x, self.y / value.y)
        elif isinstance(value, (int, float)):
            return Vector2(self.x / value, self.y / value)


class Vector3(pygame.Vector3):
    """
    A superset of pygame.Vector3 with additional functionality.
    """

    def toDict(self):
        """Convert the vector to a dictionary."""
        return {"x": self.x, "y": self.y, "z": self.z}

    def toList(self):
        """Convert the vector to a list."""
        return [self.x, self.y, self.z]

    def toTuple(self):
        """Convert the vector to a tuple."""
        return (self.x, self.y, self.z)

    def toSet(self):
        """Convert the vector to a set."""
        return {self.x, self.y, self.z}


def setToVector(set: set):
    """Convert a set to a vector."""
    if len(set) == 0:
        raise ValueError("Set cannot be empty.")

    if len(set) == 1:
        return Vector2(list(set)[0], 0)
    elif len(set) == 2:
        return Vector2(list(set)[0], list(set)[1])
    elif len(set) == 3:
        return Vector3(list(set)[0], list(set)[1], list(set)[2])
    else:
        raise ValueError("Set must have 1, 2 or 3 elements.")


def tupleToVector(tuple: tuple):
    """Convert a tuple to a vector."""
    if len(tuple) == 0:
        raise ValueError("Tuple cannot be empty.")

    if len(tuple) == 1:
        return Vector2(tuple[0], 0)
    elif len(tuple) == 2:
        return Vector2(tuple[0], tuple[1])
    elif len(tuple) == 3:
        return Vector3(tuple[0], tuple[1], tuple[2])
    else:
        raise ValueError("Tuple must have 1, 2 or 3 elements.")


def listToVector(list: list):
    """Convert a list to a vector."""
    if len(list) == 0:
        raise ValueError("List cannot be empty.")

    if len(list) == 1:
        return Vector2(list[0], 0)
    elif len(list) == 2:
        return Vector2(list[0], list[1])
    elif len(list) == 3:
        return Vector3(list[0], list[1], list[2])
    else:
        raise ValueError("List must have 1, 2 or 3 elements.")


def dictToVector(dict: dict):
    """
    Convert a dictionary to a vector.
    The dictionary must contain "x" and "y" keys.
    """
    if dict.keys().__len__() == 0:
        raise ValueError("Dictionary cannot be empty.")

    keys = dict.keys()
    if "x" in keys and "y" in keys and "z" in keys:
        return Vector3(dict["x"], dict["y"], dict["z"])
    elif "x" in keys and "y" in keys:
        return Vector2(dict["x"], dict["y"])
    elif "x" in keys and "z" in keys:
        return Vector2(dict["x"], dict["z"])
    elif "y" in keys and "z" in keys:
        return Vector2(dict["y"], dict["z"])
    else:
        raise ValueError("Dictionary must have 'x' and 'y' or 'z' keys.")


def vectorToList(vector):
    """Convert a vector to a list."""
    return list(vector)


def vectorToTuple(vector):
    """Convert a vector to a tuple."""
    return tuple(vector)


def vectorToDict(vector):
    """Convert a vector to a dictionary."""
    return {"x": vector.x, "y": vector.y}


def toVector(value):
    """Convert a value to a vector."""
    if isinstance(value, pygame.Vector2) or isinstance(value, pygame.Vector3):
        return value

    elif isinstance(value, tuple):
        return tupleToVector(value)
    elif isinstance(value, list):
        return listToVector(value)
    elif isinstance(value, dict):
        return dictToVector(value)
    elif isinstance(value, set):
        return setToVector(value)
    else:
        raise ValueError("Value must be a vector, tuple, list or dictionary.")
