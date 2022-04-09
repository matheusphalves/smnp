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
pip -r requirements.txt
```


# What's is SNMP?

Pretty text


# **Open endpoints**

## Get oid info


```POST URL_API/get_request```: Pretty test

### **Request body (example)**
```
{
    "ip_address": "127.0.0.1",
    "community": "public",
    "oid": "1.3.6.1.2.1.1.1.0"
}
```

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