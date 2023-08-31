# amplifydata-public

This repo holds directions and utilities for how to interact with [Amplify Data's](https://www.amplifydata.io/) public facing utilities (like the data API).

# Data API

The Data API allows you to programmatically download data products from any data portal powered by [Amplify](https://www.amplifydata.io/). To download a data product, follow these steps:
1. Generate an API key by creating an API Connection in the Connections tray
2. Generate the API URL by subscribing to the data product with the API option
3. Call the V2 API URL with your API key to generate a list of file links
4. Download the file(s) from the generated links

## Sample Code in Python

### V2 Endpoint

#### Calling the API
```python
import requests
 
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

results = requests.get(url=PRODUCT_API_PATH,
                       headers={
                        "X-API-KEY": API_KEY,
                        'accept': 'application/json'
                       })
print(results.json())
```
#### Results:
```python
{
    "download_links": [str], # list of downloadable links
    "metadata": {
        "num_files": int,
        "total_size_mb": float,
        "avg_file_size_mb": float,
        "expires_at": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'" # UTC datetime
    }
}
```
#### Download all files
```python
for i, link in enumerate(results.json()["download_links"]):
    print(f"Downloading file {i}...")
    data = requests.get(link)
    open(f'file-{i}.csv.gz', 'wb').write(data.content)
```

### V3 Endpoint

#### New in V3 - API Parameters:

- `page`: Pagination parameter for the page offset number to retrieve the files for maximum of 1000 files per page, defaulted to 1.
- `partition_key_after`: Filtering parameter to retrieve all files after the specified partition_key, inclusive
- `partition_key_before`: Filtering parameter to retrieve all files before the specified partition_key, inclusive

#### Endpoint Results:
```python
{
    "download_links": [{
        "link": str, # downloadable link
        "partition_key": str, # the partition str used to partition the links. Can be used for filtering, example provided below
    }], # list of downloadable links and partition_keys
    "page": int, # defaulted to 1, the page offset number to retrieve the links for maximum of 1000 links per page
    "number_of_files_for_page": int, # num of files for page after filter and pagination
    "avg_file_size_for_page": float, # avg file size in bytes for page after filter and pagination
    "partition_column": str, # partition column name used to partition the links
    "total_files": int, # total number of files after filter
    "total_pages": int, # total number of pages after filter
    "total_size": int, # total file size in bytes after filter
    "expires_at": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'" # UTC datetime
}
```

#### Download all files
```python
import requests

API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

page = 1
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json'
}

def download_file(link, index):
    print(f'Downloading file {index}...')
    data = requests.get(link)
    with open(f'file-{index}.csv.gz', 'wb') as file:
        file.write(data.content)

download_count = 0
while True:
    results = requests.get(url=PRODUCT_API_PATH, params={'page': page}, headers=headers)
    response_json = results.json()

    for link in response_json['download_links']:
        download_file(link['link'], download_count)
        download_count += 1

    total_pages = response_json.get('total_pages')
    if page >= total_pages:
        break

    page += 1

print(f"Successfully downloaded {download_count} files.")
```

#### Download files for the first 10 pages
```python
import requests

API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

page_limit = 10
page = 1
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json'
}

def download_file(link, index):
    print(f'Downloading file {index}...')
    data = requests.get(link)
    with open(f'file-{index}.csv.gz', 'wb') as file:
        file.write(data.content)

download_count = 0
while True:
    results = requests.get(url=PRODUCT_API_PATH, params={'page': page}, headers=headers)
    response_json = results.json()

    for link in response_json['download_links']:
        download_file(link['link'], download_count)
        download_count += 1

    total_pages = response_json.get('total_pages')
    if page >= total_pages or page >= page_limit:
        break

    page += 1

print(f"Successfully downloaded {download_count} files.")
```

#### Filtering
Filtering Parameters:

- `partition_key_after`: Retrieve all links after the specified partition_key, inclusive
- `partition_key_before`: Retrieve all links before the specified partition_key, inclusive

```python
import requests

API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

page = 1
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json'
}

partition_key_after = '2017-01-01'
partition_key_before = '2023-01-01'

def download_file(link, index):
    print(f'Downloading file {index}...')
    data = requests.get(link)
    with open(f'file-{index}.csv.gz', 'wb') as file:
        file.write(data.content)

download_count = 0
while True:
    results = requests.get(
        url=PRODUCT_API_PATH,
        params={
            'page': page,
            'partition_key_after': partition_key_after,
            'partition_key_before': partition_key_before
        },
        headers=headers
    )
    response_json = results.json()

    for link in response_json['download_links']:
        download_file(link['link'], download_count)
        download_count += 1

    total_pages = response_json.get('total_pages')
    if page >= total_pages:
        break

    page += 1

print(f"Successfully downloaded {download_count} files.")
```
