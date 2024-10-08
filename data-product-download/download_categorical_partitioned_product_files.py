# import requests library to call API endpoint
import random
import requests
import time

# set key and API endpoint variables
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

# method to handle different responses including retries
def make_request(
    url, params = None, retry_count = 0, max_retries = 6, backoff_factor = 2, jitter_max = 2.0
):
    kwargs = {
        'headers': {
            'X-API-KEY': API_KEY,
            'Content-Type': 'application/json'
        }
    }
    if params is not None:
        kwargs['params'] = params

    response = requests.get(url, **kwargs)

    if response.status_code == 429 and retry_count < max_retries:
        retry_count += 1
        base_sleep_time = backoff_factor ** (retry_count - 1)
        jitter = random.uniform(0, jitter_max)
        sleep_time = base_sleep_time + jitter
        print(f'Ratelimit reached, waiting {sleep_time} then retrying with count {retry_count}')
        time.sleep(sleep_time)
        return make_request(url=url, params=params, retry_count=retry_count)

    if response.status_code == 400:
        raise Exception(f'Request failed with {response.status_code}')

    if not (response.status_code >= 200 and response.status_code < 300):
        raise Exception(f'Request failed with {response.status_code} and {response.json()}')

    if response.status_code >= 200 or response.status_code < 300:
        print(f'Request successful')

    return response

# loop through all API result pages, keeping track of number of downloaded files
page = 1
download_count = 0
while True:
    # get results from API endpoint, using API key for authentication
    print(f"Gettings files from page {page}")
    results = make_request(url=PRODUCT_API_PATH,
                           params={'page': page,
                                   'partition_keys': [<partition_value_1>, <partition_value_2>]
                                  }   # set partition key values here
                          )
    response_json = results.json()

    # for each result page, loop through download links and save to your computer
    for link_data in response_json['download_links']:
        print(f"Downloading file {link_data['file_name']}...")
        data = make_request(url=link_data['link'])
        with open(link_data['file_name'], 'wb') as file:
            file.write(data.content)
        download_count += 1

    # only continue if there are more result pages to process
    total_pages = response_json['total_pages']
    if page >= total_pages:
        break
    page += 1

print(f"Successfully downloaded {download_count} files.")
