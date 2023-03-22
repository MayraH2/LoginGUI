# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:14:25 2023

@author: May50x
"""

import tkinter as tk
import numpy as np
import skimage as sk
from tkinter import ttk
from tkinter import filedialog as fd
import mysql.connector as mysql
import io
from PIL import Image, ImageTk

class menu_principal(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        #master es el padre de la clase y es toda la configuración de la ventana
        self.master = master
        self.master.geometry('400x700')
        self.master.resizable(width=0, height=0)
        self.master.title('Ingreso de usuario')
        self.logo = tk.PhotoImage(file='img/usuario.png')
        self.master.iconphoto(False,self.logo)
        self.pack()
        self.create_widgets() #los elementos iniciales
        self.conexion = 0
        
    def conexion_db(self):
	#Creación de conexión con base de datos Mysql
        try:
            self.conexion=  mysql.connect(host='localhost', user='root',
                                    passwd='',db='login')
            self.cursor=self.conexion.cursor()
            return self.cursor
            print('Se ha creado la conexión')
        except:
            print('No se ha podido crear una conexión')
        
    def create_widgets(self):
        #Frame donde se encuentra todo
       self.fondo = tk.PhotoImage(file='img/fondo.png')
       self.frame1 = tk.Label(self, image=self.fondo)
       self.frame1.pack(expand=True,fill='both')
       
       #Mensaje de inicio de sesión
       
       self.mensaje = tk.Label(self, text='¡Hola de nuevo! Inicia sesión',
                                font=('Verdana',18), bg='lavender blush')
       self.mensaje.place(x=20,y=20)
        
       #boton para ingresar los datos
       # self.fuente = tk.font.Font(family='Verdana', weight='bold', size=12)
       self.button1 = tk.Button(self.frame1, text='Iniciar sesión', 
                           fg='black', bg='deep sky blue', width=26,
                           height=3, font=('Georgia',12,'bold'), command=self.verificar,
                           activebackground='blue4',activeforeground='white')
       self.button1.place(x=58,y=420)
       
       #boton para salir de la página
       self.button2 = tk.Button(self,bg='blue',
                                fg='white',text='Salir',
                                width=8,height=2,
                                command = self.master.destroy,
                                font=('Georgia',11))
       self.button2.place(x=300,y=640)
       
       #imagen de usuario decorativa
       self.icono = tk.PhotoImage(file='img/icono.png')      
       self.label1 = tk.Label(self,image=self.icono)
       self.label1.place(x=145,y=90)
       
       #Entrada para el nombre de usuario
       self.usuario_n = tk.StringVar()
       self.ent_usuario = tk.Entry(self, width=45,
                                   textvariable=self.usuario_n)
       self.ent_usuario.place(x=60,y=265)
       
       #Mensaje de  nombre de usuario
       self.men_correo = tk.Label(self, text='Correo electrónico o Usuario',
                                font=('Verdana',10), bg='lavender blush')
       self.men_correo.place(x=60,y=240)
       
       #Entrada para la contraseña
       self.contra_n = tk.StringVar()
       self.ent_contra = tk.Entry(self, width=45,
                                  show='*',textvariable=self.contra_n)
       self.ent_contra.place(x=60,y=370)
       
       #Mensaje de contraseña
       self.men_contra = tk.Label(self, text='Contraseña',
                                font=('Verdana',10), bg='lavender blush')
       self.men_contra.place(x=60,y=345)
       
       #Mensaje para registrarse
       self.men_reg = tk.Label(self, text='¿Eres nuevo(a)?',
                               font=('Verdana',10), bg='lavender blush')
       self.men_reg.place(x=20,y=613)
       
       #Boton de registro
       self.registro = tk.Button(self, text='Registrarse',
                                 fg='black', bg='deep sky blue', width=15,
                                 height=2, font=('Georgia',11,'bold'), command=self.Registro,
                                 activebackground='blue4',activeforeground='white')
       self.registro.place(x=20,y=638)
       
    def verificar(self):
        
        self.conexion_db()

	#Obtención del nombre de usuario
        self.usuario = self.usuario_n.get()
        
        query = ('''SELECT * FROM registros
                    WHERE nombre_usuario = %s
                ''')
        value = (self.usuario,)
        
        self.cursor.execute(query,value)

	#Obtención de todos los datos del usuario de la base de datos
        self.datos_usuario = self.cursor.fetchall()
        
	#Verificación de contraseña del usuario
        if bool(self.datos_usuario):
            contraseña = self.datos_usuario[0][2]
            if contraseña == self.contra_n.get():
                tk.messagebox.showinfo(message=f'Bienvenido de vuelta {self.usuario}',
                                   title='Inicio de sesión')
                self.Perfil()
            else:
                tk.messagebox.showerror(message='Contraseña incorrecta',
                                   title='Advertencia')      
        else:
            tk.messagebox.showerror(message=f'El nombre de usuario {self.usuario} no existe',
                               title='Advertencia') 
            
    def Perfil(self):
	#Ventana para el perfil del usuario
        self.vent2 = tk.Toplevel(self.master)
        self.vent2.geometry('750x500')
        self.vent2.resizable(0,0)
        self.vent2.title('Perfil de usuario')
        self.pack(expand=True, fill="both")
        
        #fondo de la segunda pantalla
        self.pant_2 =tk.Label(self.vent2, bg='#FFFFFF')
        self.pant_2.pack(expand=True,fill='both')
        
        #Recuperar los datos de la base de datos
        self.conexion_db()
        self.query3 = '''SELECT * FROM usuarios
        WHERE nombre_usuario = %s'''
        value =(self.usuario_n.get(),)
        
        self.cursor.execute(self.query3,value)
        self.perfil_us = self.cursor.fetchall()
        
        #Recuperar imagen
        self.ima_perfil = Image.open(io.BytesIO(self.perfil_us[0][3]))
        self.ima_perfil = self.ima_perfil.resize((155,205))
        self.ima_perfil = ImageTk.PhotoImage(self.ima_perfil)
        
        #Marco de la imagen de perfil
        self.marco = tk.Label(self.vent2, bg='#1BAAED',
                              width=25,height=15)
        self.marco.place(x=30,y=25)
        
        #Imagen de perfil del usuario
        self.recuadro = tk.Label(self.marco,bg='#1BAAED',
                                  image=self.ima_perfil)
        self.recuadro.place(x=10,y=10)
        
        #Nombre del usuario
        text1=[self.perfil_us[0][5],self.perfil_us[0][6]]
        text1= ' '.join(text1)
        
        self.name = tk.Text(self.vent2,height=2,width=18,
                            bg='#FFFFFF',font=('Arial',32),
                            relief="flat",borderwidth=0)
        self.name.tag_config("right", justify='right')
        self.name.insert('end', text1)
        self.name.configure(state='disabled')
        self.name.place(x=260,y=40)
           
        # #Profesión del usuario
        text2=['Actualmente soy',self.perfil_us[0][7]]
        text2=' '.join(text2)
    
        self.profe = tk.Text(self.vent2,height=2,width=35,
                            bg='#FFFFFF',font=('Arial',16,'bold'),
                            relief="flat",borderwidth=0)
        self.profe.insert('end', text2)
        self.profe.configure(state='disabled')
        self.profe.place(x=260,y=150)
        
        #Dirección del usuario
        text3=['Vivo en',self.perfil_us[0][9]]
        text3=' '.join(text3)
        
        self.direcc = tk.Text(self.vent2,height=2,width=45,
                            bg='#FFFFFF',font=('Arial',12,'bold'),
                            relief="flat",borderwidth=0)
        self.direcc.insert('end', text3)
        self.direcc.configure(state='disabled')
        self.direcc.place(x=260,y=220)
        
        #Información del usuario
        self.dat_mul = (self.perfil_us[0][0],self.perfil_us[0][1],
                        self.perfil_us[0][2],self.perfil_us[0][4])
        
	#Estilo del cabezal y cuerpo de la tabla Treeview
        style = ttk.Style()
        style.configure("Estilo", bd=0, font=('Arial', 11)) # Modificación de estilo del cuerpo del Treeview
        style.configure("Estilo.Heading", font=('Arial', 12,'bold')) # Modificar los encabezados
        style.layout("Estilo", [('Estilo.treearea', {'sticky': 'nswe'})]) # Quitar los bordes
       
        self.info = ttk.Treeview(self.vent2, columns=[f"#{n}" for n in range(1, 5)],
                                 show='headings',height=2,style='Estilo')
	
	#Encabezados de la tabla
        self.info.heading('#1', text='ID', anchor='center')
        self.info.heading('#2', text='Nombre usuario', anchor='center')
        self.info.heading('#3', text='Correo', anchor='center')
        self.info.heading('#4', text='Contraseña', anchor='center')
        
	#Insertar los datos a la tabla
        self.info.insert('',tk.END,values=self.dat_mul)
        self.info.place(x=30,y=350,width=690)
        
	#Scrollbar horizontal para la tabla 
        scroll = ttk.Scrollbar(self.vent2, orient="horizontal", command=self.info.xview)
        scroll.place(x=30, y=400, width=690)
        self.info.configure(xscrollcommand=scroll.set)
        
        #Boton para cerrar sesión
        self.cer_ses = tk.Button(self.vent2, bg='#9DC5E7',
                                  text='Cerrar Sesión',command=self.Borrar_cont,
                                  font=('Verdana',11,'bold'),width=13)
        self.cer_ses.place(x=550,y=450)
        
        self.conexion.close()
        
        
    def Borrar_cont(self):
        self.ent_usuario.delete(0,'end')
        self.ent_contra.delete(0,'end')
        self.vent2.destroy()
    
    def Registro(self):
        self.vent1 = tk.Toplevel(self.master)
        self.vent1.geometry('600x700')
        self.vent1.resizable(0,0)
        self.vent1.title('Registro de usuario')
        self.pack(expand=True, fill="both")
        
        #fondo de la segunda pantalla
        self.pant_1 =tk.Label(self.vent1, bg='#BEF0FA')
        self.pant_1.pack(expand=True,fill='both')
        
        #Titulo de registro
        self.title_reg = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Registro de nuevo usuario',
                                font=('Verdana',22,'bold'))
        self.title_reg.place(x=83,y=30)
        
        #Entrada para el nombre de usuario
        self.reg_usu = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Nombre de usuario',
                                font=('Verdana',12))
        self.reg_usu.place(x=40,y=130)
        
        #Entry para el nombre de usuario
        self.var_usu=tk.StringVar()
        self.entr_usu = tk.Entry(self.vent1, width=40,
                                 textvariable=self.var_usu)
        self.entr_usu.place(x=40,y=160)
        
        #Entrada para el correo electronico
        self.reg_corr = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Correo electrónico',
                                font=('Verdana',12))
        self.reg_corr.place(x=40,y=210)
        
        #Entry para el correo electrónico
        self.var_corr = tk.StringVar()
        self.entr_corr = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_corr)
        self.entr_corr.place(x=40,y=240)
        
        #Verificación del correo electronico
        self.ver_corr = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Confirma tu correo electrónico',
                                font=('Verdana',12))
        self.ver_corr.place(x=40,y=290)
        
        #Entry para verificación del correo electrónico
        self.var_verc = tk.StringVar()
        self.enve_corr = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_verc)
        self.enve_corr.place(x=40,y=320)
        
        #Entrada para contraseña
        self.reg_cont = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Contraseña',
                                font=('Verdana',12))
        self.reg_cont.place(x=40,y=370)
        
        #Entry para contraseña
        self.var_cont = tk.StringVar()
        self.entr_cont = tk.Entry(self.vent1, width=40,
                                  show='*',textvariable=self.var_cont)
        self.entr_cont.place(x=40,y=400)
        
        #Entrada para el Nombre de la persona
        self.reg_nomper = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Nombre completo',
                                font=('Verdana',12))
        self.reg_nomper.place(x=320,y=130)
        
        #Entry para nombre de la persona
        self.var_noper = tk.StringVar()
        self.entr_nom = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_noper)
        self.entr_nom.place(x=320,y=160)
        
        #Entrada para la profesión del usuario
        self.reg_prof = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Profesión',
                                font=('Verdana',12))
        self.reg_prof.place(x=320,y=210)
        
        #Entry para la profesión
        self.var_prof = tk.StringVar()
        self.entr_prof = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_prof)
        self.entr_prof.place(x=320,y=240)
        
        #Entrada para la edad del usuario
        self.reg_edad = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Edad',
                                font=('Verdana',12))
        self.reg_edad.place(x=320,y=290)
        
        #Entry para la edad
        self.var_edad = tk.StringVar()
        self.entr_edad = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_edad)
        self.entr_edad.place(x=320,y=320)
        
        #Entrada para la dirección
        self.reg_dir = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Dirección',
                                font=('Verdana',12))
        self.reg_dir.place(x=320,y=370)
        
        #Entry para la dirección
        self.var_dir = tk.StringVar()
        self.entr_dir = tk.Entry(self.vent1, width=40,
                                  textvariable=self.var_dir)
        self.entr_dir.place(x=320,y=400)
        
        #Entrada para imagen de perfil
        self.reg_img = tk.Label(self.vent1,bg='#BEF0FA',
                                text='Imagen de perfil',
                                font=('Verdana',12))
        self.reg_img.place(x=40,y=450)
        
        #Mostrar el nombre del archivo
        self.var_img = tk.StringVar()
        self.entr_img = tk.Entry(self.vent1, width=60,
                                 textvariable=self.var_img)
        self.entr_img.place(x=40,y=480)
        
        #Boton para abrir un archivo
        self.arch = tk.Button(self.vent1, bg='#9DC5E7',
                                  text='Examinar',command=self.Abrir_archivo,
                                  font=('Verdana',11,'bold'),width=11)
        self.arch.place(x=420, y=473)
        
        #boton para registrar al usuario
        self.bot_reg = tk.Button(self.vent1, bg='#9DC5E7',
                                  text='Crear una cuenta',command=self.Registrar_usuario,
                                  font=('Verdana',11,'bold'),width=50)
        self.bot_reg.place(x=40,y=550)
        
        #boton para volver al inicio de sesion
        self.bot_volv = tk.Button(self.vent1, bg='#9DC5E7',
                                  text='Volver a inicio \n de sesión',command=self.vent1.destroy,
                                  font=('Verdana',11,'bold'),width=13)
        self.bot_volv.place(x=40,y=625)
        
        
        
    def Abrir_archivo(self):
        self.nom_arch = fd.askopenfilename(initialdir = '/', 
                                           title = 'Seleccione archivo',
                                           filetypes = [("Todos los archivos", "*.*")])
        if self.nom_arch !='':        
            self.entr_img.insert(0,self.nom_arch)
        
    
    def Registrar_usuario(self):
        self.conexion_db()
        self.casillas = [self.var_usu,self.var_corr,self.var_verc,
                         self.var_cont,self.var_noper,self.var_prof,
                         self.var_edad,self.var_dir,self.var_img]
        
        
	#Verificación para que todos los campos tengan valores
        verificacion = 0
        self.values=[]
        for elemento in self.casillas:
            if len(elemento.get()) == 0:
                self.mensaje_registro = tk.messagebox.showerror(message='Por favor rellene todos los campos',
                                   title='Registro de usuario')
                verificacion = 1
                break
        
	#Verificación de que los correos ingresados sean los mismos               
        if (verificacion == 0):
            if (self.entr_corr.get() == self.enve_corr.get()):
		
		#Ingreso de los datos a la base de datos

                self.Conversion_imagen()
                self.casillas.pop(2)
                for dato in range(len(self.casillas)-1):
                    self.values.append(self.casillas[dato].get())
                self.values.append(self.img)
                nombre = self.values[3].split()
                if len(nombre)==3:
                    self.values[3]=nombre[0]
                    self.values.insert(4,(' '.join(nombre[1:])))
                elif len(nombre)==4:
                    self.values[3]=' '.join(nombre[0:2])
                    self.values.insert(4,(' '.join(nombre[2:])))
                self.values = tuple(self.values)
                
                values2 = tuple((self.values[0],self.values[2]))
                query2 = ('''INSERT INTO registros (nombre_usuario,contraseña) 
                         VALUES (%s,%s)
                         ''')
                self.cursor.execute(query2,values2)
                self.conexion.commit()       
                self.mensaje_registro = tk.messagebox.showinfo(message='Su cuenta ha sido registrada',
                           title='Registro de usuario')
                
                self.Crear_perfil()
                
            else:
                self.mensaje_correo = tk.messagebox.showerror(message='Verifique el correo ingresado',
                               title='Registro de usuario')
        
        self.conexion.close()
        
    def Crear_perfil(self):
        
        query = ('''INSERT INTO usuarios (nombre_usuario,correo,contraseña,nombre,apellidos,profesion,edad,direccion,foto_perfil) 
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                  ''')
        self.cursor.execute(query,self.values)
        self.conexion.commit()
                
     
    def Conversion_imagen(self):       
        with open( self.var_img.get(),'rb') as f:
            self.img = f.read()
            
    
            
        
        
            
        
        

window = tk.Tk()
# window['bg']='grey'
# window.attributes('-transparentcolor','grey')
main = menu_principal(window)
main.mainloop()
# window.destroy()

# root = tk.Tk()
# root.geometry('400x300')
# root.title('Ingreso de usuario')

# logo=tk.PhotoImage(file='C:/Users/May50x/Documents/Cursos/Curso_python/usuario.png')
# root.iconphoto(False,logo)




# root.mainloop()