#########################
# Auto-preguntador V 1.0
# Autor: Martín López
#########################

from db import Database
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

db = Database('preguntas.db')

root = tk.Tk()
root.title('Auto-preguntador')
root.geometry("500x500")

# #########################################
# ###### Lógica ###########################
# #########################################

# REFACTOR : usar Diccionarios para ID y Nombre de la Materia
# definimos las variables globales
MATERIAS = []
TEMAS = []

# funciones globales


def listar_materias():
    """Carga las materias desde la DB a la lista"""
    # las cargamos desde la db
    MATERIAS.clear()
    rows = db.obtener_materias()
    for row in rows:
        MATERIAS.append(row[1])


def win_nueva_pregunta():
    """Muestra la ventana para agregar una pregunta"""

    def agregar_pregunta(materia, tema, pregunta, respuesta):
        # la agregamos a la DB
        db.insertar_pregunta(materia, tema, pregunta, respuesta)

        # limpiamos los campos
        pregunta_e.delete(0, tk.END)
        respuesta_e.delete(0, tk.END)

        # confirmamos y cerramos la ventana
        messagebox.showinfo('Pregunta agregada',
                            'Pregunta agregada correctamente')
        nueva_pregunta_top.destroy

    def listar_temas():
        """Carga los temas según la materia elegida"""
        # traemos los temas de la db según la materia
        rows = db.obtener_temas(materia.get())

        # los almacenamos en un diccionario
        temas_dic = {}
        for row in rows:
            temas_dic[row[1]] = row[0]

        # los agregamos a la lista de temas
        for key, value in temas_dic.items():
            TEMAS.append(key)

    def actualizar_temas(*args):
        """Actualiza los nombres de los temas en la lista"""
        # limpiamos el drop de temas
        tema_drop['values'] = []

        # traemos los temas
        rows = db.obtener_temas(materia.get())

        # vaciamos la lista y la poblamos con el resultado
        global TEMAS
        TEMAS = []
        # TEMAS = [t for t, in rows]

        # los almacenamos en un diccionario
        temas_dic = {}
        for row in rows:
            temas_dic[row[1]] = row[0]

        # los agregamos a la lista de temas
        for key, value in temas_dic.items():
            TEMAS.append(key)

        # los asignamos al drop
        tema_drop['values'] = TEMAS

        # dejamos en blanco el primer valor
        tema_drop.set('')

    nueva_pregunta_top = tk.Toplevel()
    nueva_pregunta_top.title('Nueva pregunta')

    # ----------------------------------------
    # - Drop Materias
    # ----------------------------------------

    # cargamos la materia
    listar_materias()

    materia_lbl = tk.Label(nueva_pregunta_top, text='Materia: ')
    materia_lbl.grid(row=0, column=0)

    materia = tk.StringVar()
    try:
        materia.set(MATERIAS[0])
    except:
        print('No se pudieron cargar las materias correctamente')
        materia.set('')

    materia_drop = ttk.Combobox(
        nueva_pregunta_top, values=MATERIAS, width=15, textvariable=materia, state="readonly")
    materia_drop.grid(row=0, column=1)
    # Trace está al pendiende si se actualiza una variable, y ejecuta una función
    materia.trace("w", actualizar_temas)

    # ----------------------------------------
    # - Drop Temas
    # ----------------------------------------

    # Cargamos los temas
    listar_temas()

    tema_lbl = tk.Label(nueva_pregunta_top, text='Tema: ')
    tema_lbl.grid(row=1, column=0)

    tema = tk.StringVar()
    tema.set('')
    tema_drop = ttk.Combobox(
        nueva_pregunta_top, values=TEMAS, width=15, textvariable=tema, state="readonly")
    tema_drop.grid(row=1, column=1)

    # ----------------------------------------
    # - Entry para Preguntas y Respuestas
    # ----------------------------------------

    pregunta_l = tk.Label(nueva_pregunta_top, text='Pregunta: ')
    pregunta_l.grid(row=2, column=0)

    pregunta_e = tk.Entry(nueva_pregunta_top, width=40)
    pregunta_e.grid(row=3, column=0, columnspan=3, padx=10)

    respuesta_l = tk.Label(nueva_pregunta_top, text='Respuesta: ')
    respuesta_l.grid(row=4, column=0, pady=10)

    respuesta_e = tk.Entry(nueva_pregunta_top, width=40)
    respuesta_e.grid(row=5, column=0, columnspan=3, padx=10)

    # ----------------------------------------
    # - Entry para Preguntas y Respuestas
    # ----------------------------------------

    enviar_btn = tk.Button(nueva_pregunta_top, text='Enviar',
                           command=lambda: agregar_pregunta(materia.get(), tema.get(), pregunta_e.get(), respuesta_e.get(),))
    enviar_btn.grid(row=6, column=2, pady=10)

    cancel_btn = tk.Button(nueva_pregunta_top, text='Cancelar',
                           command=nueva_pregunta_top.destroy)
    cancel_btn.grid(row=6, column=1, padx=10, pady=10)

    pregunta_e.focus()

    # ------------ MAIN - LOOP ---------------
    nueva_pregunta_top.mainloop()
    # ----------------------------------------


