import view.buha_gui
import model.Repositorio

print("Inicializando repositorio")
repositorio = model.Repositorio.Repositorio(False)

print("Inicializando Interface Gráfica")
janela = view.buha_gui.Buha_gui(repositorio)

print("Terminando aplicação.")
