import http.client
import base64
import ssl
import requests

def authentication(host,user,password):
    #host = "192.168.75.15"
    #user = "ERSAdmin"
    #password = "Adm1n4p1"


    conn = http.client.HTTPSConnection("{}:9060".format(host), context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))

    creds = str.encode(':'.join((user, password)))
    encodedAuth = bytes.decode(base64.b64encode(creds))

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': " ".join(("Basic",encodedAuth)),
        'cache-control': "no-cache",
        'X-CSRF-TOKEN': "fetch"
        }
   
    return conn, headers



def authentication2():
    host = "192.168.75.15"
    user = "ERSAdmin"
    password = "Adm1n4p1"


    conn = http.client.HTTPSConnection("{}:9060".format(host), context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))

    creds = str.encode(':'.join((user, password)))
    encodedAuth = bytes.decode(base64.b64encode(creds))

    headers = {
        'accept': "application/json",
        'content-type': "application/json",  
        'content_type': 'application/xml',   
        'authorization': " ".join(("Basic",encodedAuth)),
        'cache-control': "no-cache",
        'X-CSRF-TOKEN': "fetch"
        }
   
    return conn, headers



