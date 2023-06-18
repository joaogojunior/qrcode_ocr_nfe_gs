from unittest import TestCase
from unittest.mock import patch, mock_open, Mock, MagicMock

import csv_utils


class Test(TestCase):
    def test_abre_csv(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.return_value = "teste"
            file_handle = csv_utils.abre_csv("teste.csv")
            mock_file.assert_called_with("teste.csv", "a+")
            self.assertEqual(file_handle, "teste")

    def test_escreve_csv(self):
        wrt = Mock()
        csv = Mock(write=wrt)
        csv_utils.escreve_csv(csv, "http://teste|0|1", "{}")
        wrt.assert_called_once_with("http://teste|0|1, {}\n")

    def test_get_csv_como_lista(self):
        sk = Mock()
        rdlns = Mock()
        rdlns.return_value = ["0", "1", "2"]
        csv = Mock(seek=sk, readlines=rdlns)
        ret = csv_utils.get_csv_como_lista(csv)
        sk.assert_called_once_with(0)
        self.assertEqual(ret, ["0", "1", "2"])

    def test_cria_relatorio_vazio(self):
        with patch.object(csv_utils, "get_csv_como_lista", MagicMock()) as getccl:
            getccl.return_value = []
            nfl = csv_utils.cria_relatorio("teste_file")
            self.assertEqual(nfl, [])

    def test_cria_relatorio_populado(self):
        with patch.object(csv_utils, "get_csv_como_lista", MagicMock()) as getccl:
            getccl.return_value = ['http://teste|0|1, {"nfeProc": {"proc": {"nfeProc": {"NFe": {"infNFe": {"ide": '
                                   '{"dhEmi": "2023-03-03T12:00:00-03:00"}, "emit": {"CNPJ": "00000000000000", "xNome":'
                                   ' "fornecedor teste", "xFant": "loja legal", "enderEmit": {"xLgr": '
                                   '"Rua sei nao", "nro": "000", "xBairro": "logo ali", "xMun":'
                                   ' "Recife", "UF": "PE", "CEP": "50000000"}}, "det": {"prod": {"xProd": '
                                   '"Produto teste 1", "uCom": "Un", "qCom": "1.0", "vProd": "99.99"}}, '
                                   '"total": {"ICMSTot": {"vProd": "99.99", "vDesc": "0.00", "vNF": "99.99"}}}}}}}}']
            nfl = csv_utils.cria_relatorio("teste_file")
            self.assertEqual(nfl, [{'data_emit': '2023-03-03', 'fornecedor_bairro': 'logo ali', 'fornecedor_cep':
                                    '50000000', 'fornecedor_cnpj': '00000000000000', 'fornecedor_estado': 'PE',
                                    'fornecedor_fantasia': 'loja legal', 'fornecedor_logadouro': 'Rua sei nao',
                                    'fornecedor_municipio': 'Recife', 'fornecedor_nome': 'fornecedor teste',
                                    'fornecedor_numero': '000', 'hora_emit': '12:00:00', 'produtos':
                                        [{'nome_produto': 'Produto teste 1', 'qtd_produto': '1.0', 'total_produto':
                                            '99.99', 'un_produto': 'Un'}], 'valor_bruto': '99.99', 'valor_desconto':
                                        '0.00', 'valor_total': '99.99'}])

    def test_has_mostra_relatorio(self):
        # testa que o objeto é uma função
        self.assertEqual(type(csv_utils.mostra_relatorio), type(lambda x: x))
