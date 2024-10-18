import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk, messagebox

#-------------------------------------Variable global para el Arduino----------------------------------------------------------------------------------
arduino = None

#-------------------------------------Función para conectar al puerto seleccionado---------------------------------------------------------------------
def conectar_arduino():
    global arduino
    puerto_seleccionado = desplegable_puertos.get()
    if puerto_seleccionado:
        try:
            arduino = serial.Serial(port=puerto_seleccionado, baudrate=115200, timeout=0.1)
            messagebox.showinfo("Conexión", f"Conectado a {puerto_seleccionado}")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo conectar: {error}")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un puerto")

# -------------------------------------Función para enviar un valor numérico y recibir respuesta--------------------------------------------------------
def enviar_un_valor():
    global arduino
    if arduino:
        valor = entrada_valor.get()
        if valor.isdigit():
            try:
                arduino.write(bytes(valor, 'utf-8'))
                time.sleep(0.05)
                respuesta = arduino.readline().decode('utf-8').strip()
                etiqueta_respuesta.config(text=f"Resultado: {respuesta}")
            except Exception as error:
                messagebox.showerror("Error", f"Error al comunicar: {error}")
        else:
            messagebox.showwarning("Advertencia", "Ingrese un número válido")
    else:
        messagebox.showwarning("Advertencia", "Conéctese a un puerto primero")

#---------------------------------------Función para listar los puertos disponibles---------------------------------------------------------------------
def listar_num_puertos():
    puertos = serial.tools.list_ports.comports()
    lista_puertos = [puerto.device for puerto in puertos]
    desplegable_puertos['values'] = lista_puertos

#-------------------------------------------------Crear la ventana principal---------------------------------------------------------------------------
ventana_principal = tk.Tk()
ventana_principal.title("Interfaz de la ESP32 en Python")
ventana_principal.geometry("400x400")

#----------------------------------------------------Widgets de la interfaz---------------------------------------------------------------------------
marco_principal = tk.Frame(ventana_principal)
marco_principal.pack(pady=20)

etiqueta_puerto = tk.Label(marco_principal, text="Seleccione el puerto:")
etiqueta_puerto.grid(row=0, column=0, padx=5)

desplegable_puertos = ttk.Combobox(marco_principal, state="readonly")
desplegable_puertos.grid(row=0, column=1, padx=5)

boton_listar_puertos = tk.Button(marco_principal, text="Listar puertos", command=listar_num_puertos)
boton_listar_puertos.grid(row=0, column=2, padx=5)

boton_conectar = tk.Button(ventana_principal, text="Conectar", command=conectar_arduino)
boton_conectar.pack(pady=10)

entrada_valor = tk.Entry(ventana_principal)
entrada_valor.pack(pady=5)
entrada_valor.insert(0, "Ingrese un número")

boton_enviar = tk.Button(ventana_principal, text="Enviar", command=enviar_un_valor)
boton_enviar.pack(pady=5)

etiqueta_respuesta = tk.Label(ventana_principal, text="Resultado: ")
etiqueta_respuesta.pack(pady=10)

#-----------------------------------------------------Iniciar el loop de la interfaz-----------------------------------------------------------------
ventana_principal.mainloop()