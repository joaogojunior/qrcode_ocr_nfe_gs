import opcoes_utils

def extrai_nfe_data_from_json_dict_return_nf_dict(dict_json_line):
    nf_dict = dict()
    nf_dict["fornecedor_cnpj"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"]
    nf_dict["fornecedor_nome"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"]
    nf_dict["fornecedor_fantasia"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["xFant"]
    nf_dict["fornecedor_logadouro"] = \
        dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xLgr"]
    nf_dict["fornecedor_numero"] = \
        dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["nro"]
    nf_dict["fornecedor_bairro"] = \
        dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xBairro"]
    nf_dict["fornecedor_municipio"] = \
        dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xMun"]
    nf_dict["fornecedor_estado"] = \
        dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["UF"]
    nf_dict["fornecedor_cep"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
        "CEP"]
    dh_emit = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["ide"]["dhEmi"]
    nf_dict["data_emit"], hr_emit = dh_emit.split("T", 1)
    nf_dict["hora_emit"] = hr_emit.split("-", 1)[0]
    produtos = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["det"]
    produtos_saida = list()
    nf_dict["produtos"] = produtos_saida
    if not isinstance(produtos, list):
        produtos = [produtos]
    for produto in produtos:
        produto_saida = dict()
        produto_saida["nome_produto"] = produto["prod"]["xProd"]
        produto_saida["qtd_produto"] = produto["prod"]["qCom"]
        produto_saida["un_produto"] = produto["prod"]["uCom"]
        produto_saida["total_produto"] = produto["prod"]["vProd"]
        produtos_saida.append(produto_saida)
    nf_dict["valor_total"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"][
        "vNF"]
    nf_dict["valor_bruto"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"][
        "vProd"]
    nf_dict["valor_desconto"] = dict_json_line["nfeProc"]["proc"]["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"][
        "vDesc"]
    return nf_dict


def valida_nfe_link(link):
    return opcoes_utils.le_opcao("NFE_BASE_URL") == link[:50]


def formata_campos_lista_de_celulas(nf_dict):
    lista = [['Nome Fornecedor', nf_dict["fornecedor_nome"] + " " + nf_dict["fornecedor_fantasia"], 'CNPJ',
              nf_dict["fornecedor_cnpj"], 'Data de emissão', nf_dict["data_emit"]],
             ['Endereço Fornecedor',
              nf_dict["fornecedor_logadouro"] + " " + nf_dict["fornecedor_numero"] + " " + nf_dict[
                  "fornecedor_bairro"] + " " +
              nf_dict["fornecedor_municipio"] + " " + nf_dict["fornecedor_estado"] + " " + nf_dict["fornecedor_cep"],
              'Total de produtos', str(len(nf_dict['produtos'])), 'Hora de emissão', nf_dict["hora_emit"]],
             ['Itens', 'Nome Produto', 'Quantidade', 'Unidade', 'Preço Unitario', 'Preço']]
    for n, produto in enumerate(nf_dict['produtos']):
        lista.append([n + 1, produto["nome_produto"], produto["qtd_produto"], produto["un_produto"],
                      str(float(produto["total_produto"]) / float(produto["qtd_produto"])), produto["total_produto"]])
    return lista
