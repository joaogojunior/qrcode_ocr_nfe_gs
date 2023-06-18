import json

opcoes_dict = json.loads("./config/opcoes.json")


def le_opcao(chave):
    return opcoes_dict["chave"]
