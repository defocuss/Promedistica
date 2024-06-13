import json
import time


#                    #
# Agregar las clases #
#                    #


def menu():
    while True:
        time.sleep(3)
        print("Promedios de notas:")
        print("1. Agregar Ramo y Notas")
        print("2. Ver notas de un ramo")
        print("3. Modificar Ramo/Nota")
        print("4. Eliminar Ramo")
        print("5. Ver notas")
        print("6. Exportar a un CSV")
        print("7. Salir")
        print(" ")
        opcion = leer_opcion_menu()
        if opcion == '1':
            agregar_ramo(filename='notas.json')
        elif opcion == '2':
            ver_notas_ramo(filename= 'notas.json')
        elif opcion == '3':
            modificar_ramo(filename='notas.json')
        elif opcion == '4':
            eliminar_ramo(filename='notas.json')
        elif opcion == '5':
            imprimir_todas_notas(filename='notas.json')
        elif opcion == '6':
            exportar_a_csv(filename='notas.json')
        elif opcion == '7':
            print("Programa Terminado :)")
            break

def leer_opcion_menu():
    while True:
        opcion = input("Seleccione una opción: ")
        try:
            if int(opcion) >= 1 and int(opcion) <=7:
                return opcion
        except ValueError:
            pass
        print("Por favor seleccione una opcion válida!")

