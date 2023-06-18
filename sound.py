import pygame


def toca_som(arquivo):
    # aqui é opcional, eu coloquei só pra avisar que o resultado foi guardado
    # o pygame é responsável por fazer um som tocar
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    pygame.mixer.quit()
    # fim da musica
