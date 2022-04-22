"""Get ant picture related information."""

import re
from dataclasses import dataclass
from typing import Dict, Union

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

from antweb_scraper import const


@dataclass
class PicPayload(object):
    """Store photo_metadata information for requests.

    Uses first headshot by default.
    """

    name: str
    shot: str = 'h'
    number: str = '1'

    def asdict(self) -> Dict[str, str]:
        """Return dictionary of photo_metadata payload.

        Returns:
            dict: photo_metadata payload
        """
        return {
            'name': self.name,
            'shot': self.shot,
            'number': self.number,
        }


@dataclass
class Author(object):
    """Store author information responses."""

    name: str
    url: str


def pic_html(sn: str) -> BeautifulSoup:
    """Get specimen photo_metadata html.

    Args:
        sn (str): Specimen name.

    Returns:
        BeautifulSoup: Specimen photo_metadata html.
    """
    payload = PicPayload(name=sn)
    resp = requests.get(const.PIC_URL, params=payload.asdict())
    return BeautifulSoup(resp.text, 'html.parser')


def get_pic_li(sn: str) -> Union[None, ResultSet]:
    """Get all elements from photo_metadata span.

    Args:
        sn (str): Specimen name.

    Returns:
        ResultSet: All elements from photo_metadata span.
    """
    soup = pic_html(sn)
    span = soup.find('span', {'id': 'photo_metadata'})

    return span.find_all('li') if span is not None else None


def get_pic_url(sn: str) -> str:
    """Get specimen picture url from big_picture div.

    Args:
        sn (str): Specimen name.

    Returns:
        str: Specimen picture url.
    """
    soup = pic_html(sn)
    div = soup.find('div', {'class': 'big_picture'})

    if div is None:
        return ''

    return div.img.get('src')


def get_author(sn: str) -> Dict:
    """Get author name and url.

    Args:
        sn (str): Specimen name.

    Returns:
        Dict: Author name and url.
    """
    li = get_pic_li(sn)
    if li is None:
        return {}
    author_pattern = 'Photographer: '

    name = ''
    url = ''
    for element in li:
        if re.match(author_pattern, element.text):
            name = re.sub(author_pattern, '', element.text)
            url = element.a.get('href')

    return Author(name, url)


def get_pic(sn: str) -> str:
    """Get specimen picture url.

    Args:
        sn (str): Specimen name.

    Returns:
        str: Specimen picture url.
    """
    li = get_pic_li(sn)
    if li is None:
        return ''
    pic_pattern = 'View Highest Resolution'

    url = ''
    for element in li:
        if re.match(pic_pattern, element.text):
            url = element.a.get('href')

    # fallback if no highest resolution url found
    if url is None:
        url = get_pic_url(sn)

    return url
