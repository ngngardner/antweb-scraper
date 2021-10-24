"""Get and store ant specimen information."""

from dataclasses import dataclass


@dataclass
class SpecimenRequestInfo(object):
    """Store ant specimen information."""

    genus: str
    species: str
    subspecies: str
