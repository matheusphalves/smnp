from flask import Flask, request
from flask_cors import CORS, cross_origin
import logging
from service.snmp_manager import SnmpManager
from service.check_health import check_health


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

@app.route('/get_request', methods=['GET'])
@cross_origin()
def get_request_params():
    ip_address = request.args.get('ip_address')
    community = request.args.get('community')
    oid = request.args.get('oid')
    logging.info(f'Sending GET REQUEST to ({ip_address}, {community}, {oid})')
    status, oid_response = snmp.get_request(ip_address=ip_address, community=community, oid=oid) 
    return {'status': status, 'response': oid_response} 

@app.route('/health', methods=['GET'])
@cross_origin()
def check_agent_health():
    ip_address = request.args.get('ip_address')
    logging.info(f'Checking availablity of {ip_address}')
    return check_health(ip_address)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)