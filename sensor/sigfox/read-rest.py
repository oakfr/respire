import os
import re
import json
import requests
import datetime

def post_rest (url, data, method):
    username = open ('username.txt','r').read().strip()
    passwd = open('password.txt','r').read().strip()
    headers = {'Content-type': 'application/json'}
    ntrials = 3
    for trial in range(ntrials):
        try:
            if method=='post':
                response = requests.post(url,data=data,auth=(username,passwd),headers=headers)
            else:
                response = requests.get(url,data=data,auth=(username,passwd),headers=headers)
        except:
            print ('Warning.  REST API request failed.  Re-trying...')
            continue
        if not response.ok:
            print(response)
            return None
        else:
            return response.content
    return None

def main():


# list devices
#    url = 'https://backend.sigfox.com/api/devicetypes'
#    data = None
#    d = post_rest (url, data, 'post')
#    if d is None:
#        return

    deviceid = '5887c3519058c25feb21326f'
    url = 'https://backend.sigfox.com/api/devicetypes/%s/messages'%deviceid
    data = None
    d = post_rest (url, data, 'post')
    print (d)
    if d is None:
        print ('request failed')
        return


if __name__ == "__main__":
    main()
