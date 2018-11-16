from collections import namedtuple

Aluno = namedtuple ('Aluno', ['nome', 'universidade', 'ra','rbuha', 'historico'])

# Histórico é uma lista de disciplinas:

Disciplina = namedtuple('Disciplina', ['nome', 'cod', 'carga_horaria', 'nota', 'conclusao'])


hist = []
histusp = []
for i in range (1000):
    hist.append(Disciplina("AED2 "+str(i), "CODAED", 30, "A", "3Q/2018"))
    histusp.append(Disciplina("USP"+str(i), "USP+{}".format(i), 10, 4, "10/2018"))



andre = Aluno("André Rodrigues Barbosa",
                         "UFABC", "11001814", "12311001814", hist)

joao = Aluno("João Pedro", "USP", "115314", "133115314", histusp)