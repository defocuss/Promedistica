import json
import time
import csv

class Ramo:
    def __init__(self, nombre, evaluaciones):
        self.nombre = nombre
        self.evaluaciones = evaluaciones
            
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'evaluaciones': [e.to_dict() for e in self.evaluaciones]
        }

class Evaluacion:
    def __init__(self, tipo, nota, ponderacion):
        self.tipo = tipo
        self.nota = nota
        self.ponderacion = ponderacion
        
    def to_dict(self):
        return {
            'tipo': self.tipo,
            'nota': self.nota,
            'ponderacion': self.ponderacion
        }
    
class Menu:
    @staticmethod
    def menu():
        while True:
            time.sleep(3)
            print("\nPromedistica:")
            print("1. Agregar Ramo y Notas")
            print("2. Ver notas de un ramo")
            print("3. Modificar Ramo/Nota")
            print("4. Eliminar Ramo")
            print("5. Ver notas")
            print("6. Exportar a un CSV")
            print("7. Salir")
            print(" ")
            opcion = Menu.leer_opcion_menu()
            gestor_evaluaciones = Gestor_Evaluaciones()
            if opcion == '1':
                gestor_evaluaciones.agregar_ramo()
            elif opcion == '2':
                gestor_evaluaciones.ver_notas_especifico()
            elif opcion == '3':
                gestor_evaluaciones.modificar_ramo()
            elif opcion == '4':
                gestor_evaluaciones.eliminar_ramo()
            elif opcion == '5':
                gestor_evaluaciones.imprimir_datos()
            elif opcion == '6':
                gestor_evaluaciones.exportar_a_csv()
            elif opcion == '7':
                print("Programa Terminado :)")
                break
    
    @staticmethod
    def leer_opcion_menu():
        while True:
            opcion = input("Seleccione una opción: ")
            try:
                if int(opcion) >= 1 and int(opcion) <=7:
                    return opcion
            except ValueError:
                pass
            print("Por favor seleccione una opcion válida!")
            
class Gestor_Archivo:
    @staticmethod
    def guardar_datos(ramos, filename='notas.json'):
        with open(filename, 'w') as file:
            json.dump([r.to_dict() for r in ramos], file, indent=4)

    @staticmethod
    def cargar_datos(filename='notas.json'):
        try:
            with open(filename, 'r') as file:
                try:
                    ramos_data = json.load(file)
                    if not ramos_data:
                        return []
                except json.JSONDecodeError:
                    return []
                
                ramos = []
                for data in ramos_data:
                    nombre = data['nombre']
                    evaluaciones_data = data['evaluaciones']
                    evaluaciones = [Evaluacion(e['tipo'], e['nota'], e['ponderacion']) for e in evaluaciones_data]
                    ramo = Ramo(nombre, evaluaciones)
                    ramos.append(ramo)
                return ramos
        except FileNotFoundError:
            return []
        
