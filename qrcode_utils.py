import time
from imutils.video import VideoStream
from pyzbar import pyzbar

import imutils
import cv2  # 4.5.4.60

#titulo da janela de visualização
import opcoes_utils

titulo_janela = "Ajuste o QRCODE na janela ('ESC' p/ sair)"
# id do video source (0 = webcam interna)


def abre_videosource(vid):
    # Iniciar a stream (iniciar a webcam)
    VS = VideoStream(src=vid)
    # vs = VideoStream(usePiCamera=True).start()
    vs = VS.start()
    # # permitir que o sensor da câmera aqueça
    time.sleep(2.0)
    return vs

def read_frame_e_qrcodes_from_videosource(vs):
    # pega o quadro do fluxo de vídeo encadeado e redimensione-o para
    # conter uma largura máxima de 400 pixels
    frame = vs.read()
    # encontrar os códigos de barras (qr code) no quadro e decodificar cada um
    return frame, pyzbar.decode(frame, symbols=[pyzbar.ZBarSymbol.QRCODE])


def get_barcodedata(barcode):
    # os dados do código de barras é um objeto de bytes por isso, se queremos desenhá-lo
    # na nossa imagem de saída, precisamos convertê-lo para uma string primeiro
    barcode_data = barcode.data.decode("utf-8")
    # barcodeType = barcode.type
    return barcode_data


def marca_barcode_no_frame(frame, barcode, encontrado, valido):
    if encontrado and valido:
        rgb = (0, 255, 0)
        texto = "QRCODE ENCONTRADO"
    elif encontrado and not valido:
        rgb = (0, 0, 255)
        texto = "QRCODE INVALIDO"
    else:
        rgb = (255, 0, 0)
        texto = "QRCODE JA CAPTURADO"
    # extrair o local da caixa delimitadora do código de barras e desenhar
    # a caixa delimitadora que envolve o código de barras na imagem
    desenha_retangulo_e_texto_no_frame(frame, (texto, rgb), barcode.rect)


def desenha_retangulo_e_texto_no_frame(frame, texto_tuple, vertices_list):
    texto, rgb = texto_tuple
    x, y, w, h = vertices_list
    cv2.rectangle(frame, (x, y), (x + w, y + h), rgb, 2)
    # escreve texto perto acima da caixa delimitadora
    if texto != "":
        cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, rgb, 2)


def mostra_frame(frame):
    resize = int(opcoes_utils.le_opcao("RESIZE_FRAMES"))
    if resize:
        frame = imutils.resize(frame, width=int(opcoes_utils.le_opcao("RESIZE_WIDTH")))
    cv2.imshow(titulo_janela, frame)


def finaliza_stream(vs):
    #fecha janela de previsualização
    cv2.destroyAllWindows()
    #finaliza stream do videosource
    vs.stop()


def le_tecla_cv2():
    #waitKey retorna -1 quando nenhuma tecla eh pressionada
    k = cv2.waitKey(1)
    #retorna os primeiros dois bytes (limita a resposta de 0 a 255)
    #e faz o -1 virar 255
    return k & 0xFF


def converte_frame_as_str(frame):
    return cv2.imencode('.png', frame)[1].tostring()
