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

# get results from API endpoint, using API key for authentication
results = make_request(url=PRODUCT_API_PATH,
                       params={'page': 1, # only getting 1st page of results
                               'partition_key_after': '1900-01-01', # set date value here, exclude if product is not date-partitioned
                               'partition_key_before': '2099-01-01'} # set date value here, exclude if product is not date-partitioned
                      )

download_count = 0
# loop through download links and save to your computer
for i, link_data in enumerate(results.json()["download_links"]):
    print(f"Downloading file {i}...")
    data = make_request(url=link_data["link"])
    open(link_data["file_name"], 'wb').write(data.content)
    download_count += 1

print(f"Successfully downloaded {download_count} files.")
