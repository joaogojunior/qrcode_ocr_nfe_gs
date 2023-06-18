from unittest import TestCase

import nfe_utils


class Test(TestCase):
    def test_has_extrai_nfe_data_from_json_dict_return_nf_dict(self):
        # testa que o objeto é uma função
        self.assertEqual(type(nfe_utils.extrai_nfe_data_from_json_dict_return_nf_dict), type(lambda x: x))

    def test_extrai_nfe_data_from_json_dict_return_nf_dict(self):
        dict_json_line = {"nfeProc": {"proc": {"nfeProc": {"NFe": {"infNFe": {"ide":
                                                                              {"dhEmi": "2023-03-03T12:00:00-03:00"},
                                                                              "emit": {"CNPJ": "00000000000000",
                                                                                       "xNome":
                                                                                           "fornecedor teste",
                                                                                       "xFant": "loja legal",
                                                                                       "enderEmit": {"xLgr":
                                                                                                     "Rua sei nao",
                                                                                                     "nro": "000",
                                                                                                     "xBairro":
                                                                                                         "logo ali",
                                                                                                     "xMun":
                                                                                                         "Recife",
                                                                                                     "UF": "PE",
                                                                                                     "CEP": "50000000"}
                                                                                       },
                                                                              "det": {"prod": {"xProd":
                                                                                               "Produto teste 1",
                                                                                               "uCom": "Un",
                                                                                               "qCom": "1.0",
                                                                                               "vProd": "99.99"}},
                                                                              "total": {"ICMSTot": {"vProd": "99.99",
                                                                                                    "vDesc": "0.00",
                                                                                                    "vNF": "99.99"}}
                                                                              }}}}}}
        nf_dict = nfe_utils.extrai_nfe_data_from_json_dict_return_nf_dict(dict_json_line)
        self.assertEqual(nf_dict, {'data_emit': '2023-03-03', 'fornecedor_bairro': 'logo ali', 'fornecedor_cep':
                                   '50000000', 'fornecedor_cnpj': '00000000000000', 'fornecedor_estado': 'PE',
                                   'fornecedor_fantasia': 'loja legal', 'fornecedor_logadouro': 'Rua sei nao',
                                   'fornecedor_municipio': 'Recife', 'fornecedor_nome': 'fornecedor teste',
                                   'fornecedor_numero': '000', 'hora_emit': '12:00:00', 'produtos':
                                       [{'nome_produto': 'Produto teste 1', 'qtd_produto': '1.0', 'total_produto':
                                           '99.99', 'un_produto': 'Un'}], 'valor_bruto': '99.99', 'valor_desconto':
                                       '0.00', 'valor_total': '99.99'})

    def test_has_valida_nfe_link(self):
        # testa que o objeto é uma função
        self.assertEqual(type(nfe_utils.valida_nfe_link), type(lambda x: x))

    def test_valida_nfe_link_ok(self):
        r = nfe_utils.valida_nfe_link("http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe")
        self.assertTrue(r)

    def test_valida_nfe_link_bad(self):
        r = nfe_utils.valida_nfe_link("http://teste")
        self.assertFalse(r)
