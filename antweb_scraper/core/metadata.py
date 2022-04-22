"""Get ant specimen metadata."""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from antweb_scraper import const


@dataclass
class SpecimenInfo(object):
    """Store ant specimen information."""

    genus: str
    species: str
    subspecies: str

    def __repr__(self) -> str:
        """Return string representation of specimen info.

        Returns:
            str: string representation of specimen info
        """
        return '{0} {1} {2}'.format(self.genus, self.species, self.subspecies)


@dataclass
class ImagesPayload(object):
    """Store images information for requests."""

    genus: str
    species: str
    rank: str = 'species'
    project: str = 'allantwebants'

    def asdict(self) -> dict:
        """Return dictionary of images payload.

        Returns: 
            dict: images payload
        """
        return {
            'genus': self.genus,
            'species': self.species,
            'rank': self.rank,
            'project': self.project,
        }


def images_html(si: SpecimenInfo) -> BeautifulSoup:
    """Get specimen image html.

    Args:
        si (SpecimenInfo): Specimen information.

    Returns:
        BeautifulSoup: Specimen image html.
    """
    payload = ImagesPayload(
        genus=si.genus,
        species=si.species,
    )
    resp = requests.get(const.IMAGES_URL, params=payload.asdict())
    return BeautifulSoup(resp.text, 'html.parser')


def get_name(si: SpecimenInfo) -> str:
    """Get specimen name from image html metadata.

    Args:
        si (SpecimenInfo): Specimen information.

    Returns:
        str: Specimen name.
    """
    soup = images_html(si)
    div = soup.find('div', {'class': 'name'})

    if div is None:
        return ''

    return str(div.text).strip()
