import urllib3
import xmltodict
import json


def get_url_from_code(code):
    # pega url do qrcode
    return code.split("|")[0]


def read_response_from_http_get_as_str(url):
    http = urllib3.PoolManager()
    # http get
    response = http.request("GET", url)
    # retorna a resposta como string
    return response.data.decode("utf-8")


def converte_xml_para_json_str(data):
    dict_xml = xmltodict.parse(data)
    # gera json do dicionario e retorna
    return json.dumps(dict_xml), dict_xml


def get_json_from_qrcode(code):
    # pega substring url de code
    url = get_url_from_code(code)
    try:
        # tenta obter xml da url
        xml_str = read_response_from_http_get_as_str(url)
        # converte dados da resposta em json
        return converte_xml_para_json_str(xml_str)
    except Exception as e:
        print("Sem conectividade com a internet...", e)
        print("devolvendo um json vazio...")
        return "{}", {}
