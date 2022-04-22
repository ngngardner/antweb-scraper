"""antweb_scraper main entrypoint."""

from pathlib import Path

import pandas as pd

from antweb_scraper import const
from antweb_scraper.console import console
from antweb_scraper.core.result import AntInfo


def download_image(
    idx: int,
    genus: str,
    species: str,
    subspecies: str,
    path: str = const.OUT_PATH,
):
    """Download ant specimen picture as tif file.

    Args:
        idx (int): index of ant
        genus (str): genus name
        species (str): species name
        subspecies (str): subspecies name
        path (str): path to store picture
    """
    image_path = '{0}/images/{1}.tif'.format(path, idx)
    Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    if not Path(image_path).exists():
        ant_info = AntInfo(genus, species, subspecies)
        ant_info.download()


def main():
    """Run main program."""
    console.log('Antweb Scraper')
    image_path = '{0}/images'.format(const.OUT_PATH)
    Path(image_path).mkdir(parents=True, exist_ok=True)

    excel = pd.read_excel('{0}/all.xlsx'.format(const.IN_PATH))
    for idx, row in excel.iterrows():
        # filter non alphanumeric characters
        genus = row['Genus']
        genus = ''.join(ch for ch in genus if ch.isalnum())
        species = row['Species']
        subspecies = row['Sub_Species']

        if pd.isnull(subspecies):
            subspecies = ''

        download_image(idx, genus, species, subspecies)
    console.log('Done')


if __name__ == '__main__':
    main()
