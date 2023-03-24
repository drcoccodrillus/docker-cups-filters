from flask import Blueprint, request
import os
import subprocess
import base64
import json
import re

from config import *

api = Blueprint('api', __name__)

#region APIs
@api.route('/v1/print-jobs', methods=['GET'])
def get_printer_queues():
    queues = []
    lpstat_result = subprocess.check_output(['lpstat', '-h', CUPS_HOST, '-d', 'gprinter'])
    i = 0
    for line in lpstat_result.decode('utf-8').split('\n'):
        if line.startswith('gprinter'):
            value = line.split()
            queues.append({})
            queues[i]['id'] = value[0]
            queues[i]['owner'] = value[1]
            queues[i]['size'] = value[2]
            queues[i]['date'] = value[4] + " " + value[5] + " " + value[6]
            queues[i]['time'] = value[7]
            i += 1
    return json.dumps(queues)

@api.route('/v1/printer-status', methods=['GET'])
def get_printer_status():
    details = []
    lpstat_result = subprocess.check_output(['lpstat', '-h', CUPS_HOST, '-t'])
    i = 0
    for line in lpstat_result.decode('utf-8').split('\n'):
        if(re.match('printer.*disabled', line)):
            value = line.split(' ')
            details.append({})
            details[i]['printer'] = value[1]
            details[i]['status'] = value[2]
            details[i]['date'] = value[5] + " " + value[6] + " " + value[7].rstrip(',')
            details[i]['time'] = value[8]
            print(re.match('printer.*', line).group())
        elif(re.match('printer.*is', line)):
            value = line.split(' ')
            details.append({})
            details[i]['printer'] = value[1]
            details[i]['status'] = value[5]
            details[i]['date'] = value[8] + " " + value[9] + " " + value[10].rstrip(',')
            details[i]['time'] = value[11]
            print(re.match('printer.*', line).group())
        i += 1
    return json.dumps(details)

@api.route('/v1/printer-details', methods=['GET'])
def get_printer_details():
    details = []
    lpinfo_result = subprocess.check_output(['lpinfo', '-h', CUPS_HOST, '-v'])
    i = 0
    for line in lpinfo_result.decode('utf-8').split('\n'):
        value = line.split(' ')
        if(len(value) == 2 and re.match('usb://.*', value[1])):
            print(re.match('usb://.*', value[1]).group())
            details.append({})
            details[i]['connection'] = value[0]
            details[i]['uri'] = value[1]
            i += 1
    return json.dumps(details)

@api.route('/v1/print-base64', methods=['POST'])
def print_pdf():
    data = request.get_json()
    if('pdf' in data):
        pdf_base64 = data['pdf']
        pdf_decoded = base64.b64decode(pdf_base64)

        with open('temp.pdf', 'wb') as file:                    #Create temporary PDF file
            file.write(pdf_decoded)
            file.close()

        #Render PDF through foomatic then send the job to CUPS server
        #----------------------
        result = subprocess.run(['foomatic-rip', '--ppd', '/usr/share/ppd/cupsfilters/'+PPD, '-q', 'temp.pdf', '-o', '-'], stdout=subprocess.PIPE)
        subprocess.run(['lp', '-h', CUPS_HOST, '-d', 'gprinter', '-'], input=result.stdout)
        #----------------------

        os.rename('temp.pdf', 'last_ticket.pdf')                #Preserve temporary PDF file as last printed ticket
        return {'message': 'PDF printed'}
    else:
        return {'message': 'Error: No PDF provided'}, 400
#endregion
