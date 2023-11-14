# amplifydata-public

This repo holds directions and utilities for how to interact with [Amplify Data's](https://www.amplifydata.io/) public facing utilities (like the data API).

# Data API

The Data API allows you to programmatically download data products from any data portal powered by [Amplify](https://www.amplifydata.io/). To download a data product, follow these steps:
1. Generate an API Key by creating an API Connection in the Connections tray (be sure to save it before use) - this will look similar to `gddmanPX.jDGupTCuLR0wJXqUIe8ysakBsfHajFblQyPPLEUpFDCxGbDF2Xq4fpbb`
2. Generate the API Endpoint by subscribing to the data product with the Connect to API option - this will look similar to `https://dev.amplifydata.io/external-api/v3/products/ec9b12fb-e306-4856-8ec2-b0b2f570e00b/files`
3. Call the API Endpoint as needed with your API key to generate a list of file links
4. Download the file(s) from the generated links

## Sample Code in Python

### V3 Endpoint

#### Calling the API
```python
import requests
 
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

results = requests.get(url=PRODUCT_API_PATH,
                       params={<optional API parameters>},
                       headers={
                        "X-API-KEY": API_KEY,
                        'accept': 'application/json'
                       })
print(results.json())
```

#### API Parameters:

- `page`: Page number (API will return maximum of 1000 files per page), defaulted to 1
- `partition_key_after`: Filtering parameter to retrieve all files after the specified partition_key, inclusive
- `partition_key_before`: Filtering parameter to retrieve all files before the specified partition_key, inclusive

#### Endpoint Results:
```python
{
    "download_links": [{
        "link": str, # downloadable link
        "partition_key": str, # the partition str used to partition the links. Can be used for filtering, example provided below. Will be None if no file partitioning set
        "file_name": str, # name of file
        "file_extension": str, # .csv or .csv.gz - indicating if files are compressed.  Larger products will be delivered via compressed files
        "file_size_bytes": int, # size of downloaded file in bytes
        "modified_at": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'" # UTC datetime when file was last modified
    }], # list of downloadable links and partition_keys
    "page": int, # defaulted to 1, the page offset number to retrieve the links for maximum of 1000 links per page
    "number_of_files_for_page": int, # num of files for page after filter and pagination
    "avg_file_size_for_page": float, # avg file size in bytes for page after filter and pagination
    "partition_column": str, # partition column name used to partition the links. Will be None if no file partitioning set
    "total_files": int, # total number of files after filter
    "total_pages": int, # total number of pages after filter
    "total_size": int, # total file size in bytes after filter
    "expires_at": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'" # UTC datetime
}
```
#### Download first page of files (up to 1000 files)
```python
# import requests library to call API endpoint
import requests

# set key and API endpoint variables
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

# get results from API endpoint, using API key for authentication
results = requests.get(url=PRODUCT_API_PATH,
                       params={'page': 1}, # only getting 1st page of results
                       headers={'X-API-KEY': API_KEY,
                                'accept': 'application/json'
                               })

# loop through download links and save to your computer
for i, link_data in enumerate(results.json()["download_links"]):
    print(f"Downloading file {i}...")
    data = requests.get(link_data["link"])
    open(link_data["file_name"], 'wb').write(data.content)

```

#### Download all files
```python
# import requests library to call API endpoint
import requests

# set key and API endpoint variables
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

# loop through all API result pages, keeping track of number of downloaded files
page = 1
download_count = 0
while True:
    # get results from API endpoint, using API key for authentication, for a specific page
    results = requests.get(url=PRODUCT_API_PATH,
                           params={'page': page},
                           headers={'X-API-KEY': API_KEY,
                                    'accept': 'application/json'
                                   })
    response_json = results.json()

    # for each result page, loop through download links and save to your computer
    for link_data in response_json['download_links']:
        print(f"Downloading file {link_data['file_name']}...")
        data = requests.get(link_data['link'])
        with open(link_data['file_name'], 'wb') as file:
            file.write(data.content)
        download_count += 1

    # only continue if there are more result pages to process
    total_pages = response_json['total_pages']
    if page >= total_pages:
        break
    page += 1

print(f"Successfully downloaded {download_count} files.")
```

#### Download specific files using date filters
Filtering Parameters:

- `partition_key_after`: Retrieve file links for data at or after the specified date in YYYY-MM-DD format
- `partition_key_before`: Retrieve file links for data at or before the specified date in YYYY-MM-DD format

```python
# import requests library to call API endpoint
import requests

# set key and API endpoint variables
API_KEY = <key generated by step 1>
PRODUCT_API_PATH = <URL generated by step 2>

# loop through all API result pages, keeping track of number of downloaded files
page = 1
download_count = 0
while True:
    # get results from API endpoint, using API key for authentication
    results = requests.get(url=PRODUCT_API_PATH,
                           params={'page': page,
                                   'partition_key_after': <'YYYY-MM-DD'>,   # optionally set date value here
                                   'partition_key_before': <'YYYY-MM-DD'>}, # optionally set date value here
                           headers={'X-API-KEY': API_KEY,
                                    'accept': 'application/json'
                                   })
    response_json = results.json()

    # for each result page, loop through download links and save to your computer
    for link_data in response_json['download_links']:
        print(f"Downloading file {link_data['file_name']}...")
        data = requests.get(link_data['link'])
        with open(link_data['file_name'], 'wb') as file:
            file.write(data.content)
        download_count += 1

    # only continue if there are more result pages to process
    total_pages = response_json['total_pages']
    if page >= total_pages:
        break
    page += 1

print(f"Successfully downloaded {download_count} files.")
```

