from re import I
import socket 
import logging
import json
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

class SnmpManager():
    '''Class provide an SNMP Manager instance to handle protocol's requests.'''

    def __init__(self, timeout,  port = 161) -> None:
        self.port = port
        self.timeout = timeout
        logging.basicConfig(level=logging.INFO)
        self.is_ready = False

    def __create_socket(self) -> bool:
        try:
            logging.info('Creating SNMP socket...')
            self.__snmp_socket = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
            self.__snmp_socket.settimeout(self.timeout)
            self.is_ready = True
        except Exception as ex:
            logging.error(f'Error during SnmpManager initialization: {ex}') 
            self.is_ready = False

    def get_request(self, ip_address, community, oid):
        status = False
        json_response = {}
        self.__create_socket() 
        if(self.is_ready):
            if (community == ''):
                logging.info('Using default community: public')
                community = 'public'

            snmp_message = self.__build_snmp_message(oid = oid, community= community)
            logging.info(snmp_message)
            self.__snmp_socket.sendto(snmp_message, (ip_address, self.port))
            logging.info('Frame sent! Waiting response...')
            while True:
                try: 
                    snmp_response = self.__snmp_socket.recv(2000)
                    logging.info('SNMP Message received!')
                    json_response = self.__handle_snmp_response(snmp_response)
                    status = True
                    break
                except Exception as ex:
                    if(self.__snmp_socket.timeout):
                        logging.info(f'The socket timed out ({self.timeout})')
                    else: 
                        logging.info(f'Unhandled exception: {ex}')
                    break
            self.__snmp_socket.close()

        return status, json_response

    def __build_snmp_message(self, community, oid = 'public'):
        TypeVal= b'\x05'
        lenVal_b = b'\x00'
        SVal = TypeVal + lenVal_b
        lenSVal_i = 2

        OID = oid
        b = OID.split(".")
        b = b[2:]
        oid = chr(0x2b)

        for i in range(len(b)):
            oid = oid + chr(int(b[i]))
        oid = oid.encode()

        lenOID_b = chr(len(oid)).encode()
        lenOID_i = len(oid)
        TypeOid = b'\x06'
        SOid = TypeOid + lenOID_b + oid
        lenSOid_i = 2 + lenOID_i

        TypeVarbind = b'\x30'
        lenVar_i = lenSOid_i + lenSVal_i
        lenVar_b = lenVar_i.to_bytes(1,'little')
        SVarbind = TypeVarbind + lenVar_b + SOid + SVal

        # MONTANDO VARBINDLIST
        TypeVarbindList = b'\x30'
        lenVarList_i = 2 + lenVar_i
        lenVarList_b = lenVarList_i.to_bytes(1,'little')
        SVarbindList = TypeVarbindList + lenVarList_b+ SVarbind

        # MONTANDO REQUEST ID
        lenRqID_i = 3
        SRqID = b'\x02'+ b'\x01' + b'\x01'

        # MONTANDO ERROR
        lenErr_i = 3
        SErr = b'\x02' + b'\x01' + b'\x00'

        # MONTANDO ERROR INDEX
        lenErrIndex_i = 3
        SErrIndex = b'\x02' + b'\x01' + b'\x00'

        # MONTANDO SNMP PDU
        TypeSPDU = b'\xa0' 
        lenPDU_i = lenRqID_i + lenErr_i + lenErrIndex_i + (2 + lenVarList_i)
        lenPDU_b = lenPDU_i.to_bytes(1,'little')
        SPDU = TypeSPDU + lenPDU_b + SRqID + SErr + SErrIndex + SVarbindList

        # MONTANDO COMMUNITY STRING
        TypeComm = b'\x04'
        Comm = community.encode()
        logging.info(community)
        CommChr = Comm.decode()
        lenComm_b = chr(len(CommChr)).encode()
        lenComm_i = len(Comm)
        SComm = TypeComm + lenComm_b + Comm

        # MONTANDO VERSION
        TypeVersao = b'\x02'
        lenVersao_b = b'\x01'
        lenVersao_i = 3
        Versao = b'\x00'
        SVersao = TypeVersao + lenVersao_b + Versao

        # MONTANDO SNMP MESSAGE (GETREQUEST)
        MsgType = b'\x30'
        lenSSnmpMsg_i = lenVersao_i + (2 + lenComm_i)+ (2 + lenPDU_i)
        lenSSnmpMsg_b = lenSSnmpMsg_i.to_bytes(1,'little')
        SSnmpMsg =  MsgType + lenSSnmpMsg_b + SVersao + SComm + SPDU
        return SSnmpMsg

    def __handle_snmp_response(self, wholeMsg):
        while wholeMsg:
            msgVer = int(api.decodeMessageVersion(wholeMsg))
            if msgVer in api.protoModules:
                pMod = api.protoModules[msgVer]
            else:
                logging.info('Unsupported SNMP version %s' % msgVer)
                return {}

            reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())
            fullMessage = str(reqMsg)
            dict_get_response = {}
            try:
                msg_itens = fullMessage.split('\n')
                dict_get_response = {
                    'version': msg_itens[1].split('=')[1],
                    'community': msg_itens[2].split('=')[1],
                    'type': msg_itens[13].split('=')[0].strip(),
                    'value': msg_itens[13].split('=')[1],
                    'name': msg_itens[10].split('=')[1],
                    'request_id': msg_itens[5].split('=')[1],
                    'error_status': msg_itens[6].split('=')[1],
                    'error_index': msg_itens[7].split('=')[1]
                }
            except Exception as ex:
                logging.info('Error during parsing SNMP response message')
                logging.error(ex)

        logging.info(fullMessage)
        return dict_get_response