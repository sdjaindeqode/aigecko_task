# AIGecko

## Running the local environment

### Run server
To run server run these commands:

    cd <path_to_aigecko_root>
    pip install -r requirements.txt
    export FLASK_APP=main.py
    flask run


## Accessing data through API
### Uploading Images
For uploading images through form submission:

    method: 'post'
    endpoint: '/upload_image'
    data: 'file1',
    returns: 'id' 

For uploading images through url link:

    method: 'get'
    endpoint: '/upload_image/<path:url>'
    returns: 'id' 

    
### Analysing an image
For analysing image:
    
    method: 'get'
    endpoint: '/analyse_image/<string:hash_id>'
    returns: 'Width and height of image'


### Listing all image
For listing all images:
    
    method: 'get'
    endpoint: '/list_images'
    returns: List of object containing 'image' and their 'id'
