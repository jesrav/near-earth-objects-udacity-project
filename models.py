"""Represent models for near-Earth objects and their close approaches."""
import math

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.
    """

    def __init__(
        self,
        designation,
        name=None,
        diameter=None,
        hazardous=None,
    ):
        """Create a new `NearEarthObject`.

        :param designation: primary designation of the asteroid or comet
        :param name: IAU name
        :param diameter: Diameter of asteroid or meteor.
        :param hazardous: if the asteroid or meteor is hazardous
        """

        self.designation = designation
        self.name = None if name == "" else str(name)
        self.diameter = float(diameter) if diameter else float("nan")
        self.hazardous = True if hazardous else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        else:
            return f"{self.designation}"

    def serialize(self):
        """Return a dictionary with key attributes of the near earth object."""
        return {
            "designation": self.designation,
            "name": self.name if self.name else "",
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and is potentially hazardous."
        else:
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and is not potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.
    """

    def __init__(
        self,
        designation,
        time,
        distance,
        velocity,
        neo: NearEarthObject = None,
    ):
        """Create a new `CloseApproach`.

        :param neo: A Near earth object.
        :param time: Time of close approach in NASA-formatted calendar date/time format.
        :param distance: Approach distance in astronomical units.
        :param velocity: relative approach velocity in kilometers per second
        """
        self._designation = designation
        self.time = cd_to_datetime(time) if time else None
        self.distance = float(distance) if distance else float("nan")
        self.velocity = float(velocity) if velocity else float("nan")
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return f"{datetime_to_str(self.time)}"

    def serialize(self):
        """Return a dictionary with key attributes of the close approach."""
        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} "
            f"au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
