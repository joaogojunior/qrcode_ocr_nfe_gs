from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock

import http_json


class Test(TestCase):
    def test_has_get_json_from_qrcode(self):
        self.assertIsNotNone(http_json.get_json_from_qrcode)

    def test_has_get_url_from_code(self):
        self.assertIsNotNone(http_json.get_url_from_code)

    def test_get_url_from_code(self):
        code = "http://teste|teste|1|2|3"
        self.assertEqual(http_json.get_url_from_code(code), "http://teste")

    def test_has_read_response_from_http_get_as_str(self):
        self.assertIsNotNone(http_json.read_response_from_http_get_as_str)

    def test_read_response_from_http_get_as_str(self):
        with patch.object(http_json.urllib3.PoolManager, "request", MagicMock()) as mock_poolmanager:
            mock_poolmanager.return_value = Mock(status="200", data="teste".encode("utf-8"))
            data = http_json.read_response_from_http_get_as_str("http://teste")
        # Assert
        self.assertEqual(data, "teste")

    def test_has_converte_json_para_xml(self):
        self.assertIsNotNone(http_json.converte_xml_para_json)

    def test_converte_json_para_xml(self):
        data = "<test>testes</test>"
        ret = '{"test": "testes"}'
        self.assertEqual(http_json.converte_xml_para_json(data), ret)

    def test_get_json_from_qrcode_with_invalid_url(self):
        with patch.object(http_json.urllib3.PoolManager, "request", MagicMock()) as mock_poolmanager:
            mock_poolmanager.side_effect = Exception('Test')
            json_str = http_json.get_json_from_qrcode("http://teste|0|1")
        self.assertEqual(json_str, "{}")

    def test_get_json_from_qrcode_with_valid_url(self):
        with patch.object(http_json.urllib3.PoolManager, "request", MagicMock()) as mock_poolmanager:
            mock_poolmanager.return_value = Mock(status="200", data="<test>testes</test>".encode("utf-8"))
            json_str = http_json.get_json_from_qrcode("http://teste|0|1")
            ret = '{"test": "testes"}'
        self.assertEqual(json_str, ret)