def crear_json_notas(data, filename='notas.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=6)

def leer_json(filename='notas.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def agregar_ramo(filename='notas.json'):
    data = leer_json(filename)
    
    ramo = input("Cual es el ramo?: ")
    if ramo in data:
        for i in range(0,3):
            print(" ")
        print("---------- Ramo existente ----------")
        print(" ")
        print("Este ramo ya existe. Intenta nuevamente con uno nuevo.")
        print(" ")
        print("---------- Ramo existente ----------")
        for i in range(0,2):
            print(" ")
    else:
        data[ramo] = []
        pruebas = input("Dime cuantas pruebas tienes: ")
        variable = True
        while variable:
            try:
                pruebas = int(pruebas)
                variable = False
            except ValueError:
                pruebas = input("Agregue una cantidad válida: ")
        # for x in range(pruebas):
        #     print(f"\nAgregar prueba {x + 1}:")
        #     nota = input("Dime la nota de esta prueba: ")
        #     variable = True
        #     while variable:
        #         try:
        #             nota = float(nota)
        #             variable = False
        #         except ValueError:
        #             nota = input("Agregue una nota valida: ")
        #     ponderacion = input("Dime cuanto es la ponderacion de esta prueba: ")
        #     variable = True
        #     while variable:
        #         try:
        #             ponderacion = float(ponderacion)
        #             variable = False
        #         except ValueError:
        #             ponderacion = input("Agregue una ponderacion valida valida: ")
        #     promedio = nota * ponderacion
        #     evaluacion = {"tipo": "prueba", "nombre": f"Prueba {x + 1}", "nota": nota, "ponderacion": ponderacion, "promedio": promedio}
        #     data[ramo].append(evaluacion)
        # controles = int(input("Dime cuantos controles tienes: "))
        # for y in range(controles):
        #     print(f"\nAgregar control {y + 1}:")
        #     nota = float(input("Dime la nota de este control: "))
        #     ponderacion = float(input("Dime cuanto es la ponderacion de este control: "))
        #     promedio = nota * ponderacion
        #     evaluacion = {"tipo": "control", "nombre": f"Control {y + 1}", "nota": nota, "ponderacion": ponderacion, "promedio": promedio}
        #     data[ramo].append(evaluacion)
        
        # todo lo comentado lo voy a pasar a una funcion, por lo de las buenas practicas

        suma_promedios = 0
        for evaluacion in data[ramo]:
            promedio_ramo =  evaluacion['promedio']
            suma_promedios += promedio_ramo
        suma_promedios = {"promedio_ramo": suma_promedios}
        data[ramo].append(suma_promedios)

        
    
        crear_json_notas(data, filename)
        for i in range(0,3):
            print(" ")
        print("---------- Ramo agregado ----------")
        print(" ")
        print(f"{ramo.capitalize()} ha sido agregado.")
        print(" ")
        print("---------- Ramo agregado ----------")
        for i in range(0,2):
            print(" ")
# Ver el agregar la funcion de notas no convencinales (como las notas de ecodiseño) / intentar acotar

def eliminar_ramo(filename='notas.json'):
    data = leer_json(filename)
    ramo = input("Dime que ramo quieres eliminar: ")
    if ramo in data:
        del data[ramo]
        crear_json_notas(data, filename)
        def print_ramo_eliminado():
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print("---------- Ramo eliminado ----------")
            print(" ")
            print(f"{ramo.capitalize()} ha sido eliminado.")
            print(" ")
            print("---------- Ramo eliminado ----------")
            print(" ")
            print(" ")
            print(" ")
        print_ramo_eliminado()
    else:
        print(" ")
        print(" ")
        print("El ramo no existe.")
        print(" ")
        print(" ")

def imprimir_todas_notas(filename='notas.json'):
    data = leer_json(filename)
    dash = '-' * 40
    print(dash)
    for ramo, notas in data.items():
        print(f"Ramo: {ramo.capitalize()}")
        numero_de_evaluaciones = len(data[ramo])
        contador = 1
        ponderado_necesario = 0
        for evaluacion in notas:
            if contador < numero_de_evaluaciones:
                contador +=1
                if (evaluacion['nota'] == 0):
                    nombre = evaluacion["nombre"]
                    nota = evaluacion["nota"]
                    ponderacion = evaluacion['ponderacion']
                    ponderado_necesario = ponderado_necesario + ponderacion
                    print(f"{nombre} - Nota: {nota}, Ponderación: {ponderacion}")
                elif (evaluacion['nota'] != 0):
                    nombre = evaluacion["nombre"]
                    nota = evaluacion["nota"]
                    ponderacion = evaluacion['ponderacion']
                    print(f"{nombre} - Nota: {nota}, Ponderación: {ponderacion}")
            elif contador == numero_de_evaluaciones:
                promedio_ramo = evaluacion['promedio_ramo']
                promedio_redondeado = round(promedio_ramo, 2)
                if promedio_redondeado >= 3.96:
                    estado = 'YA PASASTE EL RAMO!!!'
                else:
                    estado = (3.96 - promedio_ramo) / ponderado_necesario
                print(' ')
                print(f'Promedio: {promedio_redondeado} / Nota n: {round(estado, 2)}')
                break
        print(dash)
# Arreglar para meter cada cosa en una funcion / intentar acotar

def ver_notas_ramo(filename='notas.json'):
    data = leer_json(filename)
    
    ramo = input("Dime el ramo del que quieres ver las notas: ")
    if ramo in data:
        dash = '-' * 40
        print(dash)
        print(f"Notas de {ramo}:")
        numero_de_evaluaciones = len(data[ramo])
        contador = 1
        ponderado_necesario = 0
        for evaluacion in ramo:
            if contador < numero_de_evaluaciones:
                    print(f"  {evaluacion['nombre']} - Nota: {evaluacion['nota']}, Ponderación: {evaluacion['ponderacion']}")
                    contador += 1   
            elif contador == numero_de_evaluaciones:
                print(" ")
                print(f"Promedio: {evaluacion['promedio_ramo']}")
        print(dash)
    else:
        print("El ramo no existe.")
# Aqui debo arreglarlo

def modificar_ramo(filename='notas.json'):
    data = leer_json(filename)
    ramo = input("Dime el ramo que quieres modificar: ")
    if ramo in data:
        numero_de_evaluaciones = len(data[ramo])
        alala = 1
        dash = '-' * 40
        print(dash)
        print(f"Notas actuales del ramo {ramo}:")
        print(" ")
        for idx, evaluacion in enumerate(data[ramo]):
            if alala < numero_de_evaluaciones:
                alala += 1
                print(f"{idx + 1}. {evaluacion['nombre']} - Nota: {evaluacion['nota']}, Ponderación: {evaluacion['ponderacion']}")
            elif alala == numero_de_evaluaciones:
                break
        print(dash)
        print(" ")
        prueba_idx = int(input("Dime el número de la evaluacion que quieres modificar: ")) - 1
        if 0 <= prueba_idx < (len(data[ramo]) - 1):
            print(" ")
            nueva_nota = float(input("Dime la nueva nota: "))
            print(" ")
            nueva_ponderacion = float(input("Dime la nueva ponderación: "))
            data[ramo][prueba_idx] = {"tipo": data[ramo][prueba_idx]['tipo'], "nombre": data[ramo][prueba_idx]['nombre'], "nota": nueva_nota, "ponderacion": nueva_ponderacion}
            crear_json_notas(data, filename)
            print(" ")
            print(dash)
            print(" ")
            print(f"Evaluacion {prueba_idx + 1} de {ramo.capitalize()} ha sido modificada.")
            print(" ")
            print(dash)
            print(" ")
        else:
            print("Índice de prueba no válido.")
    else:
        print("El ramo no existe.")
# Revisar por el promedio del ramo / intentar acotar

def exportar_a_csv(filename='notas.json'):
    import csv
    data = leer_json(filename)
    csv_filename = 'notas.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ramo", "Prueba", "Nota", "Ponderación"])
        for ramo, notas in data.items():
            for evaluacion in notas:
                writer.writerow([ramo, evaluacion['prueba'], evaluacion['nota'], evaluacion['ponderacion']])
    print(f"Datos exportados a {csv_filename}")
# Arreglar la impresion en el csv

def calcular_promedio_ramo(filename= 'notas.json'):
    data = leer_json(filename)
 
    ramo = input("Dime el ramo al que le quieres calcular el promedio: ")
    if ramo in data:
        suma_ponderada = 0
        suma_ponderaciones = 0
        
        for evaluacion in data[ramo]:
            nota = float(evaluacion['nota'])
            ponderacion = float(evaluacion['ponderacion'])
            suma_ponderada += nota * ponderacion
            suma_ponderaciones += ponderacion
        if suma_ponderaciones != 0:
            promedio = suma_ponderada / suma_ponderaciones
            dash = '-' * 40
            print(dash)
            print(" ")
            print(f"El promedio ponderado de {ramo} es: {promedio:.2f}")
            print(" ")
            print(dash)
        else:
            print("No hay ponderaciones válidas para calcular el promedio.")
    else:
        print("El ramo no existe.")
# Agregar esta funcion para mostrar solo las notas de un ramo en especifico / momentaneamente no funciona

menu() 