def win_ver_preguntas():
    """ Ventana para y editar preguntas """
    print('Abre ventana de ver preguntas')
    db.mostrar_preguntas()

    ver_preg_top = tk.Toplevel()
    ver_preg_top.attributes('-topmost', True)
    ver_preg_top.title('Banco de preguntas')

    # lógica
    def render_preguntas(*args):
        # limpiamos la tree
        pregs.delete(*pregs.get_children())

        # consultamos las preguntas
        rows = db.mostrar_preguntas()
        for row in rows:
            # si materia no está seleccionado, carga todas
            if materia.get() == '':
                pregs.insert('', tk.END, row[0],
                             values=(row[4], row[5], row[6]))
            # si materia está seleccionado, carga las de esa materia
            elif row[2] == materia.get():
                pregs.insert('', tk.END, row[0],
                             values=(row[4], row[5], row[6]))

    def modificar_pregunta():
        pass

    def eliminar_pregunta():
        # tomamos la selección
        id = pregs.selection()[0]

        # validamos
        pregunta = db.seleccionar_pregunta(id)
        confirmar_eliminar = messagebox.askokcancel(
            'Eliminar pregunta', '¿Seguro que quiere elminmar la pregunta?\n' + str(pregunta[3]), parent=ver_preg_top)
        if confirmar_eliminar:
            db.eliminar_pregunta(id)
            render_preguntas()
        else:
            pass

    # menú arriba
    materia_lbl = tk.Label(ver_preg_top, text='Materia: ')
    materia_lbl.grid(row=0, column=0)

    # listamos materias
    listar_materias()

    materia = tk.StringVar()
    materia_drop = ttk.Combobox(
        ver_preg_top, values=MATERIAS, width=15, textvariable=materia, state="readonly")
    materia_drop.grid(row=0, column=1)
    materia.trace('w', render_preguntas)

    modificar_btn = tk.Button(ver_preg_top, text='Modificar',
                              command=modificar_pregunta)
    modificar_btn.grid(row=0, column=3)

    eliminar_btn = tk.Button(ver_preg_top, text='Eliminar',
                             command=eliminar_pregunta)
    eliminar_btn.grid(row=0, column=4)

    # tree-view
    pregs = ttk.Treeview(ver_preg_top, selectmode='browse')
    pregs['columns'] = ('Tema', 'Pregunta', 'Respuesta')

    pregs.column('#0', width=0, stretch=tk.NO)
    pregs.column('Tema', width=100, anchor=tk.CENTER)
    pregs.column('Pregunta', width=300, anchor=tk.W)
    pregs.column('Respuesta', width=300, anchor=tk.W)

    pregs.heading('Tema', text='Tema')
    pregs.heading('Pregunta', text='Pregunta')
    pregs.heading('Respuesta', text='Respuesta')

    pregs.grid(row=1, column=0, columnspan=5)

    # botón cerrar
    cerrar_btn = tk.Button(ver_preg_top, text='Cerrar',
                           command=ver_preg_top.destroy)
    cerrar_btn.grid(row=2, column=1)

    # cargamos las preguntas
    render_preguntas()

    # main loop (sub-ventana)
    ver_preg_top.mainloop()


