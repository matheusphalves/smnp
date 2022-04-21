from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import logging
from service.snmp_manager import SnmpManager
from service.check_health import check_health
from validation.validation import GetRequestForm, get_errors_wtforms


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
snmp = SnmpManager(timeout=10)
logging.basicConfig(level=logging.INFO)

@app.route('/get_request', methods=['GET'])
@cross_origin()
def get_request_params():
    form = GetRequestForm(request.args)
    if(form.validate()):
        ip_address = request.args.get('ip_address')
        community = request.args.get('community')
        oid = request.args.get('oid')
        logging.info(f'Sending GET REQUEST to ({ip_address}, {community}, {oid})')
        status, oid_response = snmp.get_request(ip_address=ip_address, community=community, oid=oid) 
        return make_response({'status': status, 'response': oid_response}, 200)

    return make_response({'status': False, 'errors': get_errors_wtforms(form)}, 400)

@app.route('/health', methods=['GET'])
@cross_origin()
def check_agent_health():
    ip_address = request.args.get('ip_address')
    logging.info(f'Checking availablity of {ip_address}')
    return check_health(ip_address)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)