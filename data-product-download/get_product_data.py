import os
import concurrent.futures
import requests
from tqdm import tqdm
import click
import time
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["AMPLIFY_API_KEY"]

# https://dev.amplifydata.io/products/b16f31fd-41e1-4dd9-839d-f67d06af95c0/columns/edit

# res = requests.get(
#     "https://dev.amplifydata.io/external-api/v2/products/ddbb7b6e-0978-4e5f-8916-1d3fb3bfebaf/files",
#     headers = {
#         "X-API-KEY": API_KEY,
#         'accept': 'application/json'
#     }
# )

def download_file(url, filename, max_retries=6, backoff_factor=2, jitter_max=2.0):
    attempt = 0
    while attempt < max_retries:
        try:
            with requests.get(url, stream=True) as r:
                if r.status_code == 429:
                    attempt += 1
                    if attempt < max_retries:
                        base_sleep_time = backoff_factor ** (attempt - 1)
                        jitter = random.uniform(0, jitter_max)
                        sleep_time = base_sleep_time + jitter
                        print(f'Rate limit encountered. Retrying in {sleep_time} seconds...')
                        time.sleep(sleep_time)
                        continue
                    else:
                        raise Exception('Rate limit encountered. Max retries exceeded.')

                r.raise_for_status()  # Raise an exception for other HTTP errors

                total_size = int(r.headers.get('content-length', 0))
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))

                progress_bar.close()
                print(f"Downloaded to {filename} completed")
                return
        except requests.RequestException as e:
            # Handle other exceptions (e.g., connection errors)
            print(f"An error occurred: {e}")
            attempt += 1
            if attempt < max_retries:
                base_sleep_time = backoff_factor ** (attempt - 1)
                jitter = random.uniform(0, jitter_max)
                sleep_time = base_sleep_time + jitter
                print(f'Retrying in {sleep_time} seconds...')
                time.sleep(sleep_time)
            else:
                raise # Re-raise the last exception after max retries

@click.command()
@click.option('--api_url', help='Product id')
@click.option('--download_dir', help='Download directory')
@click.option('--partition_key_after', help='Partition Key After')
def main(api_url, download_dir, partition_key_after):
    page = 1
    print(f'==== Page number {page} ====')
    res = requests.get(
        api_url,
        params = {
            'page': page,
            'partition_key_after': partition_key_after
        },
        headers = {
            "X-API-KEY": API_KEY,
            'accept': 'application/json'
        }
    )
    time.sleep(2) # better do retry instead
    if res.status_code != 200:
        raise Exception(res.json())
    print(res)
    data = res.json() # { "download_links": [], "metadata": {} }
    # print(f"Downloading {len(data['download_links'])} files to {download_dir}")
    for num, i_url in enumerate(data["download_links"]):
        print(f"Downloading file [{num}/{len(data['download_links'])}]")
        download_file(i_url['link'], f"{download_dir}/file-{num}.csv")
        print(f"Removing file {download_dir}/file-{num}.csv")
        os.remove(f'{download_dir}/file-{num}.csv')

    # file_list = [f"{download_dir}/file-{num}.csv" for num in range(len(data["download_links"]))]
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(download_file, data["download_links"], file_list)

    while page < data['total_pages']:
        page += 1
        print(f'==== Page number {page} ====')
        res = requests.get(
            api_url,
            params = {
                'page': page,
                'partition_key_after': partition_key_after
            },
            headers = {
                "X-API-KEY": API_KEY,
                'accept': 'application/json'
            }
        )
        time.sleep(2) # better do retry instead
        if res.status_code != 200:
            raise Exception(res.json())

        data = res.json()

        for num, i_url in enumerate(data["download_links"]):
            print(f"Downloading file [{num}/{len(data['download_links'])}]")
            download_file(i_url['link'], f"{download_dir}/file-{num}.csv")
            print(f"Removing file {download_dir}/file-{num}.csv")
            os.remove(f'{download_dir}/file-{num}.csv')
        time.sleep(2) # better do retry instead

if __name__ == "__main__": 
    main()