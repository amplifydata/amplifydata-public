
# Amplify Data API: Downloading Product Data

To follow along, it is easiest to clone with repo: 

```bash
git clone git@github.com:amplifydata/amplifydata-public.git
cd amplifydata-public/data-product-download
```

## API Key

First, you must obtain an AMPLIFY_API_KEY by following the Generating the API Key directions on this repo's readme.

Your AMPLIFY_API_KEY will be used to authenticate all requests againt the Amplify API.

We suggest creating a `.env` file in this directory and adding your amplify api key like this: 
```bash
AMPLIFY_API_KEY=your-key-from-amplify
```

### Python Env
To run the python for this project, install the minimal requirements:
```
pip install -r requirements.txt
```

## Download Data
PRODUCT_URL

### Script 
If you want to just get the data, You can run the following command.
**Replace the `--api_url` arg with the `PRODUCT_URL` provided in the subscription card. 
```bash

python get_product_data.py \
    --api_url "https://dev.amplifydata.io/external-api/v2/products/b16f31fd-41e1-4dd9-839d-f67d06af95c0/files" \
    --download_dir data_dir
```

### Notebook
For a more detail description of how the api works, you run the notebook [download-data.ipynb](https://github.com/amplifydata/amplifydata-public/blob/main/data-product-download/download-data.ipynb).

