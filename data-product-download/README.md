
# Amplify Data API: Downloading Product Data

To follow along, it is easiest to clone with repo: 

```bash
git clone git@github.com:amplifydata/amplifydata-public.git
cd amplifydata-public/data-product-download
```

## API Key

First, you must obtain an AMPLIFY_API_KEY by following the Generating the API Key directions on this [repo's readme](https://github.com/amplifydata/amplifydata-public/tree/main).

Your AMPLIFY_API_KEY will be used to authenticate all requests againt the Amplify API.

We suggest creating a `.env` file in this directory and adding your amplify api key like this: 
```bash
AMPLIFY_API_KEY=your-key-from-amplify
```

## Create API Product Subscription

Before accessing data related to a specific product, **you must created a product subscription for that product on the frontend**. 

1. Go to the Product Package Page
2. Click "Get/Subscribe" in the upper right corner
3. Select "Connect to API"
4. Click "add"
5. **Copy and save the url shown**, it will be used below


### Setup your Python Env
To run the python for this project, install the minimal requirements:
```
pip install -r requirements.txt
```

## Download Data

Now that you have your product's api_url from the `Create API Product Subscription` section above, you can download your data. 

There are 2 options: 
1. A python script you can run
2. A notebook you can run (explains more detail behind how the api works)

### Script 

If you just want to just get the data, ou can run the following command.
**Replace the `--api_url` arg with the `PRODUCT_URL` provided in the subscription card.** 

Also, be sure to replace `data_dir` with the directory you want to save the downloaded data to. This directory must already exist. 

```bash

python get_product_data.py \
    --api_url "YOUR_API_URL_FROM_ABOVE" \
    --download_dir data_dir
```


### Notebook
For a more detail description of how the api works, you run the notebook [download-data.ipynb](https://github.com/amplifydata/amplifydata-public/blob/main/data-product-download/download-data.ipynb).

