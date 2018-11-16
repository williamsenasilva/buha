import Formularios
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from MyDialog import MyInfo, EditarDisciplina, IncluirDisciplina

import Aluno


# region ALUNO
class FormularioAluno(Formularios.Formulario):
    def __init__(self, root, repositorio=None):
        super().__init__(root, repositorio)
        self.inputs = {}
        self.buttons = {}
        self.prepara_formulario()
        self.ativa_botoes()
        self.top.after(1, lambda: self.top.focus_force())


    def prepara_formulario(self):
        self.prepara_inputs()
        self.prepara_botoes()

    def prepara_botoes(self):
        nome_frame = 'botoes_aluno'
        botoes = ['incluir', 'atualizar', 'buscar']
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
        self.buttons["atualizar"].config(command=self.botao_atualizar)

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
                print("\n buscando rbuha %s..." % rbuha)
                alunoEncontrado = self.busca_por_rbuha(rbuha)
            if rbuha == "andre":
                alunoEncontrado = Aluno.andre
            if rbuha == "joao":
                alunoEncontrado = Aluno.joao

        elif ra:
            alunoEncontrado = self.busca_por_ra(ra, universidade)

        if alunoEncontrado is None:
            MyInfo(self.top, "Não foi possível localizar o aluno solicitado.")
            print(self.repo.alunos)
        else:
            self.abre_janela_disciplinas(alunoEncontrado)

    def botao_incluir(self):
        nome, universidade, ra, rbuha = self.obtem_dados_do_formulario()
        if not (nome and universidade and ra):
            MyInfo(self.top, "Por favor, preencha: Nome, Universidade e RA.")
            return
        if rbuha:
            MyInfo(self.top, self.text['incluir erro buha'])
            txtRbuha = self.inputs['rbuha']
            txtRbuha.delete(0, len(txtRbuha.get()))

            return
        rbuha = self.calcula_rbuha(universidade, ra)
        aluno = Aluno.Aluno(nome, universidade, ra, rbuha, [])
        mensagem = self.texts['aluno incluido'].format(*aluno)
        MyInfo(self.top, mensagem)
        self.repo.inserir_aluno(aluno)


    def busca_por_rbuha(self, rbuha):
        return self.repo.obtem_aluno_por_rbuha(rbuha)

    def busca_por_ra(self, ra, universidade):
        return self.busca_por_rbuha(self.calcula_rbuha(universidade, ra))

    def botao_atualizar(self):
        aluno = self.obtem_dados_do_formulario()
        if (self.valida_dados(nome=True, universidade=True, ra=True, rbuha=True)):
            anterior = self.repo.obtem_aluno_por_rbuha(aluno[3])
            novo = Aluno.Aluno(aluno[0], aluno[1], aluno[2], aluno[3], None)

            if not anterior:
                MyInfo(self.top, "Não existe estudante com esse Registro BUHA. Utilize Incluir.")
                return

            mensagem = "ESSE PROCEDIMENTO NÃO PODE SER DESFEITO!\n"
            mensagem += self.texts['confirmar edicao aluno']
            mensagem += "\nESSE PROCEDIMENTO NÃO PODE SER DESFEITO!"

            tupla_para_mensagem = anterior[0:-1] + novo[0:-1]

            mensagem = mensagem.format(*tupla_para_mensagem)

            confirmacao = messagebox.askokcancel("Atenção", mensagem)
            if confirmacao:
                self.repo.editar_aluno(anterior, novo)
            else:
                MyInfo(self.top, "Alteração Cancelada.")
        else:
            MyInfo(self.top, self.texts['preencher todos os campos'])

    def valida_dados(self, nome=False, universidade=False, ra=False, rbuha=False):
        nome_f, univ_f, ra_f, rbuha_f = self.obtem_dados_do_formulario()
        is_nome_ok = nome_f if nome else True
        is_univ_ok = univ_f if universidade else True
        is_ra_ok = ra_f if ra else True
        is_rbuha_ok = rbuha_f if rbuha else True
        return is_nome_ok and is_univ_ok and is_ra_ok and is_rbuha_ok

    def abre_janela_disciplinas(self, aluno):
        f = FormularioDisciplinas(self._root_reference, self.repo)
        f.set_aluno(aluno)
        self.destroy()
        print("Encerrado Formulario Alunos")

    def calcula_rbuha(self, universidade, ra):
        # TODO: Calcula um hash da universidade+ra
        return str(universidade) + str(ra)


