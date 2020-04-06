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

def peticion(do):
    requests.packages.urllib3.disable_warnings()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/"+do
    headers={"Content-Type":"application/json", "X-Auth-Token":ticket}
    
    resp =requests.get(url,headers=headers,verify=False)
    global respuesta_json
    respuesta_json= resp.json()
    if do == "network-device":
        print("Los equipos de red disponibles son: ")
        lista_nom={}
        cont=0
        for equipo in respuesta_json["response"]:
            lista_nom[respuesta_json["response"][cont]["hostname"]]=cont
            cont+=1
        for key,value in lista_nom.items():
            print(value,"-",key)
        return lista_nom
    
    if do == "host":
        print("Los host en la red son: ")
        lista_nom={}
        cont=0
        for equipo in respuesta_json["response"]:
            lista_nom[respuesta_json["response"][cont]["hostIp"]]=cont
            cont+=1
        for key,value in lista_nom.items():
            print(value,"-",key)
        return lista_nom
    else:
        print("invalido")
        
def quin(cual,lst):
    for key,value in lst.items():
        que_equipo=lst[key]
        
        if cual == str(value):
            if do == "network-device":
                print("El dispositivo", respuesta_json["response"][que_equipo]["hostname"]+" es un",
                respuesta_json["response"][que_equipo]["type"],"version",respuesta_json["response"][que_equipo]["softwareVersion"] ,"y su funcion es actuar como ",respuesta_json["response"][que_equipo]["role"],"teniendo como ip de gestion:",respuesta_json["response"][que_equipo]["managementIpAddress"])
                return que_equipo
            elif do == "host":
                if respuesta_json["response"][que_equipo]["hostType"] =="wireless":
                    print("El dispositivo", respuesta_json["response"][que_equipo]["hostIp"]+" tiene la mac ",respuesta_json["response"][que_equipo]["hostMac"]+ "y esta en la vlan "+ respuesta_json["response"][que_equipo]["vlanId"], "conectado por ", respuesta_json["response"][que_equipo]["hostType"], "a el dispositivo de red ",respuesta_json["response"][que_equipo]["connectedAPName"] )
                    return que_equipo
                else :
                    print("El dispositivo", respuesta_json["response"][que_equipo]["hostIp"]+" tiene la mac ",respuesta_json["response"][que_equipo]["hostMac"]+ "y esta en la vlan "+ respuesta_json["response"][que_equipo]["vlanId"], "conectado por ", respuesta_json["response"][que_equipo]["hostType"], "a el dispositivo de red con ip",respuesta_json["response"][que_equipo]["connectedNetworkDeviceIpAddress"], "en la interfaz",respuesta_json["response"][que_equipo]["connectedInterfaceName"]  )
                    return que_equipo
            

        elif  cual == key:
            if do == "network-device":
                print("El dispositivo", respuesta_json["response"][que_equipo]["hostname"]+" es un",
                respuesta_json["response"][que_equipo]["type"],"version",respuesta_json["response"][que_equipo]["softwareVersion"] ,"y su funcion es actuar como ",respuesta_json["response"][que_equipo]["role"],"teniendo como ip de gestion:",respuesta_json["response"][que_equipo]["managementIpAddress"])
                return que_equipo
            elif do == "host":
                if respuesta_json["response"][que_equipo]["hostType"] =="wireless":
                    print("El dispositivo", respuesta_json["response"][que_equipo]["hostIp"]+" tiene la mac ",respuesta_json["response"][que_equipo]["hostMac"]+ "y esta en la vlan "+ respuesta_json["response"][que_equipo]["vlanId"], "conectado por ", respuesta_json["response"][que_equipo]["hostType"], "a el dispositivo de red ",respuesta_json["response"][que_equipo]["connectedAPName"] )
                    return que_equipo
                else :
                    print("El dispositivo", respuesta_json["response"][que_equipo]["hostIp"]+" tiene la mac ",respuesta_json["response"][que_equipo]["hostMac"]+ "y esta en la vlan "+ respuesta_json["response"][que_equipo]["vlanId"], "conectado por ", respuesta_json["response"][que_equipo]["hostType"], "a el dispositivo de red con ip",respuesta_json["response"][que_equipo]["connectedNetworkDeviceIpAddress"], "en la interfaz",respuesta_json["response"][que_equipo]["connectedInterfaceName"]  )
                      
def inicio(que):
    if que== "red":        
        return "network-device"
    if que== "host":        
        return "host"
    else:
        que=input("El dispositivo tipo de dispositivo introducido no es valido. Introduce *host* o *red* \n")
        return inicio(que)

obtencion_ticket()
que=input("Que deseas tipo de dispositivo deseas revisar host o red?:")
do =inicio(que)
exi=peticion(str(do))

cual=input("¿De cual de ellos quieres saber la informacion? Introduce su numero asociado o su identificacion exacta: \n")
que_equipo=quin(cual,exi)

while que_equipo == None:
                cual=input("Has introducido mal el equipo. Introduce su numero asociado o su identificacion exacta: \n")
                que_equipo=quin(cual,exi)

            
            
