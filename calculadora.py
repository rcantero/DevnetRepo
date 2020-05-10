#!/usr/bin/env python3

def num1():
    stringa=input("Introduce un numero : ")
    try:
        global numeroa
        numeroa=int(stringa)
        return numeroa
    except ValueError:
        print ("Has introduciodo un caracter incorrecto. Vuelve a realizar la operacion. ")
        num1()
       
  
def op_num2(resultado):
    global operacion
    operacion=input("Introduce siguiente operacion: " )
        
    stringb=input("Introduce otro numero : ")
    
    try:
        global numerob
        numerob=int(stringb)
    except ValueError:
        print ("Has introduciodo un caracter incorrecto. Vuelve a realizar la operacion. ")
        op_num2(resultado)
    if operacion == "+":
             
        print("El resultado es ",resultado+numerob) 
        return  resultado+numerob
                          
        
    elif operacion == "-":
        
        
        print("El resultado es ",resultado-numerob)
        return  resultado-numerob
        
    elif operacion == "*":
        
        
        print("El resultado es ",resultado*numerob)
        return  resultado*numerob
        
    elif operacion == "/":
        try:
            
            
            print("El resultado es ",resultado/numerob)
            return  resultado/numerob
        except ZeroDivisionError:
            print ("Un valor no se puede dividir por cero. Vuelve a realizar la operacion. ")
            op_num2(resultado)
    
    #exponenciales y raíces cuadradas
    elif operacion == "**":
        
        
        print("El resultado es ",resultado**numerob)
        return  resultado**numerob

    elif operacion == "%":
        
        
        print("El resultado es ",resultado%numerob)
        return  resultado%numerob


    else:
        print("La operacion", operacion," introducida no es valida o no esta contemplada.Vuelve a introducirla por favor")
        op_num2(resultado)
   

def continuar(a):
    seguir=input("Quieres realizar una nueva  operacion sobre el resultado anterior? s/n: ")
    while seguir == "s":
        resultado=op_num2(a)
        continuar(resultado)
        break
        

def seguir(new):
    
    while new == "s":
        num1()  
        resultado=op_num2(numeroa)
        resultado=continuar(resultado)
        new=input("Quieres realizar una nueva  operacion? s/n: ")
        if new == "n":
            break

num1()  
resultado=op_num2(numeroa)
resultado=continuar(resultado)




new=input("Quieres realizar una nueva  operacion? s/n: ")
seguir(new)
print("Bye,bye")
