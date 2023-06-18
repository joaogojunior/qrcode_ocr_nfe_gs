import argparse
import json
import time

import nfe_utils
import qrcode_utils
import sound
import http_json
import csv_utils
import ocr_utils
import google_sheets_utils
import opcoes_utils

TEMPO_CONGELA_FRAME = opcoes_utils.le_opcao("TEMPO_CONGELA_FRAME")


def init():
    if __name__ == '__main__':
        ret = loop_principal()
    else:
        ret = -1
    return ret


def carrega_found(csv):
    set_carregado = set(map(lambda x: x.split(",", 1)[0], csv_utils.get_csv_como_lista(csv)))
    return set_carregado


def le_tecla_e_chama_rotina(vs, csv, frame):
    # se a tecla `q` foi pressionada, vai interromper o loop e fechar a janela
    key = qrcode_utils.le_tecla_cv2()
    # checa se ESC (27) para sair, "r" para relatorio, ou "enter" para ocr foram pressionados

    if key == 27:
        print("[INFO] Finalizando a stream...")
        qrcode_utils.finaliza_stream(vs)
        # fecha o arquivo CSV
        print("Fechando arquivo .csv")
        csv.close()
        return 1
    elif key == ord("r"):
        print("Mostrando relatorio das notas fiscais encontrados (debug):")
        nfs = csv_utils.cria_relatorio(csv)
        csv_utils.mostra_relatorio(nfs)
    elif key == 13:
        ocr_padrao = opcoes_utils.le_opcao("OCR_PADRAO")
        print("Enviando imagem para " + ocr_padrao)
        ocr_func = getattr(ocr_utils, "ocr_utils.detect_" + ocr_padrao)
        ocr_func(frame)
    elif key == ord("s"):
        pass

    return 0


def loop_principal():
    # pega valor de vid para abrir o videosource
    vid = int(opcoes_utils.le_opcao("VID_PADRAO"))
    print("[INFO] Iniciando o stream do dispositivo", vid)
    vs = qrcode_utils.abre_videosource(vid)

    # inicializa csv
    csv = csv_utils.abre_csv(opcoes_utils.le_opcao("CSV_SAIDA"))

    # inicializar o conjunto de códigos qrcode encontrados até agora
    found = carrega_found(csv)

    # inicializa variavel tempo qrcode encontrado, subtrai dois segundos para que nao influencie
    # na visualizacao nos primeiros quatro segundos
    tempo_qrcode_encontrado = time.time() - TEMPO_CONGELA_FRAME

    # pega um frame para inicializar variavel, porem este frame nao sera exibido
    frame_com_qrcodes = qrcode_utils.read_frame_e_qrcodes_from_videosource(vs)[0]

    #inicia google-sheets client
    sheet = google_sheets_utils.open_sheet(google_sheets_utils.get_client())

    # loop sobre a stream
    while True:
        # le um frame e procura por qrcodes
        frame, barcodes = qrcode_utils.read_frame_e_qrcodes_from_videosource(vs)

        # loop sobre os códigos de barras detectados
        for barcode in barcodes:
            # salva momento que o qrcode eh encontrado
            tempo_qrcode_encontrado = time.time()
            barcode_data = qrcode_utils.get_barcodedata(barcode)
            # se o texto do qrcode não estiver em found, vai escrever
            # os dados no csv e atualizar a variavel found com qrcode encontrada
            novo_qrcode = barcode_data not in found
            # marca qrcode encontrado no frame
            qrcode_utils.marca_barcode_no_frame(frame, barcode, novo_qrcode)
            # salva frame com qrcodes marcados
            frame_com_qrcodes = frame
            # checa se o qrcode detectado ja foi detectado antes
            if novo_qrcode and nfe_utils.valida_nfe_link(barcode_data):
                sound.toca_som(opcoes_utils.le_opcao("SOM_NOVO_QRCODE"))
                json_out, json_dict = http_json.get_json_from_qrcode(barcode_data)
                csv_utils.escreve_csv(csv, barcode_data, json_out)

                # extrai nf_list
                nf_dict = nfe_utils.extrai_nfe_data_from_json_dict_return_nf_dict(json_dict)
                # print(nf_dict)
                lista = nfe_utils.formata_campos_lista_de_celulas(nf_dict)
                row = google_sheets_utils.next_available_row(sheet)
                google_sheets_utils.write_sheet(sheet, "A"+row, lista)

                # adicionar qrcode encontrado
                found.add(barcode_data)
            else:
                sound.toca_som(opcoes_utils.le_opcao("SOM_QRCODE_JA_DETECTADO"))

        # atualiza a visualizacao do Frame a não ser que um qrcode tenha sido detectado a menos de quatro
        # segundos
        if time.time() - tempo_qrcode_encontrado < TEMPO_CONGELA_FRAME:
            frame = frame_com_qrcodes
        qrcode_utils.mostra_frame(frame)

        # le tecla e chama rotinas se retornar 1 quebra o loop
        if le_tecla_e_chama_rotina(vs, csv, frame):
            break

    # sai sem erros (0)
    return 0


# inicia execucao e ao encerrar retorna codigo de erro
init()
