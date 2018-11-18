import sys


def append(folder):
    sys.path.append('\\{}'.format(folder))


append("testes")
append("view")
append("model")
