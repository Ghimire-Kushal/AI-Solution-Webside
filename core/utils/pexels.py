import json
import urllib.parse
import urllib.request

from django.core.files.base import ContentFile
from decouple import config

PEXELS_API_KEY = config('PEXELS_API_KEY', default='')
PEXELS_SEARCH_URL = 'https://api.pexels.com/v1/search'


def search_pexels(query, per_page=12, page=1):
    """Search Pexels and return a list of photo dicts."""
    if not PEXELS_API_KEY:
        return []

    url = (
        f'{PEXELS_SEARCH_URL}?query={urllib.parse.quote(query)}'
        f'&per_page={per_page}&page={page}&orientation=landscape'
    )
    req = urllib.request.Request(url, headers={
        'Authorization': PEXELS_API_KEY,
        'User-Agent': 'Mozilla/5.0 (compatible; AI-Solutions/1.0)',
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        photos = []
        for p in data.get('photos', []):
            photos.append({
                'id': p['id'],
                'thumb': p['src']['medium'],
                'large': p['src']['large'],
                'photographer': p['photographer'],
                'url': p['url'],
                'alt': p.get('alt', query),
            })
        return photos
    except Exception:
        return []


def download_pexels_image(photo_url, filename):
    """Download a Pexels image and return a Django ContentFile."""
    req = urllib.request.Request(photo_url, headers={
        'User-Agent': 'Mozilla/5.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        return ContentFile(data, name=filename)
    except Exception:
        return None
