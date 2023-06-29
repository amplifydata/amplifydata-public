# amplifydata-public

This repo holds directions and utilities for how to interact with [Amplify Data's](https://www.amplifydata.io/) public facing utilities (like the data API).

# Data API

The Data API allows you to programmatically download data products from any data portal powered by [Amplify](https://www.amplifydata.io/). To download a data product, follow these steps:
1. Generate an API key by creating an API Connection in the Connections tray
2. Generate the API URL by subscribing to the data product with the API option
3. Call the API URL with your API key to generate a list of file links
4. Download the file(s) from the generated links 

## Sample Code in Python
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
```json
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
    open(f'file-{i}.csv', 'wb').write(data.content)
```

