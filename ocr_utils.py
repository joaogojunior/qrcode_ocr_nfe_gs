import cv2
from numpy import array, float32
from datetime import date

import opcoes_utils
import qrcode_utils


def le_contador_mes(arquivo, mes_atual):
    try:
        contador_file = open(arquivo, "r")
        contador_content = contador_file.read().strip().split(", ")
        contador, mes_contador = int(contador_content[0]), int(contador_content[1])
        contador_file.close()
    except FileNotFoundError:
        contador = 0
        mes_contador = mes_atual
    return contador, mes_contador


def atualiza_contador(arquivo, contador, mes_atual):
    contador_file = open(arquivo, "w")
    contador_file.write(str(contador) + ", " + str(mes_atual) + "\n")
    contador_file.close()


def detect_text_gvision(frame):
    def call_ocr(contador, mes_atual):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image_bytes = qrcode_utils.converte_frame_as_str(gray_frame)

        """Detects text in the file."""
        from google.cloud import vision
        from google.oauth2 import service_account

        cred = service_account.Credentials.from_service_account_file(opcoes_utils.le_opcao("GV_CREDENCIAL"))
        client = vision.ImageAnnotatorClient(credentials=cred)

        image = vision.Image(content=image_bytes)

        response = client.text_detection(image=image)

        # atualiza contador
        contador += 1
        atualiza_contador(arquivo_contador, contador, mes_atual)

        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            print(f'\n"{text.description}"')

            vertices = ([f'({vertex.x},{vertex.y})'
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return texts

    arquivo_contador = opcoes_utils.le_opcao("GV_CONTADOR")
    mes_atual = date.today().strftime("%m")
    # tenta ler contador de execucoes

    contador, mes_contador = le_contador_mes(arquivo_contador, mes_atual)

    if contador < 1000 and mes_contador == mes_atual:
        return call_ocr(contador, mes_atual)
    elif mes_contador == mes_atual:
        # nao chama o ocr pra nao gerar custos e cobranca do google
        print("Excedeu cota de uso deste ocr... Por favor selecione outro como tesseract ou easy_ocr.")
        return None
    else:
        # reseta arquivo contador
        contador = 0
        # atualiza_contador(arquivo_contador, contador, mes_atual)
        return call_ocr(contador, mes_atual)


def detect_text_tesseract(frame):
    import pytesseract
    import os
    os.environ["TESSDATA_PREFIX"] = opcoes_utils.le_opcao("TES_PREFIX")
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = opcoes_utils.le_opcao("TES_PATH")
    print(pytesseract.get_tesseract_version())
    print(pytesseract.image_to_string(gray_frame))


def detect_text_keras_test(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # import matplotlib.pyplot as plt

    import keras_ocr

    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()

    # Get a set of three example images
    # images = [
    #     keras_ocr.tools.read(url) for url in [
    #         'https://upload.wikimedia.org/wikipedia/commons/b/bd/Army_Reserves_Recruitment_Banner_MOD_45156284.jpg',
    #         'https://upload.wikimedia.org/wikipedia/commons/e/e8/FseeG2QeLXo.jpg',
    #         'https://upload.wikimedia.org/wikipedia/commons/b/b4/EUBanana-500x112.jpg'
    #     ]
    # ]

    images = [
        keras_ocr.tools.read(gray_frame)
    ]

    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(images)

    print(prediction_groups)
    # # Plot the predictions
    # fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    # for ax, image, predictions in zip(axs, images, prediction_groups):
    #     keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)


def detect_text_easyocr(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print(gray_frame)
    # image_bytes = qrcode_utils.converte_frame_as_str(gray_frame)
    import easyocr
    reader = easyocr.Reader(['pt', 'en'], gpu=False)  # this needs to run only once to load the model into memory
    print(frame)
    print(type(frame))
    print(reader.readtext(gray_frame))


def le_lista_resultados_ocr_retorna_frame(lista, frame):
    lista = [[('vimber', array([[153., 79.],
                                [223., 79.],
                                [223., 103.],
                                [153., 103.]], dtype=float32)),
              ('cadena', array([[249., 79.],
                                [322., 79.],
                                [322., 104.],
                                [249., 104.]], dtype=float32)),
              ('to', array([[221., 80.],
                            [246., 80.],
                            [246., 102.],
                            [221., 102.]], dtype=float32)),
              ('rosas', array([[325., 81.],
                               [387., 81.],
                               [387., 106.],
                               [325., 106.]], dtype=float32)),
              ('junir', array([[390.10248, 80.567955],
                               [456.36188, 81.81814],
                               [455.88287, 107.20533],
                               [389.62347, 105.95515]], dtype=float32)),
              ('ds', array([[77., 82.],
                            [101., 82.],
                            [101., 98.],
                            [77., 98.]], dtype=float32)),
              ('511s85', array([[523., 89.],
                                [595., 89.],
                                [595., 112.],
                                [523., 112.]], dtype=float32)),
              ('sharlys', array([[180., 129.],
                                 [264., 129.],
                                 [264., 154.],
                                 [180., 154.]], dtype=float32)),
              ('genuino', array([[267.10403, 129.03139],
                                 [348.30984, 130.24342],
                                 [347.9379, 155.16325],
                                 [266.7321, 153.95122]], dtype=float32)),
              ('da', array([[351., 132.],
                            [377., 132.],
                            [377., 155.],
                            [351., 155.]], dtype=float32)),
              ('silva', array([[378.51224, 132.48721],
                               [431.87888, 131.15305],
                               [432.47348, 154.93817],
                               [379.10684, 156.27234]], dtype=float32)),
              ('oa', array([[79., 134.],
                            [102., 134.],
                            [102., 150.],
                            [79., 150.]], dtype=float32)),
              ('z13bll', array([[521., 136.],
                                [599., 136.],
                                [599., 159.],
                                [521., 159.]], dtype=float32)),
              ('wermissin', array([[166., 180.],
                                   [277., 180.],
                                   [277., 205.],
                                   [166., 205.]], dtype=float32)),
              ('leandro', array([[279., 180.],
                                 [362., 180.],
                                 [362., 205.],
                                 [279., 205.]], dtype=float32)),
              ('da', array([[365., 182.],
                            [391., 182.],
                            [391., 205.],
                            [365., 205.]], dtype=float32)),
              ('silva', array([[394., 181.99998],
                               [446., 181.99998],
                               [446., 204.99998],
                               [394., 204.99998]], dtype=float32)),
              ('2061225', array([[525., 183.],
                                 [597., 183.],
                                 [597., 206.],
                                 [525., 206.]], dtype=float32)),
              ('05', array([[80., 184.],
                            [102., 184.],
                            [102., 200.],
                            [80., 200.]], dtype=float32)),
              ('mateus', array([[194., 216.],
                                [267., 216.],
                                [267., 240.],
                                [194., 240.]], dtype=float32)),
              ('lpes', array([[269.99997, 216.],
                              [329.99997, 216.],
                              [329.99997, 240.],
                              [269.99997, 240.]], dtype=float32)),
              ('de', array([[333., 216.],
                            [358., 216.],
                            [358., 240.],
                            [333., 240.]], dtype=float32)),
              ('souza', array([[360., 216.],
                               [419., 216.],
                               [419., 240.],
                               [360., 240.]], dtype=float32)),
              ('207523', array([[523., 216.],
                                [599., 216.],
                                [599., 239.],
                                [523., 239.]], dtype=float32)),
              ('cs', array([[81., 219.],
                            [104., 219.],
                            [104., 236.],
                            [81., 236.]], dtype=float32)),
              ('2178667', array([[522.99994, 249.],
                                 [598.99994, 249.],
                                 [598.99994, 272.],
                                 [522.99994, 272.]], dtype=float32)),
              ('joao', array([[211., 251.],
                              [261., 251.],
                              [261., 275.],
                              [211., 275.]], dtype=float32)),
              ('vitor', array([[264.53714, 251.4866],
                               [318.8782, 250.12808],
                               [319.47348, 273.9382],
                               [265.13242, 275.29672]], dtype=float32)),
              ('da', array([[322., 251.],
                            [348., 251.],
                            [348., 274.],
                            [322., 274.]], dtype=float32)),
              ('silva', array([[351., 251.],
                               [401., 251.],
                               [401., 274.],
                               [351., 274.]], dtype=float32)),
              ('07', array([[84., 256.],
                            [104., 256.],
                            [104., 270.],
                            [84., 270.]], dtype=float32)),
              ('207865', array([[527., 296.],
                                [600., 296.],
                                [600., 320.],
                                [527., 320.]], dtype=float32)),
              ('nascimentd', array([[339., 299.],
                                    [452., 299.],
                                    [452., 323.],
                                    [339., 323.]], dtype=float32)),
              ('pereira', array([[230., 299.99997],
                                 [306., 299.99997],
                                 [306., 324.99997],
                                 [230., 324.99997]], dtype=float32)),
              ('do', array([[309., 300.],
                            [336., 300.],
                            [336., 324.],
                            [309., 324.]], dtype=float32)),
              ('thiago', array([[159.99997, 300.99997],
                                [227.99997, 300.99997],
                                [227.99997, 324.99997],
                                [159.99997, 324.99997]], dtype=float32)),
              ('08', array([[84., 306.],
                            [106., 306.],
                            [106., 321.],
                            [84., 321.]], dtype=float32)),
              ('z08u6sd', array([[524., 344.],
                                 [603., 344.],
                                 [603., 367.],
                                 [524., 367.]], dtype=float32)),
              ('matias', array([[356., 347.],
                                [422., 347.],
                                [422., 370.],
                                [356., 370.]], dtype=float32)),
              ('luiz', array([[314., 349.],
                              [353., 349.],
                              [353., 372.],
                              [314., 372.]], dtype=float32)),
              ('washington', array([[192., 350.],
                                    [312., 350.],
                                    [312., 374.],
                                    [192., 374.]], dtype=float32)),
              ('0g', array([[84., 355.],
                            [106., 355.],
                            [106., 370.],
                            [84., 370.]], dtype=float32)),
              ('2018851', array([[523.32855, 376.85574],
                                 [599.9434, 374.3019],
                                 [600.7059, 397.17648],
                                 [524.091, 399.73032]], dtype=float32)),
              ('silva', array([[366.17502, 378.69934],
                               [417.46878, 380.12415],
                               [416.87357, 401.55206],
                               [365.5798, 400.12726]], dtype=float32)),
              ('da', array([[339., 380.],
                            [364., 380.],
                            [364., 402.],
                            [339., 402.]], dtype=float32)),
              ('perelira', array([[261.09393, 383.78458],
                                  [335.62433, 379.8619],
                                  [336.86188, 403.3757],
                                  [262.33148, 407.29837]], dtype=float32)),
              ('daniel', array([[197., 383.],
                                [259., 383.],
                                [259., 406.],
                                [197., 406.]], dtype=float32)),
              ('10', array([[87., 388.],
                            [108., 388.],
                            [108., 403.],
                            [87., 403.]], dtype=float32))]]
    return lista
