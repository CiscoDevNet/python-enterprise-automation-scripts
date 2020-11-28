import http.client
import base64
import ssl
import json
import requests
import datetime
import xmltodict
from jinja2 import Template
import csv
from authentication import authentication


def get_sgtsids(conn,header):
 
    sgtids=[]
    conn.request("GET", "/ers/config/sgt", headers=header)

    res = conn.getresponse()
    data = res.read()

    #print("Status: {}".format(res.status))
    #print("Header:\n{}".format(res.headers))
    #print("Body:\n{}".format(data.decode("utf-8")))
    sgts = json.loads(data.decode("utf-8"))["SearchResult"]["resources"]
    for sgt in sgts:
        #print(sgt["name"])
        sgtids.append(sgt["id"])
    
    return sgtids

def get_sgt_info(conn,header,sgtids):

    try:
        with open(f"SGT_Report_{datetime.datetime.now().date()}.csv", 'w') as csvf:

            writer = csv.writer(csvf)

            for sgtid in sgtids:
                conn.request("GET", f"/ers/config/sgt/{sgtid}", headers=header)   
                res = conn.getresponse()
                data = res.read()
                sgts = json.loads(data.decode("utf-8"))["Sgt"]
                writer.writerow((sgts["id"],sgts["name"],sgts["description"],sgts["value"]))
            
        return True
    except Exception as e:
        print ("Error trying to write the file" ,e)
        return False






def create_sgt(conn,header,name,description,value):

    with open("payload.j2", 'r') as f:
        jinpayload = Template(f.read())

    data={
        "sgt_name": name,
        "sgt_description": description,
        "sgt_value": value
    }

    jsonpayload = jinpayload.render(data)

    #print(jsonpayload)

    conn.request("POST", "/ers/config/sgt",headers=header,body=jsonpayload)

    res = conn.getresponse()
    data = res.read()
    if res.status==201:

        print(f"Status: {res.status}")
        print("SGT was created succesfully on ISE")


def bulk_sgt(conn,header,optype,listaux):

    #with open("bulkupdate.xml",'r') as f:
        #xmldoc = xmltodict.parse(f.read())

    #    jparse=json.dumps(xmldoc,indent=4)

    #print(jparse)
    
    # conn.request("PUT", "/ers/config/sgt/bulk/submit",headers=header,body=xmltodict.unparse(xmldoc))

    # res = conn.getresponse()
    # data = res.read()
    # if res.status==202:

    #     print(f"Status: {res.status}")
    #     print("SGT was created succesfully on ISE")

    # else:
    #     print("Error ",res.status)
    #     print("Body:\n{}".format(data.decode("utf-8")))

    payload={}
    

    # with open('sgt.csv', 'r') as csvfile:
    #     spreadsheet = csv.reader(csvfile, delimiter=',')
    #     for row in spreadsheet:
    #         listaux.append({"@description":row[1],"@name":row[0],"generationId":"0","value":row[2]})
            #print(row[0])

    payload={"ns5:sgtBulkrequest":{"@operationType":optype,"@resourceMediaType": "vnd.com.cisco.ise.trustsec.sgt.1.0+xml",
             "@xmlns:ns6": "sxp.ers.ise.cisco.com","@xmlns:ns5": "trustsec.ers.ise.cisco.com","@xmlns:ns8": "network.ers.ise.cisco.com",
             "@xmlns:ns7": "anc.ers.ise.cisco.com","@xmlns:ers": "ers.ise.cisco.com","@xmlns:xs": "http://www.w3.org/2001/XMLSchema",
             "@xmlns:ns4": "identity.ers.ise.cisco.com","ns5:resourcesList":{"ns5:sgt":listaux}}}
    
    #pypayload=json.loads(payload)
    xmlpayload=xmltodict.unparse(payload)
    #print(xmlpayload)

    conn.request("PUT", "/ers/config/sgt/bulk/submit",headers=header,body=xmlpayload)

    res = conn.getresponse()
    data = res.read()
    if res.status==202:

        print(f"Status: {res.status}")
        print("SGT was created/updated succesfully on ISE")
        print("Body:\n{}".format(data.decode("utf-8")))
        return True

    else:
        print("Error ",res.status)
        print("Body:\n{}".format(data.decode("utf-8")))
        return False


def update_sgt_org(sgtid,**kwargs):
    #Get SGT info of the object before update!
    dictaux={}

    dictaux["id"]=sgtid
    for k,v in kwargs.items():

        dictaux[k]= v

    payload={"Sgt":dictaux}

    print(json.dumps(payload,indent=4))

    conn.request("PUT", f"/ers/config/sgt/{sgtid}",headers=header,body=json.dumps(payload,indent=4))
    res = conn.getresponse()
    data = res.read()

    if res.status==200:
        print(f"Status: {res.status}")
        print(f"Response: {data.decode('utf-8')}")
    
    else:
        print(f"Error {res.status}")


def update_sgt(host,user,passw,sgtid,**kwargs):
    #Get SGT info of the object before update!
    dictaux={}

    dictaux["id"]=sgtid
    for k,v in kwargs.items():

        dictaux[k]= v

    payload={"Sgt":dictaux}

    print(json.dumps(payload,indent=4))

    base_url=f"https://{host}:9060/"
    sgt_url=f"ers/config/sgt/{sgtid}"

    print(base_url)

    creds = str.encode(':'.join((user, passw)))
    encodedAuth = bytes.decode(base64.b64encode(creds))

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': " ".join(("Basic",encodedAuth)),
        'cache-control': "no-cache",
        'X-CSRF-TOKEN': "fetch"
       
    }

    response=requests.request("POST",url=f"{base_url}{sgt_url}",headers=headers,data=json.dumps(payload))
    if response.status_code==200:
        print(response.text)
    else:
        print("Error ",response.status_code,response.text)


#if __name__ == "__main__":

    #conn,header = authentication()
    #get_sgtsids(conn,header)
    #create_sgt(conn,header,"Python_developer","SGT from python",27)
    #update_sgt("192.168.75.15","ERSAdmin","Adm1n4p1","65b47340-26ab-11eb-a815-a66c39a2629c",name="testUser",description="Modified from python again",value=17)
    #create_bulk_sgt(conn,header)