class Gestor_Evaluaciones:
    def __init__(self):
        self.ramos = Gestor_Archivo.cargar_datos()
    
    def ramo_existe(self, nombre_ramo):
        for ramo in self.ramos:
            if ramo.nombre == nombre_ramo:
                return True
            
        return False 
    
    def agregar_evaluacion(self, n_evaluaciones, tipo):
        lista_evaluaciones = []
        for x in range(n_evaluaciones):
                print(f"\nAgregar {tipo} {x + 1}:")
                nota = input(f"Dime la nota de este/a {tipo}: ")
                variable = True
                while variable:
                    try:
                        nota = float(nota)
                        variable = False
                    except ValueError:
                        nota = input("Agregue una nota valida: ")
                ponderacion = input(f"Dime cuanto es la ponderacion de este/a {tipo}: ")
                variable = True
                while variable:
                    try:
                        ponderacion = float(ponderacion)
                        variable = False
                    except ValueError:
                        ponderacion = input("Agregue una ponderacion valida valida: ")
                evaluacion = Evaluacion(f'{tipo} {x + 1}', nota, ponderacion)
                lista_evaluaciones.append(evaluacion)
        return lista_evaluaciones
            
    def agregar_ramo(self):
        nombre_ramo = input('Dime el nombre del ramo que quieres agregar: ')
        if not self.ramo_existe(nombre_ramo):
            n_evaluaciones = int(input('Dime cuantas pruebas quieres agregar: '))
            lista_1 = self.agregar_evaluacion(n_evaluaciones, 'Prueba')
            n_evaluaciones = int(input('Dime cuantos controles quieres agregar: '))
            lista_2 = self.agregar_evaluacion(n_evaluaciones, 'Control')
            evaluaciones = lista_1 + lista_2
            ramo = Ramo(nombre_ramo, evaluaciones)
            self.ramos.append(ramo)
            Gestor_Archivo.guardar_datos(self.ramos)
            print(f'{nombre_ramo} ha sido agregado')
            return
        print('Este ramo ya existe, pruebe modificando sus notas.')
        
    def imprimir_datos(self):
        dash = '-' * 40
        print(dash)
        for ramo in self.ramos:
            print(f"Ramo: {ramo.nombre.capitalize()}")
            suma_ponderaciones_sin_nota = 0
            for evaluacion in ramo.evaluaciones:
                if (evaluacion.nota == 0):
                    print(f"{evaluacion.tipo} - Nota: {evaluacion.nota}, Ponderacion: {evaluacion.ponderacion}")
                    suma_ponderaciones_sin_nota = suma_ponderaciones_sin_nota + evaluacion.ponderacion
                else:
                    print(f"{evaluacion.tipo} - Nota: {evaluacion.nota}, Ponderacion: {evaluacion.ponderacion}")
            print(' ') 
            print(f'Promedio actual:  {self.promedio_actual_ramo(ramo)} / Nota necesaria: {self.calculo_de_nota_necesaria(ramo, suma_ponderaciones_sin_nota)}')
            print(dash)

    def calculo_de_nota_necesaria(self,nombre_ramo, suma_ponderaciones_sin_nota):
        promedio_actual = self.promedio_actual_ramo(nombre_ramo)
        if suma_ponderaciones_sin_nota == 0:
            if 3.6 <= promedio_actual < 3.96:
                return 'Te fuiste a examen'
            elif promedio_actual < 3.6:
                return 'NOOO HMRN TE ECHASTE EL RAMO'
            return 'YA PASASTE EL RAMOOOO!!!'
        return round((3.96 - promedio_actual) / suma_ponderaciones_sin_nota, 2)           
    
    def promedio_actual_ramo(self,ramo):
        suma_promedios = 0
        for evaluacion in ramo.evaluaciones:
            suma_promedios += evaluacion.nota * evaluacion.ponderacion
        return round(suma_promedios, 2)  
    
    def ver_notas_especifico(self):
        nombre_ramo = input('Dime el ramo del que quieres ver las notas: ')
        dash = '-' * 40
        print(dash)
        for ramo in self.ramos:
            if ramo.nombre == nombre_ramo:
                print(f"Ramo: {nombre_ramo.capitalize()}")
                suma_ponderaciones_sin_nota = 0
                for evaluacion in ramo.evaluaciones:
                    if (evaluacion.nota == 0):
                        print(f"{evaluacion.tipo} - Nota: {evaluacion.nota}, Ponderacion: {evaluacion.ponderacion}")
                        suma_ponderaciones_sin_nota = suma_ponderaciones_sin_nota + evaluacion.ponderacion
                    else:
                        print(f"{evaluacion.tipo} - Nota: {evaluacion.nota}, Ponderacion: {evaluacion.ponderacion}")
                print(' ') 
                print(f'Promedio actual:  {self.promedio_actual_ramo(ramo)} / Nota necesaria: {self.calculo_de_nota_necesaria(ramo, suma_ponderaciones_sin_nota)}')
                print(dash)
        
    def modificar_ramo(self):
        nombre_ramo = input('Dime el ramo que quieres modificar: ')
        dash = '-' * 40
        if self.ramo_existe(nombre_ramo):
            for ramo in self.ramos:
                if ramo.nombre == nombre_ramo:
                    print(dash)
                    print(f'Notas actuales de {nombre_ramo}')
                    print(" ")
                    for idx, evaluacion in enumerate(ramo.evaluaciones):
                        print(f'{idx + 1}. {evaluacion.tipo} - Nota: {evaluacion.nota}, Ponderacion: {evaluacion.ponderacion}')
                    print(dash)
                    print(" ")
                    prueba_idx = int(input("Dime el número de la evaluacion que quieres modificar: ")) - 1
                    if 0 <= prueba_idx <= len(ramo.evaluaciones):
                        nueva_nota = float(input("Dime la nueva nota: "))
                        nueva_ponderacion = float(input("Dime la nueva ponderación: "))
                        ramo.evaluaciones[prueba_idx].nota = nueva_nota
                        ramo.evaluaciones[prueba_idx].ponderacion = nueva_ponderacion
                        Gestor_Archivo.guardar_datos(self.ramos)
                        print(f'La evaluacion {evaluacion.tipo} de {nombre_ramo.capitalize()} ha sido modificada correctamente.')
                    else:
                        print('El nuemero ingresado es incorrecto.')
        else:
            print(f'{nombre_ramo} no existe actulmente.')
     
    def eliminar_ramo(self):
        nombre_ramo = input('Dime el ramo que quieres eliminar: ')
        if self.ramo_existe(nombre_ramo):
            for ramo in self.ramos:
                if ramo.nombre == nombre_ramo:
                    self.ramos.remove(ramo)
                    Gestor_Archivo.guardar_datos(self.ramos)
                    print(f"{nombre_ramo} ha sido eliminado.")
        else:
            print('Este ramo no existe actualmente.')
            
    def exportar_a_csv(self):
        csv_filename = 'notas.csv'
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ramo", "Evaluacion", "Nota", "Ponderacion"])
            for ramo in self.ramos:
                for evaluacion in ramo.evaluaciones:
                    writer.writerow([f'{ramo.nombre}', f'{evaluacion.tipo}', f'{evaluacion.nota}', f'{evaluacion.ponderacion}'])
                writer.writerow([ ])
        print(f"Datos exportados a {csv_filename}")             
                  
Menu.menu()