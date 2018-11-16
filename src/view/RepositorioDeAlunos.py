from Aluno import Aluno, Disciplina
import Aluno as A


class Repositorio:
    def __init__(self, teste=True):
        self.alunos = []
        if teste:
            self.base_de_testes()

    def base_de_testes(self):
        historicos = [
            [Disciplina("Fenômenos Térmicos", "BCJ0205-13", 4, "E", "02 de 2014"),
             Disciplina("Fenômenos Mecânicos", "BCJ0208-13", 5, "E", "02 de 2014"),
             Disciplina("Fenômenos Eletromagnéticos", "BCJ0209-13", 5, "E", "02 de 2014"),
             Disciplina("Processamento da Informação", "BCM0505-13", 5, "E", "02 de 2014")],

            [Disciplina("Fenômenos Térmicos", "BCJ0205-13", 4, "E", "02 de 2014"),
             Disciplina("Fenômenos Mecânicos", "BCJ0208-13", 5, "E", "02 de 2014"),
             Disciplina("Fenômenos Eletromagnéticos", "BCJ0209-13", 5, "E", "02 de 2014"),
             Disciplina("Processamento da Informação", "BCM0505-13", 5, "E", "02 de 2014")]

        ]

        self.alunos = [
            Aluno("André Rodrigues Barbosa", "UFABC", "11001814", "1", historicos[0]),
            Aluno("João Da Silva", "UTI", "1", "2", historicos[1])
        ]

    def inserir_aluno(self, aluno):
        print("Repo: Inserindo aluno", aluno)
        if self._aluno_ja_existe(aluno):
            return False
        else:
            self.alunos.append(aluno)
            print(self.alunos)
            return True

    def remover_aluno(self, aluno):
        if self._aluno_ja_existe(aluno):
            a_remover = self._get_aluno_by_rbuha(aluno.rbuha)
            self.alunos.remove(a_remover)

    def editar_aluno(self, aluno_anterior, novo_aluno):
        # print("Editando aluno. Antes %s\n\tDepois %s." %(aluno_anterior, novo_aluno))
        a_editar = self._get_index_of_rbuha(aluno_anterior.rbuha)
        #  print("Index = %d" % a_editar)
        if a_editar is not -1:
            #      print("Efetuando alteracao")
            self.alunos[a_editar] = novo_aluno
            return True
        else:
            #      print("Aluno não encontrado. Inserindo")
            return self.inserir_aluno(novo_aluno)

    def obtem_aluno_por_rbuha(self, rbuha):
        # print("Repo: obtem aluno por rbuha")
        return self._get_aluno_by_rbuha(rbuha)

    def _aluno_ja_existe(self, aluno):
        return any(map(lambda a: a.rbuha == aluno.rbuha, self.alunos))

    def _get_aluno_by_rbuha(self, rbuha):
        # print("Repo _get_aluno_by_rbuha(%s)" %rbuha)
        for a in self.alunos:
            a_rbuha = a.rbuha
            #    print("checando %s" %a_rbuha)
            if a_rbuha == rbuha:
                return a
        # print("Todos os elementos verificados.")
        # print(self.alunos)
        return None

    def _get_index_of_rbuha(self, rbuha_desejado):
        #    print("\t\tget_index_of_rbuha. Desejado: {}".format(rbuha_desejado))
        for i in range(len(self.alunos)):
            rbuha_aluno = self.alunos[i].rbuha
            #       print("\t\tI = %s, RBUHA=%s" %(i, rbuha_aluno))
            if rbuha_aluno == rbuha_desejado:
                #          print("\t\tencontrado")
                return i
        #  print("\t*\t*Não encontrado.*\t*")
        return -1


if __name__ == "__main__":
    print("Iniciando testes.")

    repo = Repositorio()

    aluno = Aluno("t1", "uf1", "0", "01", None)
    aluno2 = Aluno("t2", "x", "1", "02", None)
    aluno3 = Aluno("editado", "editado", "editado", aluno.rbuha, None)

    testeNone = repo.obtem_aluno_por_rbuha(aluno)
    if not testeNone is None:
        print("Falha 1. Obtido aluno!", testeNone)

    print(repo.alunos)

    repo.inserir_aluno(aluno)
    testeAluno = (repo.obtem_aluno_por_rbuha(aluno), repo.obtem_aluno_por_rbuha(aluno2))

    if not ((testeAluno[0] == aluno) and (testeAluno[1] == None)):
        print("Falha 2. testeAluno != aluno")

    print(repo.alunos)

    print("\n Insere aluno 2 ")
    repo.inserir_aluno(aluno2)
    print(repo.alunos)
    print("\nRemove aluno2")
    repo.remover_aluno(aluno2)
    print(repo.alunos)

    print("\nEditar aluno1 para aluno3")
    repo.inserir_aluno(aluno2)
    print(repo.alunos)
    repo.editar_aluno(aluno, aluno3)
    testeEdita = repo.obtem_aluno_por_rbuha(aluno3.rbuha)
    print("Apos editar obtive o aluno: ", testeEdita)
    if not (testeEdita.nome == aluno3.nome):
        print("Falha 3. testeEdita não é uma edição de aluno.", testeEdita)

    print(repo.alunos)

    repo.remover_aluno(aluno2)
    testeAlunoRemovido = repo.obtem_aluno_por_rbuha(aluno2)
    if testeAlunoRemovido is not None:
        print("Falha 4. Obtido um aluno.")

    print(repo.alunos)

    print("Sucesso")
