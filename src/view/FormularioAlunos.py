import Formularios
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from MyDialog import MyInfo, EditarDisciplina

import Aluno

# region aluno
class FormularioAluno(Formularios.Formulario):
    def __init__(self, root):
        super().__init__(root)
        self.inputs = {}
        self.buttons = {}
        self.prepara_formulario()
        self.ativa_botoes()

    def prepara_formulario(self):
        self.prepara_inputs()
        self.prepara_botoes()

    def prepara_botoes(self):
        nome_frame = 'botoes_aluno'
        botoes = ['incluir', 'buscar']
        self.prepara_frame_botoes('botoes_aluno', botoes)
        self.frames[nome_frame].pack(padx=(10, 10), pady=(10, 10))

    def prepara_inputs(self):
        campos = ['nome', 'universidade', 'ra', 'rbuha']
        nome_frame = 'formulario_aluno'
        self.prepara_frame_formulario(nome_frame, campos)
        self.frames[nome_frame].pack(padx=(10, 10), pady=(10, 10))

    def ativa_botoes(self):
        self.buttons["buscar"].config(command=self.botao_busca)
        self.buttons["incluir"].config(command=self.botao_incluir)

    def obtem_dados_do_formulario(self):
        nome = self.inputs['nome'].get()
        universidade = self.inputs['universidade'].get()
        ra = self.inputs['ra'].get()
        rbuha = self.inputs['rbuha'].get()

        return (nome, universidade, ra, rbuha)

    def botao_busca(self):
        nome, universidade, ra, rbuha = self.obtem_dados_do_formulario()
        if not (rbuha or (universidade and ra)):
            mensagem = "Para localizar um aluno é preciso de seu Registro BUHA ou então de sua Universidade e RA."
            MyInfo(self.top, mensagem)
            return
        mensagem = "Localizando estudante "
        if nome:
            mensagem += str(nome) + " "
        if universidade:
            mensagem += "da universidade " + str(universidade)
        if ra:
            mensagem += "\nRA (" + str(ra) + ")"
        if rbuha:
            mensagem += "\nRBUHA (" + str(rbuha) + ")"
        MyInfo(self.top, mensagem)

        alunoEncontrado = None
        if (rbuha):
            if not (rbuha == "andre" or rbuha == "joao"):
                alunoEncontrado = self.busca_por_rbuha(rbuha)
            if rbuha == "andre":
                alunoEncontrado = Aluno.andre
            if rbuha == "joao":
                alunoEncontrado = Aluno.joao
        if (ra):
            alunoEncontrado = self.busca_por_ra(ra, universidade)
        if alunoEncontrado is None:
            MyInfo(self.top, "Não foi possível localizar o aluno solicitado.")
        else:
            self.abre_janela_disciplinas(alunoEncontrado)


    def botao_incluir(self):
        nome, universidade, ra, rbuha = self.obtem_dados_do_formulario()
        if not (nome and universidade and ra):
            MyInfo(self.top, "Por favor, preencha: Nome, Universidade e RA.")
            return
        if rbuha:
            MyInfo(self.top, "O sistema calculará o valor do Registro Buha automaticamente.\n" +
                   "Por favor preencha apenas Nome, Universidade e RA.")
            txtRbuha = self.inputs['rbuha']
            txtRbuha.delete(0, len(txtRbuha.get()))

            return
        rbuha = self.calcula_rbuha(universidade, ra)
        aluno = Aluno.Aluno(nome, universidade, ra, rbuha, None)
        mensagem = "Aluno Incluído: "+nome+" ("+universidade+")"
        mensagem += "\nRA("+ra+")\nRBuha("+rbuha+")"
        MyInfo(self.top, mensagem)

        # TODO Essa função deverá incluir o aluno na CHORD.

    def busca_por_rbuha(self, rbuha):
        #TODO Realiza uma busca real no CHORD.
        print("A implementar busca por rbuha.")
        for i in range(10000 * 10):
            print(str(i))
        return None

    def busca_por_ra(self, ra, universidade):
        return self.busca_por_rbuha(self.calcula_rbuha(universidade, ra))

    def abre_janela_disciplinas(self, aluno):
        f = FormularioDisciplinas(self._root_reference)
        f.set_aluno(aluno)
        self.destroy()
        print("Encerrado Formulario Alunos")

    def calcula_rbuha(self, universidade, ra):
        #TODO: Calcula um hash da universidade+ra
        return str(universidade)+'-'+str(ra)

# end region

