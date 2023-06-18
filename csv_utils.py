import json

import nfe_utils


def abre_csv(filename):
    # abra o arquivo CSV de saída para leitura e escrita (append)
    return open(filename, "a+")


def escreve_csv(csv, barcode_data, json_out):
    print("Escrevendo o arquivo CSV...")
    output = "{}, ".format(barcode_data) + json_out + "\n"
    csv.write(output)
    csv.flush()


def get_csv_como_lista(csv):
    csv.seek(0)
    return csv.readlines()


def cria_relatorio(csv):
    nfs_list = list()
    for line in get_csv_como_lista(csv):
        # extrai json da linha atual para dict
        dict_json_line = json.loads(line.split(",", 1)[1])
        nfs_list.append(nfe_utils.extrai_nfe_data_from_json_dict_return_nf_dict(dict_json_line))
    return nfs_list


def mostra_relatorio(nfs_list):
    total = 0.0
    for n, nfe in enumerate(nfs_list):
        print("nota fiscal", n)
        print("----------------")
        print("emissão:", nfe["data_emit"], nfe["hora_emit"])
        print("fornecedor:", nfe["fornecedor_cnpj"], nfe["fornecedor_nome"], nfe["fornecedor_fantasia"])
        print("endereco:", nfe["fornecedor_logadouro"], nfe["fornecedor_numero"], nfe["fornecedor_bairro"],
              nfe["fornecedor_municipio"], nfe["fornecedor_cep"], nfe["fornecedor_estado"])
        for p, produto in enumerate(nfe["produtos"]):
            print("produto", p, produto["nome_produto"], produto["qtd_produto"], produto["un_produto"],
                  produto["total_produto"])
        print("valores bruto, desconto e liquido:", nfe["valor_bruto"], nfe["valor_desconto"], nfe["valor_total"])
        total += float(nfe["valor_total"])
    print("valor total", "%.2f" % total)
