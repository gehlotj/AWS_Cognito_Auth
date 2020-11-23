import requests
import urllib
import json
import base64

class Req:
    '''
        The request class allows to make any post and get requests using request library
    '''

    def get_token(params,ca,login_url):
        '''
            The following method will retrieve access token based on the parameter passed
        '''

        url = login_url + urllib.parse.urlencode(params)
        headers={'Content-Type' : 'application/x-www-form-urlencoded',
                 'Authorization':ca,
                 'Accept-Encoding': 'gzip, deflate'
                 }
        r = requests.post(url, headers=headers)
        return r


    def auth_post(url,token):
        '''
            The following function will execute post method on endpoint url passed as parameter
        '''
        header = {'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(token)}
        r = requests.post(url,headers=header)
        return r


    def get_public_keys(url):
        '''
            The following fuction will retrieve the public key from AWS Cognito
        '''
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()['keys']
        else: return None


    def get_encoded_cid(data):
        '''
            The following function will encode the client id and secret
        '''
        result = 'Basic '
        message_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        result+=base64_message
        return result
