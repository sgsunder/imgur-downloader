from __future__ import annotations

import logging
import os
import re
import requests
from typing import List, Dict

from tqdm import tqdm


logger = logging.getLogger(__name__)


class ImgurImage(object):
    def __init__(self, hashid: str, url: str, mime: str):
        self.hashid = hashid
        self.url = url
        self.mime = mime

    def download(self, destfile: str) -> None:
        response = requests.get(self.url)
        if response.status_code != 200:
            raise RuntimeError(
                'Fetching Image resulted in '
                + 'status code %d' % response.status_code)
        with open(destfile, 'wb') as f:
            for chunk in response:
                f.write(chunk)
        logger.debug('Fetched %s to %s' % (self.url, destfile))

    def extension(self) -> str:
        if self.mime == 'image/jpeg':
            return 'jpg'
        if self.mime == 'image/png':
            return 'png'
        if self.mime == 'image/gif':
            return 'gif'
        assert False


class ImgurAlbum(object):
    def __init__(self, hashid: str, title: str, images: List[ImgurImage]):
        self.hashid = hashid
        self.title = title
        self.images = images

    def from_api(clientid: str, url: str) -> ImgurAlbum:
        # Check URL format
        match = re.search(r'imgur\.com/a/([\w]*)$', url)
        if not match:
            raise ValueError('Improper Imgur URL: %s' % url)
        assert match.groups()
        albumid = match.groups()[0]

        # Call API
        response = requests.get(
            'https://api.imgur.com/3/album/%s' % albumid,
            headers={
                'Accept': 'application/json',
                'Authorization': 'Client-ID %s' % clientid,
            },
        ).json()

        if not response['success']:
            raise RuntimeError('Something went wrong at Imgur\'s end')

        # Process Data
        return ImgurAlbum(
            hashid=response['data']['id'],
            title=response['data']['title'],
            images=list(map(
                lambda d: ImgurImage(
                    hashid=d['id'],
                    url=d['link'],
                    mime=d['type']
                ),
                response['data']['images']
            )),
        )

    def download(self, destdir: str, progressbar: bool = False) -> None:
        if not os.path.isdir(destdir):
            raise ValueError('Directory %s does not exist' % destdir)

        albumpath = os.path.join(
            destdir, self.title or 'Imgur - %s' % self.hashid)
        try:
            logger.debug('Saving to directory %s' % albumpath)
            os.mkdir(albumpath)
        except OSError as e:
            pass

        if progressbar:
            bf = '{l_bar}{bar}| {n_fmt}/{total_fmt} @{rate_fmt}{postfix}'
            pb = tqdm(total=len(self.images), bar_format=bf)
            pb.set_description(self.hashid)

        for index, image in enumerate(self.images):
            filename = '%03d_%s.%s' % (
                index + 1, image.hashid, image.extension())
            if progressbar:
                pb.set_postfix(image=image.hashid)
            path = os.path.join(albumpath, filename)
            image.download(path)
            if progressbar:
                pb.update()

        if progressbar:
            pb.close()
