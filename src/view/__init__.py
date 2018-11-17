# -*- coding: utf-8 -*-
import FormularioAlunos as fa
from tkinter import Tk
import tkinter as tk


print("Start")
root = Tk()
root.title("Base Unificada de Histórico Acadêmico")
root.withdraw()



#root.geometry("600x400")
#root.pack_propagate(0)
formulario = fa.FormularioAluno(root)
#formulario = fa.FormularioDisciplinas(root)
root.mainloop()
print("fim")