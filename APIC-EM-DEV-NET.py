#!/usr/bin/env python3

import requests
import json
import urllib3
from pprint import pprint


def obtencion_ticket():
    requests.packages.urllib3.disable_warnings()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"
    headers={"Content-Type":"application/json"}
    body_json={"password": "Xj3BDqbU","username": "devnetuser"}
    resp =requests.post(url,json.dumps(body_json),headers=headers,verify=False)
    respuesta_json= resp.json()
    global ticket
    ticket=respuesta_json["response"]["serviceTicket"]
        


ticket=()
obtencion_ticket()
print ("tk fuera",ticket)