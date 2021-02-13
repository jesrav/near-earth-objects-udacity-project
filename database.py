"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from typing import List, Union

from filters import (
    DateFilter,
    VelocityFilter,
    DiameterFilter,
    DistanceFilter,
    HazardousFilter,
)
from models import NearEarthObject, CloseApproach


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(
        self,
        neos: List[NearEarthObject],
        approaches: List[CloseApproach],
    ):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # Mappings to make fetching the near earth and close encounter objects easier.
        self._designation_neo_map = {}
        self._name_neo_map = {}
        for neo in neos:
            self._designation_neo_map[neo.designation] = neo
            self._name_neo_map[neo.name] = neo

        self._designation_approaches_map = {}
        for approach in approaches:
            if approach._designation in self._designation_approaches_map:
                self._designation_approaches_map[approach._designation].append(approach)
            else:
                self._designation_approaches_map[approach._designation] = [approach]

        # Link near earth objects and close encounter objects.
        for neo in self._neos:
            neo.approaches = self._designation_approaches_map.get(neo.designation, [])

        for approach in self._approaches:
            approach.neo = self._designation_neo_map.get(approach._designation, None)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self._designation_neo_map.get(designation, None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        try:
            return self._name_neo_map.get(name, None)
        except KeyError:
            raise ValueError(f"There is no near earth object with the name {name}")

    def query(
        self,
        filters=List[
            Union[
                DateFilter,
                VelocityFilter,
                DiameterFilter,
                DistanceFilter,
                HazardousFilter,
            ]
        ],
    ):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        for approach in self._approaches:
            if all([filter(approach) for filter in filters]):
                yield approach