def win_empezar_examen():
    top_empezar_examen = tk.Toplevel()
    top_empezar_examen.title('Configuración del examen')

    # tema : id
    temas_dict = {}

    # tema : checkbutton
    temas_check = {}

    def mostrar_check_temas(*args):
        """Actualiza los Checks en función de la materia elegida"""
        # Limpiamos los diccionarios
        temas_dict.clear()
        temas_check.clear()

        # Limpiamos el frame
        for widget in tema_fr.winfo_children():
            widget.destroy()

        # Traemos los temas de la DB
        rows = db.obtener_temas(materia.get())

        # Poblamos el diccionario con tema : id
        for row in rows:
            temas_dict[row[1]] = row[0]

        # Creamos los checkbuttons
        for tema in temas_dict.keys():

            # Seteamos el texto
            temas_check[tema] = tk.Checkbutton(tema_fr, text=tema)

            # Creamos una variable para cada check
            temas_check[tema].var = tk.IntVar()

            # Asociamos la variable con el checkbutton
            temas_check[tema]['variable'] = temas_check[tema].var

            # Mostramos el botón en la ventana
            temas_check[tema].pack(anchor='w')

    def comenzar_examen(*args):
        """ Abre la ventana de Examen """
        temas_seleccionados = []

        # checkeamos los temas clickeados
        for cb in temas_check.values():
            if cb.var.get():
                # el campo texto del cb, y su correspondiente id según el diccionario de temas e id
                print('Item seleccionado: {}, (id tema = {})'.format(
                    cb['text'], temas_dict[cb['text']]))
                temas_seleccionados.append(temas_dict[cb['text']])
        print(temas_seleccionados)

    materia_lbl = tk.Label(top_empezar_examen, text='Materia: ')
    materia_lbl.grid(row=0, column=0)

    # listamos las materias
    listar_materias()

    materia = tk.StringVar()
    materia_drop = ttk.Combobox(
        top_empezar_examen, values=MATERIAS, width=15, textvariable=materia, state="readonly")
    materia_drop.grid(row=0, column=1)
    materia.trace('w', mostrar_check_temas)

    tema_fr = tk.LabelFrame(
        top_empezar_examen, text='Temas incluídos', padx=10, pady=10)
    tema_fr.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    btn_salir = tk.Button(top_empezar_examen, text='Cancelar',
                          command=top_empezar_examen.destroy)
    btn_salir.grid(row=2, column=0)

    btn_comenzar = tk.Button(
        top_empezar_examen, text='Comenzar examen', command=comenzar_examen)
    btn_comenzar.grid(row=2, column=1)

    # loop
    top_empezar_examen.mainloop()


# #########################################
# ###### Interfaz #########################
# #########################################
# interfaz -> menú principal
titulo_label = tk.Label(
    root, text="Auto Preguntador - V1", font=('Verdana', 20))
titulo_label.pack(padx=20, pady=30)

# frame: EXAMEN
examen_frame = tk.LabelFrame(root, text='Examen', padx=10, pady=10)
examen_frame.pack()

comenzar_examen_btn = tk.Button(
    examen_frame, text='Comenzar examen', command=win_empezar_examen)
comenzar_examen_btn.pack()

# frame: PREGUNTAS
preguntas_frame = tk.LabelFrame(root, text='Preguntas', padx=10, pady=10)
preguntas_frame.pack()

crear_pregunta_btn = tk.Button(
    preguntas_frame, text="Nueva pregunta", command=win_nueva_pregunta)
crear_pregunta_btn.pack()

ver_preguntas_btn = tk.Button(
    preguntas_frame, text='Ver preguntas', command=win_ver_preguntas)
ver_preguntas_btn.pack()


# boton: SALIR
salir_btn = tk.Button(root, text='Salir', command=root.quit)
salir_btn.pack(padx=10, pady=10)

# main loop
root.mainloop()
