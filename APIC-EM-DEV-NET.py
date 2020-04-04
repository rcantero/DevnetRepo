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
        
#ticket=()
obtencion_ticket()
#print ("tk fuera",ticket)

def peticion(do):
    requests.packages.urllib3.disable_warnings()
    url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/"+do
    headers={"Content-Type":"application/json", "X-Auth-Token":ticket}
    
    resp =requests.get(url,headers=headers,verify=False)
    global respuesta_json
    respuesta_json= resp.json()
    #pprint(respuesta_json)
    cont=0
    print("Los equipos de red disponibles son: ")
    global lista_nom
    lista_nom={}

    for equipo in respuesta_json["response"]:
        #print(respuesta_json["response"][cont]["hostname"])
        lista_nom[respuesta_json["response"][cont]["hostname"]]=cont
        cont+=1
    
    

    #print("interior de lista", lista_nom)

    for key,value in lista_nom.items():
        print(value,"-",key)
    


    #global cual
    #cual=input("¿De cual de ellos quieres saber la informacion? Introduce su numero asociado o el nombre exacto\n")
    

    #for equipo in respuesta_json["response"]:
        #print("El dispositivo", respuesta_json["response"][cont]["hostname"]+" es un",
        #respuesta_json["response"][cont]["type"],"version",respuesta_json["response"][cont]["softwareVersion"] ,"y su funcion es actuar como ",respuesta_json["response"][cont]["role"],"teniendo como ip de gestion:",respuesta_json["response"][cont]["managementIpAddress"])
        #cont+=1


def quin(cual):
     
    for key,value in lista_nom.items():
        if cual == str(value):
            que_equipo=lista_nom[key]
            
            return que_equipo
        elif  cual == key:
            que_equipo=lista_nom[key]
            return que_equipo
                

    
        

    



    #print("los valores son",lista_nom.items())
    #que_equipo=lista_nom[cual]
    #print("numero en la lista equipos es \n",que_equipo)

    #print("El dispositivo", respuesta_json["response"][que_equipo]["hostname"]+" es un",
   #     respuesta_json["response"][que_equipo]["type"],"version",respuesta_json["response"][que_equipo]["softwareVersion"] ,"y su funcion es actuar como ",respuesta_json["response"][que_equipo]["role"],"teniendo como ip de gestion:",respuesta_json["response"][que_equipo]["managementIpAddress"])



do=input("que deseas hacer?:")

do="network-device" ### esto ira fuera 

peticion(do)

cual=input("¿De cual de ellos quieres saber la informacion? Introduce su numero asociado o el nombre exacto: \n")

que_equipo=quin(cual)

while que_equipo == None:
    cual=input("Has introducido mal el equipo. Introduce su numero asociado o el nombre exacto\n")
    que_equipo=quin(cual)


print("El dispositivo", respuesta_json["response"][que_equipo]["hostname"]+" es un",
respuesta_json["response"][que_equipo]["type"],"version",respuesta_json["response"][que_equipo]["softwareVersion"] ,"y su funcion es actuar como ",respuesta_json["response"][que_equipo]["role"],"teniendo como ip de gestion:",respuesta_json["response"][que_equipo]["managementIpAddress"])
