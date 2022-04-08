from flask import Flask, request
from flask_cors import CORS, cross_origin
import logging
from service.snmp_manager import SnmpManager


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
snmp = SnmpManager(timeout=10)
logging.basicConfig(level=logging.INFO)

@app.route('/get_request', methods=['POST'])
@cross_origin()
def get_request():
    request_body = request.get_json(force=True)
    ip_address = request_body['ip_address']
    community = request_body['community']
    oid = request_body['oid']
    logging.info(f'Sending GET REQUEST to ({ip_address}, {community}, {oid})')
    status, oid_response = snmp.get_request(ip_address=ip_address, community=community, oid=oid)
    
    return {'status': status, 'response': oid_response} 

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)