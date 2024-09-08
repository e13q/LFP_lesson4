import requests

import time
from tqdm.auto import tqdm

BASE_URL = 'https://tululu.org'


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.TooManyRedirects


def request_with_retries(url, params=None, retries=3, delay=4):
    for attempt in range(retries):
        try:
            response = requests.get(url, params, timeout=10)
            response.raise_for_status()
            check_for_redirect(response)
            return response
        except (requests.ConnectionError, requests.Timeout):
            tqdm.write(
                f'An attempt to connect {attempt + 1} of {retries} failed'
            )
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                tqdm.write('All attempts have been exhausted.')
                return None
        except requests.exceptions.HTTPError as e:
            tqdm.write(f'HTTPerror {e}')
            return None
        except requests.exceptions.TooManyRedirects:
            tqdm.write(f'Webpage for id {params.get('id')} has been moved')
            return None
        except requests.RequestException as e:
            tqdm.write(f'Request exception: {e}')
            return None
