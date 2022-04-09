import subprocess, platform
import logging

logging.basicConfig(level=logging.INFO)

def check_health(ip_address):
    parameter = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(f'ping {parameter} 1 {ip_address}')
    response.wait()
    if response.poll() == 0:
        logging.info(f'{ip_address} is up!')
        return {'status': True}
    else:
        logging.info(f'{ip_address} is down!')
        return {'status': False}



