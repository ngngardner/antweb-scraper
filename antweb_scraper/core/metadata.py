"""Get ant specimen metadata."""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from antweb_scraper import const
from antweb_scraper.core.models import SpecimenInfo


@dataclass
class ImagesPayload(object):
    """Store images information for requests."""

    genus: str
    species: str
    rank: str = 'species'
    project: str = 'allantwebants'


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
    resp = requests.get(const.IMAGES_URL, params=dict(payload))
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