# region DISCIPLINAS
class FormularioDisciplinas(Formularios.Formulario):
    def __init__(self, root, repositorio=None, aluno=Aluno.andre):
        super().__init__(root, repositorio)
        self.hist_tree = None
        self.aluno = aluno
        self.aluno_salvo = Aluno.copia_aluno(aluno)
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
        aluno = self.aluno
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
        # scrollbar(frame, tree)
        tree.pack()
        self.hist_tree = tree
        tree.bind("<<TreeviewSelect>>", self.tree_click_event)
        self.frames[nome_frame] = frame

    def scrollbar(self, parent, tree):
        yScroll = ttk.Scrollbar(parent, orient="vertical")
        xScroll = ttk.Scrollbar(parent, orient="horizontal")
        yScroll.pack(side=RIGHT, fill=Y)
        xScroll.pack(side=BOTTOM, fill=X)
        xScroll.config(command=tree.xview())
        yScroll.config(command=tree.yview())
        tree.config(yscrollcommand=yScroll.set)
        tree.config(xscrollcommand=xScroll.set)


    def tree_click_event(self, event):
        pass
        # t = self.hist_tree
        # row = t.identify_row(event.y)
        # focus = t.focus()
        # print(t, "-", row,"--", focus)

    def obtem_tabela(self, frame, aluno):
        largura_maxima = 600
        largura_colunas = (0.3 * largura_maxima, 0.15 * largura_maxima,
                           0.15 * largura_maxima, 0.1 * largura_maxima, 0.2 * largura_maxima)

        nomes_colunas = ("Disciplina", "Código", "Carga Horária", "Nota", "Conclusão")

        tree = ttk.Treeview(frame, selectmode="browse")

        # Estou adicionando +4 colunas(a #0 já tenho por padrão)
        tree.config(columns=('#1', '#2', '#3', '#4'))

        # Define o nome e tamanho das colunas:
        for i in range(len(largura_colunas)):
            tree.heading("#" + str(i), text=nomes_colunas[i], anchor='w')
            tree.column("#" + str(i), width=int(largura_colunas[i]))

        self.atualiza_tabela(tree, self.aluno)
        return tree

    def atualiza_tabela(self, tree, aluno):
        # Deleta o conteudo da tabela:
        for disc in tree.get_children():
            tree.delete(disc)

        # Adiciona as disciplinas no histórico
        historico = aluno.historico
        index = 0
        if historico is None:
            return
        else:
            for disc in historico:
                tree.insert("", "end", iid=index, text=disc.nome, values=disc[1:])
                index += 1





    def obtem_botoes(self):
        self.prepara_frame_botoes('botoes', ['incluirDisc', 'removerDisc', 'editarDisci', 'salvar', 'reverter', 'sair'])

    def set_aluno(self, novo_aluno):
        print("Aluno Salvo: %s" % str(self.aluno_salvo))
        print("Aluno Novo Aluno: %s" % str(novo_aluno))
        self.aluno = Aluno.copia_aluno(novo_aluno)
        self.reset()


    def reset(self):
        for key, frame in self.frames.items():
            frame.destroy()
        self.prepara_formulario()

    def ativar_botoes(self):
        nomes_botoes = ('incluirDisc', 'removerDisc', 'editarDisci', 'salvar', 'reverter', 'sair')
        funcoes_botoes = (
            self.botao_novo, self.botao_remover, self.botao_editar, self.botao_salvar, self.botao_cancelar,
            self.botao_sair)
        self.conecta_botoes(nomes_botoes, funcoes_botoes)

    def get_selected_index(self):
        index = self.hist_tree.focus()
        if "I" in index:
            print("Index inicial -> Linha 0")
            index = 0
        return int(index)

    def get_index_iid(self, index):
        if index == 0:
            return "I001"
        else:
            return str(index)

    def botao_novo(self):
        IncluirDisciplina(self.top, self)
        pass

    def botao_remover(self):
        Aluno.remove_disciplina(self.aluno, self.get_selected_index())
        self.atualiza_tabela(self.hist_tree, self.aluno)

    def botao_editar(self):
        index = self.get_selected_index()
        print("Editando. Start")
        EditarDisciplina(self.top, self, index)
        print("Editado. End")
        pass

    def botao_salvar(self):
        print("Salvar")
        self.repo.editar_aluno(self.aluno, self.aluno)
        self.aluno_salvo = Aluno.copia_aluno(self.aluno)
        pass

    def botao_cancelar(self):
        self.set_aluno(self.aluno_salvo)
        self.abrir_formulario_alunos()

    def botao_sair(self):
        self.abrir_formulario_alunos()

    def abrir_formulario_alunos(self):
        f = FormularioAluno(self._root_reference, self.repo)
        self.destroy()

# end region
