"""Get and store ant specimen information."""

import requests

from antweb_scraper import const
from antweb_scraper.core.metadata import SpecimenInfo, get_name
from antweb_scraper.core.picture import Author, get_author, get_pic


class AntInfo(object):
    """Store ant speciment result info."""

    specimen: SpecimenInfo
    author: Author

    def __init__(self, genus: str, species: str, subspecies: str):
        """Initialize ant info.

        Args:
            genus (str): genus name
            species (str): species name
            subspecies (str): subspecies name
        """
        self.specimen = SpecimenInfo(genus, species, subspecies)
        self.name = get_name(self.specimen)

        self.author = get_author(self.name)
        self.pic_url = get_pic(self.name)

    def cc_license(self) -> str:
        """Build CC license string for image use.

        Returns:
            str: CC license string
        """
        return '{0} by {1}, from {2}, is licensed under {3}.'.format(
            self.name,
            self.author.name,
            self.author.url,
            'CC BY 4.0',
        )

    def download(self, path: str = const.OUTPUT_PATH):
        """Download ant specimen picture as tif file.

        Args:
            path (str): path to store picture
        """
        resp = requests.get(self.pic_url, stream=True)
        out = '{0}/{1}.tif'.format(path, self.name)
        with open(out, 'wb') as fi:
            for chunk in resp:
                fi.write(chunk)
