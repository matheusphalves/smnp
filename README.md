# smnp
Simple management network protocol implementation.

# How to run

Install the following packages

```
pip install virtualenv
```


Then create a folder and activate a virtual environment.

```
virtualenv snmp snmp/Scripts/activate
```

Install the dependencies running

``` 
pip install -r requirements.txt
```


# What's is SNMP?

Simple Network Management Protocol (SNMP) is an Internet Standard protocol used to monitor and manage the network devices connected over an IP. We create one API that handle SNMP Get requests. The results are showed using a react app. If you don't want to use an API for this, just use the ```SnmpManager``` class; that provides a  atomic use of each SNMP protocolo's request.


# **Open endpoints**

## Get oid info

```GET URL_API/get_request?ip_address=127.0.0.1&community=public&oid=1.3.6.1.2.1.2.2.1.5.20```

### **Response body (example)**

HTTP Status Code: **200 OK**
```
{
    "response": {
        "community": "public",
        "error_index": "0",
        "error_status": "noError",
        "name": "1.3.6.1.2.1.2.2.1.1.11",
        "request_id": "1",
        "type": "number",
        "value": "11",
        "version": "version-1"
    },
    "status": true
}
```
