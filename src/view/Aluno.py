from collections import namedtuple

Aluno = namedtuple('Aluno', ['nome', 'universidade', 'ra', 'rbuha', 'historico'])

# Histórico é uma lista de disciplinas:

Disciplina = namedtuple('Disciplina', ['nome', 'cod', 'carga_horaria', 'nota', 'conclusao'])

hist = []
histusp = []
for i in range(1000):
    hist.append(Disciplina("AED2 " + str(i), "CODAED", 30, "A", "3Q/2018"))
    histusp.append(Disciplina("USP" + str(i), "USP+{}".format(i), 10, 4, "10/2018"))

andre = Aluno("André Rodrigues Barbosa",
              "UFABC", "11001814", "12311001814", hist)

joao = Aluno("João Pedro", "USP", "115314", "133115314", histusp)


def insere_disciplina(aluno, nova_disciplina):
    aluno.historico.append(nova_disciplina)


def remove_disciplina(aluno, index_no_historico):
    del aluno.historico[index_no_historico]


def copia_aluno(aluno):
    historico_copiado = []
    historico_original = aluno.historico
    if historico_original is not None:
        historico_copiado = historico_original.copy()

    a = Aluno(aluno.nome, aluno.universidade, aluno.ra, aluno.rbuha, historico_copiado)
    return a