# region DISCIPLINAS
class FormularioDisciplinas(Formularios.Formulario):
    def __init__(self, root, aluno=Aluno.andre):
        super().__init__(root)
        self.hist_tree = None
        self.aluno = aluno
        self.prepara_formulario()



    def prepara_formulario(self):
        self.prepara_frame_subtitulo('HISTÓRICO', 16)
        self.prepara_frame_aluno('aluno')
        self.prepara_frame_historico('historico')

        self.obtem_botoes()
        self.ativar_botoes()

        self.frames['subtitulo'].pack(side=TOP, anchor='w', padx=5)
        self.frames['aluno'].pack(anchor='w', padx=10, pady=10)
        self.frames['botoes'].pack(anchor='c', padx=10, pady=(5, 0))
        self.frames['historico'].pack(side=BOTTOM, padx=10, pady=10)


    def prepara_frame_subtitulo(self, subtitulo, tamanho):
        frame = Frame(self.top, )
        fonte = 'Arial'
        v_pad = (10, 50)
        h_pad = (10, 10)
        lbl = ttk.Label(frame, text=subtitulo, font=(fonte, tamanho))
        lbl.pack(padx=v_pad, pady=h_pad, )
        self.frames['subtitulo'] = frame

    def prepara_frame_aluno(self, nome_frame):
        frame = LabelFrame(self.top, text=self.texts['estudante'])
        fonte = ('Arial', 10)
        aluno = self.aluno;
        nome = ttk.Label(frame, text=aluno.nome, font=fonte)
        universidade = ttk.Label(frame, text=aluno.universidade, font=fonte)

        textoRa = "Registro na Universidade: " + aluno.ra
        textoRBUHA = "Registro BUHA: " + aluno.rbuha
        ra = ttk.Label(frame, text=textoRa, font=fonte)
        rbuah = ttk.Label(frame, text=textoRBUHA, font=fonte)
        nome.pack(anchor='w')
        universidade.pack(anchor='w')
        ra.pack(anchor='w')
        rbuah.pack(anchor='w')
        self.frames[nome_frame] = frame

    def prepara_frame_historico(self, nome_frame):
        frame = Frame(self.top)
        tree = self.obtem_tabela(frame, self.aluno)
        yScroll = ttk.Scrollbar(frame, orient="vertical")
        xScroll = ttk.Scrollbar(frame, orient="horizontal")
        # yScroll.pack(side=RIGHT, fill=Y)
        # xScroll.pack(side=BOTTOM, fill=X)

        tree.pack()
        # xScroll.config (command = tree.xview())
        # yScroll.config(command=tree.yview())
        # tree.config(yscrollcommand=yScroll.set)
        # tree.config(xscrollcommand=xScroll.set)
        self.hist_tree = tree
        tree.bind("<<TreeviewSelect>>", self.tree_click_event)

        self.frames[nome_frame] = frame


    def tree_click_event(self, event):
        pass
        # t = self.hist_tree
        # row = t.identify_row(event.y)
        # focus = t.focus()
        # print(t, "-", row,"--", focus)

    def obtem_tabela(self, frame, aluno):
        historico = aluno.historico
        quantidade_de_materias = len(historico)

        largura_maxima = 600
        largura_colunas = (0.3 * largura_maxima,
                           0.15 * largura_maxima,
                           0.15 * largura_maxima,
                           0.1 * largura_maxima,
                           0.2 * largura_maxima)
        nome_colunas = ("Disciplina", "Código", "Carga Horária", "Nota", "Conclusão")

        # Estou adicionando +4 colunas(a #0 já tenho por padrão)
        tree = ttk.Treeview(frame,
                            columns=('#1', '#2', '#3', '#4'))

        for i in range(5):
            tree.heading("#" + str(i), text=nome_colunas[i], anchor='w')
            tree.column("#" + str(i), width=int(largura_colunas[i]))
            # print("Alterado tamanho da col "+str(i)+" para "+str(largura_colunas[i]))

        index = 0
        for disc in historico:
            # print("Adicionando "+str(disc))
            print(disc.nome)
            print(index)
            tree.insert("", "end", iid=index, text=disc.nome, values=disc[1:])
            index += 1


        return tree

    def obtem_botoes(self):
        self.prepara_frame_botoes('botoes', ['incluirDisc', 'removerDisc', 'editarDisci', 'salvar', 'reverter'])

    def set_aluno(self, novo_aluno):
        print("Setting novo aluno: "+str(novo_aluno))
        self.aluno = novo_aluno
        self.reset()

        print("Novo Aluno")

    def reset(self):
        for key, frame in self.frames.items():
            frame.destroy()
        self.prepara_formulario()

    def ativar_botoes(self):
        nomes_botoes = ('incluirDisc', 'removerDisc', 'editarDisci', 'salvar', 'reverter')
        funcoes_botoes = (self.botao_novo, self.botao_remover, self.botao_editar, self.botao_salvar, self.botao_cancelar);
        self.conecta_botoes(nomes_botoes, funcoes_botoes)


    def get_selected_index(self):
        index = self.hist_tree.focus()
        if index=="I001":
            print("Index inicial -> Linha 0")
            index = 0;
        return int(index)

    def botao_novo(self):
        print("Novo")
        pass


    def botao_remover(self):
        print("Remover")
        print(self.get_selected_index())
        pass

    def botao_editar(self):

        index = self.get_selected_index()
        print("Editando. Start")
        EditarDisciplina(self.top, self, index)
        print("Editado. End")
        pass

    def botao_salvar(self):
        print("Salvar")
        #TODO Essa função deverá salvar as alterações na CHORD.
        pass

    def botao_cancelar(self):
        self.abrir_formulario_alunos();

    def abrir_formulario_alunos(self):
        f = FormularioAluno(self._root_reference)
        self.destroy()

# end region
