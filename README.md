
# cubemos Skeleton Estimation API Client
Example Client codes for using the cubemos Skeleton Estimation API.
**Currently, only a python sample is available.**

## Requirements
Python 3.6 and pipenv

## API key and integrating in your application
The Trial API key can be availed here: https://console.cubemos.com/authPage. 
In order to integrate it seamlessly in your application, contact meet@cubemos.com

## Getting started with python

Run the following commands

    python3.6 -m venv venv
    source venv/bin/activate
    pip install -r python-requirements.txt
    cd python
    # IMPORTANT: UPDATE The x-api-key in the code to the API Key you obtain from https://console.cubemos.com/authPage
    python skeleton-estimation-webcam.py

### API usage inside the python code
The python example runs a continous loop wherein the following steps takes place: 
1. A base64 encoded image is acquired
2. POST call is made to https://api.cubemos.com/skeletons/estimate
3. The response payload is used to render the skeletons on the acquired image and display it along with the actions 

Currently only the following actions are analysed: 
1. Sitting
2. Standing
3. Right-hand raised
4. Left-hand raised

The speed of the application depends on your internet connection. The processing time of the image at the backend is around 90ms and the remaining round trip from our servers in europe is directly dependent on your bandwidth.

   
## Contribution
  Feel free to make contributions in the programming language of your choice 

