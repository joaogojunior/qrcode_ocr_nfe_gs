import json

opcoes_file = open("./config/opcoes.json", "r")
opcoes_dict = json.load(opcoes_file)

print(opcoes_dict)


def le_opcao(chave):
    return opcoes_dict[chave]
