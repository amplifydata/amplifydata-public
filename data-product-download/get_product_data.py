import os
import concurrent.futures
import requests
from tqdm import tqdm
import click
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

def download_file(url, filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))

        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                progress_bar.update(len(chunk))
        progress_bar.close()
        print(f"Downloaded to {filename} completed")

@click.command()
@click.option('--api_url', help='Product id')
@click.option('--download_dir', help='Download directory')
def main(api_url, download_dir):
    res = requests.get(
        api_url,
        headers = {
            "X-API-KEY": API_KEY,
            'accept': 'application/json'
        }
    )
    if res.status_code != 200:
        raise Exception(res.json())
    print(res)
    data = res.json() # { "download_links": [], "metadata": {} }
    # print(f"Downloading {len(data['download_links'])} files to {download_dir}")
    # print(data)

    # file_list = [f"{download_dir}/file-{num}.csv" for num in range(len(data["download_links"]))]
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(download_file, data["download_links"], file_list)

    for num, i_url in enumerate(data["download_links"]):
        print(f"Downloading file [{num}/{len(data['download_links'])}]")
        download_file(i_url, f"{download_dir}/file-{num}.csv")
if __name__ == "__main__": 
    main()