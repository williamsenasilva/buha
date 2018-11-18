# -*- coding: utf-8 -*-
import view.FormularioAlunos as fa
from tkinter import Tk
from tkinter import ttk
import tkinter as tk


class Buha_gui:
    def __init__(self, repositorio=None):
        print("Start.")

        root = Tk()
        root.title("Base Unificada de Histórico Acadêmico")
        root.withdraw()
        # root.geometry("600x400")
        formulario = fa.FormularioAluno(root, repositorio)
        root.mainloop()

        print("Fim.")


if __name__ == "__main__":
    b = Buha_gui()
