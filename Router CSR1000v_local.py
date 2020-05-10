#!/usr/bin/env python3
import requests , urllib3
from netmiko import  ConnectHandler
from ncclient import manager
from tabulate import *



requests.packages.urllib3.disable_warnings()
username="cisco"
password="cisco123!"
host="192.168.56.101"
intlist=[]
intborrar=[]
salida2=0

def enrutamiento():
    sshcon= ConnectHandler(device_type="cisco_ios",host=host,port=22,username=username, password=password)
    ruta= sshcon.send_command("sh ip route | i is directly")
    datos=ruta.split()
    contador=0

    while  contador<len(datos):
 
        if datos[contador]== "S*":        
            datos[contador]= "Ruta por defecto"
        elif datos[contador]== "S":
            datos[contador]= "Ruta estatica"
        elif datos[contador]== "L":
            datos[contador]= "Local"
        elif datos[contador]== "C":
            datos[contador]= "Conectada"
        elif datos[contador]== "is" :    
            del datos[contador]
            continue
        elif datos[contador]==  "directly" :    
            del datos[contador]
            continue
        elif datos[contador]==  "connected," :    
            del datos[contador] 
            continue
        contador+=1

    count=0
    rutas={}
    routing=[]
    tabla1=[]

    while count<len(datos):
    
        rutas ["tipo"]=datos[count]
        count+=1
        rutas ["net"]=datos[count]
        count+=1
        rutas ["out"]=datos[count]
        count+=1
        routing=[rutas["tipo"],rutas["net"], rutas["out"] ]
        tabla1.append(routing)
    
    campos=["Tipo de ruta","Red de  destino ","Interfaz de salida"]

    print(tabulate(tabla1,campos))

def interfaces():
    url_1="https://192.168.56.101/restconf/data/interfaces"
    url_2="https://192.168.56.101/restconf/data/interfaces-state"


    headers={"Accept":"application/yang-data+json","Content-Type":"application/yang-data+json"}
    aut= ("cisco","cisco123!")

    retorno_rest1=requests.get(url_1,auth=aut,headers= headers, verify=False )
    rest_json1=retorno_rest1.json()

    retorno_rest2=requests.get(url_2,auth=aut,headers= headers, verify=False )
    rest_json2=retorno_rest2.json()

    
    cont=0
    ip=[]
    mascara=[]
    tabla=[]
    lista=[]

    for cosa in rest_json1["ietf-interfaces:interfaces"]["interface"]:
            if cosa["ietf-ip:ipv4"] == {}:
                ip.append("sin configurar")
                mascara.append("sin configurar")
            else:
                ip.append(cosa["ietf-ip:ipv4"]["address"][0]["ip"])
                mascara.append(cosa["ietf-ip:ipv4"]["address"][0]["netmask"])
          
    for el in rest_json2["ietf-interfaces:interfaces-state"]["interface"]: 
        host=[cont,el["name"],el["phys-address"], ip[cont] , mascara[cont]]
                
        lista.append(el["name"])
        
        cont+=1

        
        tabla.append(host)
        

    
    
    cabezera=["Interfaz","Nombre interfaz","Direccion Fisica","Dirección IP","Mascara de subred"]
    print(tabulate(tabla,cabezera))
    
    global intlist
    intlist=lista
    return len(lista)-1
 
def crear():
    con = manager.connect(host= "192.168.56.101", port=830, username="cisco", password="cisco123!",hostkey_verify=False)
    int_num=input("Introduce el numero de interfaz loopback: \n")
    descripcion=input("Introduce la descripcion: \n")
    direccion=input("Introduce la direccion ip: \n")
    mascara=input("Introduce la mascara de subred: \n")
    
    filtro= """
    <config> <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>"""+int_num+"""</name>
                <description>"""+descripcion+"""</description>
                <ip>
                    <address>
                        <primary>
                            <address>"""+direccion+"""</address>
                            <mask>"""+mascara+"""</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
        </native>
    </config>
    """
    #filtrado=con.get(filter=filtro)
    respuesta= con.edit_config(target="running" ,config=filtro)

    print("La interfaz loopback ",int_num, " con la descripcion ", descripcion," con IP ",direccion," y mascara ",mascara," ha sido creada.\n")
    interfaces()

def borrar():
    print("Las interfaces disponibles son: \n")
    max_int=interfaces()
    
    try:
        global intborrar
        intborrar=int(input("\nQue numero de interfaz borrar? \n"))
    
    except ValueError:
        print("\nEsta interfaz no existe o no es valida. Las interfaces estan comprendidas entre 0 y ", max_int)
        input("\n Enter para continuar\n")
        borrar() 
    while intborrar> max_int:
        print("\nEsta interfaz no existe o no es valida. Las interfaces estan comprendidas entre 0 y ", max_int)
        input("\nEnter para continuar\n")
        borrar()
     
    url_b="https://192.168.56.101/restconf/data/ietf-interfaces:interfaces:/interface="+intlist[intborrar]
    
    headers={"Accept":"application/yang-data+json","Content-Type":"application/yang-data+json"}
    aut= ("cisco","cisco123!")

    retorno_restb=requests.delete(url_b,auth=aut,headers= headers, verify=False )
    

    print("La interfaz ha sido borrada.\n")
    interfaces()
  
def aplicacion():
    print ("Hola, bienvenido a la aplicacion de gestion de la maquina virtual de CSR1000v \n")
    print ("Introduce el numero acorde a la opcion que desees realizar de la tabla \n")

    volta=0
    eleccion=["Visualizar las interfaces existentes en el dispositivo","Visualizar las tablas de ruta del dispositivo "]

    
    tabla1=[]

    for num in eleccion:
        
        opciones=[volta+1,eleccion[volta]]
        volta+=1    

        tabla1.append(opciones)

    cap=["Num proposito","Descripcion del proposito"]

    print(tabulate(tabla1,cap))
    
    
    salida1=input("\nEl numero que elegire es : ")
    while int(salida1) > len(eleccion):
        salida1=input("\nHas introducido un numero que no figura en la tabla de propositos, vuelve a intrducir el numero por favor: \n ")


    print("\nHas elegido ",eleccion[int(salida1)-1], "\n" )
    
    if salida1 == "1":
        interfaces()
        global salida2
        salida2= input("\nDeseas crear o borrar las interfaces existentes en el dispositivo? c/b : \n")
        modif(salida2)
             

    else:
        enrutamiento()

def modif(salida2):
    if salida2 == "c":
        crear()
            
    elif salida2 == "b":
        borrar()
    
    else:
        salida2=input("\nNo has introducido ni \"c\" ni \"b\", introduce \"c\" o \"b\" : \n")
        modif(salida2)
            
aplicacion()
 



    


