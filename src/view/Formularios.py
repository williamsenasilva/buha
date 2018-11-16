from tkinter import *
from tkinter import ttk
import tkinter as tk
import RepositorioDeAlunos as Repositorio
import MyDialog

from tkinter.ttk import Entry

# Chaves #
'''
'titulo'
'nome'
'universidade'
'ra'
'rbuha'
'historico' 
'buscar'
'incluir'
'atualizar'
'incluirDisc'
'removerDisc'
'editarDisci'
'''
class Formulario(object):
    def __init__(self, root, repositorio=None):
        print("Inicializando formulario.")
        self.top = tk.Toplevel(root)
        self._root_reference = root
        if repositorio is None:
            self.repo = Repositorio.Repositorio()
        else:
            self.repo = repositorio

        self.texts = {}
        self.frames = {}
        self.buttons = {}

        self.prepara_textos()
        self.prepara_header()

    def prepara_textos(self):
        self.texts = MyDialog.get_strings()


    def prepara_header(self,):
        fonte = 'Arial'
        size = 20
        v_pad = (10, 50)
        h_pad = (10, 10)
        frame = Frame(self.top)
        header_text = self.texts.get('titulo', "Não Localizado Titulo")


        lbl = ttk.Label(frame, text=header_text, font=(fonte, size))
        lbl.pack(padx=v_pad, pady=h_pad)
        self.frames['header'] = frame
        frame.pack(side=TOP)

    def prepara_frame_formulario(self, nome_frame, campos):
        frame = Frame(self.top)
        currRow = 0
        for campo in campos:
            texto_label = self.texts.get(campo, "Campo Nao encontrado")
            label = ttk.Label(frame, text=texto_label)
            label.grid(row=currRow, column=0, padx=(10,10), pady=(5,5))
            entryTxt = ttk.Entry(frame)
            entryTxt.grid(row=currRow, column=1,  padx=(10,10), pady=(5,5))
            self.inputs[campo] = entryTxt
            currRow += 1
        self.frames[nome_frame] = frame

    def prepara_frame_botoes(self, nome_frame, botoes):
        frame = Frame(self.top)
        currColumn = 0
        currLine = 0
        for botao in botoes:
            texto_botao = self.texts.get(botao, "Nao Encontrado")
            btn = ttk.Button(frame, text=texto_botao)
            btn.grid(row=currLine, column=currColumn)
            self.buttons[botao] = btn;
            currColumn += 1
        self.frames[nome_frame] = frame

    def conecta_botoes(self, identificadores, funcoes):
        for nome, func in zip(identificadores, funcoes):
            self.buttons[nome].config(command=func)
            #print("Configurado "+nome)

    def destroy(self):
        for key, frame in self.frames.items():
            frame.destroy()
        self.top.destroy()




