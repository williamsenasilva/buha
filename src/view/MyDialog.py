from tkinter import *
from tkinter import ttk
import Aluno

class MyDialog:
    def __init__(self, parent):

        top = self.top = Toplevel(parent)
        ttk.Label(top, text="Value").pack()

        self.e = ttk.Entry(top)
        self.e.pack(padx=5)

        b = ttk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()

class MyInfo:
    def __init__(self, parent, message):
        top = self.top = Toplevel(parent)
        ttk.Label(top, text=message).pack(padx=20, pady=10)

        b = ttk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()



class EditarDisciplina:

    def __init__(self, parent, formulario_disciplinas, index_disciplina):
        top = self.top = Toplevel(parent)
        self.formulario = formulario_disciplinas
        self.aluno = formulario_disciplinas.aluno
        self.disciplina = self.aluno.historico[index_disciplina]
        self.index_disciplina = index_disciplina


        ttk.Label(top, text="Editar Disciplina").pack(padx=20, pady=10)
        self.NOMES_CAMPOS = ("Disciplina", "Código", "Carga Horária", "Nota", "Conclusão")
        self.ID_CAMPOS = ('nome', 'cod', 'carga_horaria', 'nota', 'conclusao')

        self.campos = {}
        self.prepara_campos(self.disciplina)

        b = ttk.Button(top, text="OK", command=self.ok)
        b2 = ttk.Button(top, text="Cancelar", command=self.cancelar)
        b.pack(pady=5)
        b2.pack(pady=5)

    def prepara_campos(self, disciplina):
        currRow = 0

        frame = Frame(self.top)
        for i in range(len(self.NOMES_CAMPOS)):
            string_var = self.campos[self.ID_CAMPOS[i]] = StringVar()
            string_var.set(str(disciplina[i]))
            nome_campo = self.NOMES_CAMPOS[i]
            label = ttk.Label(frame, text=nome_campo)
            label.grid(row=currRow, column=0, padx=(10, 10), pady=(5, 5))
            entryTxt = ttk.Entry(frame, textvariable=string_var)
            entryTxt.grid(row=currRow, column=1, padx=(10, 10), pady=(5, 5))
            currRow += 1
        frame.pack()

    def ok(self):
        dados_disciplina = self.campos;
        nova_disciplina = Aluno.Disciplina(dados_disciplina['nome'].get(),
                                           dados_disciplina['cod'].get(),
                                           dados_disciplina['carga_horaria'].get(),
                                           dados_disciplina['nota'].get(),
                                           dados_disciplina['conclusao'].get())

        novo_historico = self.aluno.historico
        novo_historico[self.index_disciplina] = nova_disciplina
        nome = self.aluno.nome
        univ = self.aluno.universidade
        ra = self.aluno.ra
        rbuha = self.aluno.rbuha
        novo_aluno = Aluno.Aluno(nome, univ, ra, rbuha, novo_historico)
        print("Dialog - novo_aluno")
        print(novo_aluno)
        self.formulario.set_aluno(novo_aluno)
        self.top.destroy()

    def cancelar(self):
        self.top.destroy()