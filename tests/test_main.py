from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock, mock_open

import main


class Test(TestCase):
    def test_has_monta_argumentos_de_comando(self):
        # testa que o objeto é uma função
        self.assertEqual(type(main.monta_argumentos_de_comando), type(lambda x: x))

    def test_monta_argumentos_de_comando(self):
        d = dict(output="resultado.csv", videosource_id=0)
        v = main.monta_argumentos_de_comando()
        self.assertEqual(v, d)

    def test_has_carrega_found(self):
        # testa que o objeto é uma função
        self.assertEqual(type(main.carrega_found), type(lambda x: x))

    def test_carrega_found_populado(self):
        sk = Mock()
        rdlns = Mock()
        rdlns.return_value = ["http://teste|0|1, {}"]
        csv = Mock(seek=sk, readlines=rdlns)
        s = {"http://teste|0|1"}
        found = main.carrega_found(csv)
        self.assertEqual(s, found)

    def test_carrega_found_vazio(self):
        sk = Mock()
        rdlns = Mock()
        rdlns.return_value = []
        csv = Mock(seek=sk, readlines=rdlns)
        s = set()
        found = main.carrega_found(csv)
        self.assertEqual(s, found)

    def test_has_init(self):
        # testa que o objeto é uma função
        self.assertEqual(type(main.init), type(lambda x: x))

    def test_init_retorna_menos_um(self):
        ret = main.init()
        self.assertEqual(ret, -1)

    def test_has_loop_principal(self):
        self.assertEqual(type(main.loop_principal), type(lambda x: x))

    def test_name_equals_main_chamando_init_inicia_loop_principal(self):
        # substitui funcao main em main.py por mock
        with patch.object(main, "loop_principal", MagicMock()) as lp:
            # altera valor na variavel __name__ para "__main__"
            with patch.object(main, "__name__", "__main__"):
                # executa init()
                main.init()
        # Assert
        lp.assert_called_once()

    def test_init_retorna_10(self):
        with patch.object(main, "__name__", "__main__"):
            with patch.object(main, "loop_principal", MagicMock()) as lp:
                lp.return_value = 10
                ret = main.init()
                self.assertEqual(ret, 10)

    def test_loop_principal_retorna_0_encontrou_qrcode_novo(self):
        # impede e monitora a abertura do videostream
        with patch.object(main.qrcode_utils, "VideoStream", MagicMock()) as VS:
            # impede sleep
            with patch.object(main.qrcode_utils.time, "sleep", MagicMock()):
                st = MagicMock()
                rd = MagicMock()
                st.return_value = Mock(read=rd)
                VS.return_value = Mock(start=st)
                res = MagicMock()
                dec = MagicMock()
                # monitora imutils
                with patch.object(main.qrcode_utils, "imutils", Mock(resize=res)):
                    # monitora pyzbar
                    with patch.object(main.qrcode_utils, "pyzbar", Mock(decode=dec)):
                        res.return_value = "frame_resize"
                        dec.return_value = [Mock(rect=(1, 2, 3, 4), data="http://teste|0|1".encode("utf-8"))]
                        # monitora open
                        with patch("builtins.open", mock_open()) as mock_file:
                            # monitora csv.readlines
                            sk = Mock()
                            rdlns = Mock()
                            rdlns.return_value = []
                            # monitora csv.write
                            wrt = Mock()
                            csv = Mock(write=wrt, seek=sk, readlines=rdlns)
                            mock_file.return_value = csv
                            # monitora cv2.rectangle
                            with patch.object(main.qrcode_utils.cv2, "rectangle", Mock()) as rect:
                                # monitora cv2.putText
                                with patch.object(main.qrcode_utils.cv2, "putText", Mock()) as putt:
                                    # monitora music.load de pygame
                                    with patch.object(main.sound.pygame.mixer.music, "load", MagicMock()) as mock_load:
                                        # monitora music.play de pygame
                                        with patch.object(main.sound.pygame.mixer.music, "play", MagicMock()) as \
                                                mock_play:
                                            # monitora PoolManager.request
                                            with patch.object(main.http_json.urllib3.PoolManager, "request",
                                                              MagicMock()) as mock_poolmanager:
                                                mock_poolmanager.return_value = Mock(status="200",
                                                                                     data="<test>testes</test>".encode(
                                                                                         "utf-8"))
                                                # monitora cv2.imshow
                                                with patch.object(main.qrcode_utils.cv2, "imshow", Mock()) as ims:
                                                    # monitora cv2.waitKey
                                                    with patch.object(main.qrcode_utils.cv2, "waitKey", MagicMock()) \
                                                            as wk:
                                                        wk.return_value = 27
                                                        # Executa loop_principal()
                                                        ret = main.loop_principal()
                                                        # testa videosource chamado com parametos certos
                                                        VS.assert_called_once_with(src=0)
                                                        # testa chamada a cv2.rectangle com parametos certos
                                                        rect.assert_called_once_with("frame_resize", (1, 2), (4, 6),
                                                                                     (0, 255, 0), 2)
                                                        # testa chamada a cv2.puttext com parametos certos
                                                        putt.assert_called_once_with("frame_resize",
                                                                                     'QRCODE ENCONTRADO', (1, -8),
                                                                                     main.qrcode_utils.cv2.
                                                                                     FONT_HERSHEY_SIMPLEX,
                                                                                     0.5,
                                                                                     (0, 255, 0), 2)
                                                        # testa chamada a pymixer.music.load com parameto certo
                                                        mock_load.assert_called_once_with("TADA.WAV")
                                                        # testa se o pymixer.music.play foi executado
                                                        mock_play.assert_called_once()
                                                        # testa se request get http foi realizado com parametos certos
                                                        mock_poolmanager.assert_called_once_with("GET", "http://teste")
                                                        # testa se o csv.write foi chamado com parametos corretos
                                                        wrt.assert_called_once_with(
                                                            'http://teste|0|1, {"test": "testes"}\n')
                                                        # testa se o cv2.imshow foi chamado com parametos certos
                                                        ims.assert_called_once_with(
                                                            "Ajuste o QRCODE na janela ('ESC' p/ sair)", "frame_resize")
                                                        self.assertEqual(ret, 0)

    def test_loop_principal_retorna_0_nao_encontrou_qrcode_movo(self):
        # impede e monitora a abertura do videostream
        with patch.object(main.qrcode_utils, "VideoStream", MagicMock()) as VS:
            # impede sleep
            with patch.object(main.qrcode_utils.time, "sleep", MagicMock()):
                st = MagicMock()
                rd = MagicMock()
                st.return_value = Mock(read=rd)
                VS.return_value = Mock(start=st)
                res = MagicMock()
                dec = MagicMock()
                # monitora imutils
                with patch.object(main.qrcode_utils, "imutils", Mock(resize=res)):
                    # monitora pyzbar
                    with patch.object(main.qrcode_utils, "pyzbar", Mock(decode=dec)):
                        res.return_value = "frame_resize"
                        dec.return_value = [Mock(rect=(1, 2, 3, 4), data="http://teste|0|1".encode("utf-8"))]
                        # monitora open
                        with patch("builtins.open", mock_open()) as mock_file:
                            # monitora csv.readlines
                            sk = Mock()
                            rdlns = Mock()
                            rdlns.return_value = ["http://teste|0|1"]
                            csv = Mock(seek=sk, readlines=rdlns)
                            mock_file.return_value = csv
                            # monitora cv2.rectangle
                            with patch.object(main.qrcode_utils.cv2, "rectangle", Mock()) as rect:
                                # monitora cv2.putText
                                with patch.object(main.qrcode_utils.cv2, "putText", Mock()) as putt:
                                    # monitora cv2.imshow
                                    # monitora music.load de pygame
                                    with patch.object(main.sound.pygame.mixer.music, "load", MagicMock()) as mock_load:
                                        # monitora music.play de pygame
                                        with patch.object(main.sound.pygame.mixer.music, "play", MagicMock()) as \
                                                mock_play:
                                            with patch.object(main.qrcode_utils.cv2, "imshow", Mock()) as ims:
                                                # monitora cv2.waitKey
                                                with patch.object(main.qrcode_utils.cv2, "waitKey", MagicMock()) as wk:
                                                    wk.return_value = 27
                                                    # Executa loop_principal()
                                                    ret = main.loop_principal()
                                                    # testa videosource chamado com parametos certos
                                                    VS.assert_called_once_with(src=0)
                                                    # testa chamada a cv2.rectangle com parametos certos
                                                    rect.assert_called_once_with("frame_resize", (1, 2), (4, 6),
                                                                                 (255, 0, 0), 2)
                                                    # testa chamada a cv2.puttext com parametos certos
                                                    putt.assert_called_once_with("frame_resize", 'QRCODE JA CAPTURADO', (1, -8),
                                                                                 main.qrcode_utils.cv2.
                                                                                 FONT_HERSHEY_SIMPLEX,
                                                                                 0.5,
                                                                                 (255, 0, 0), 2)
                                                    # testa chamada a pymixer.music.load com parameto certo
                                                    mock_load.assert_called_once_with("DING.WAV")
                                                    # testa se o pymixer.music.play foi executado
                                                    mock_play.assert_called_once()
                                                    # testa se o cv2.imshow foi chamado com parametos certos
                                                    ims.assert_called_once_with(
                                                        "Ajuste o QRCODE na janela ('ESC' p/ sair)", "frame_resize")
                                                    self.assertEqual(ret, 0)

    def test_loop_principal_retorna_0_nao_encontrou_nenhum_qrcode_e_found_vazio(self):
        # impede e monitora a abertura do videostream
        with patch.object(main.qrcode_utils, "VideoStream", MagicMock()) as VS:
            # impede sleep
            with patch.object(main.qrcode_utils.time, "sleep", MagicMock()):
                st = MagicMock()
                rd = MagicMock()
                st.return_value = Mock(read=rd)
                VS.return_value = Mock(start=st)
                res = MagicMock()
                dec = MagicMock()
                # monitora imutils
                with patch.object(main.qrcode_utils, "imutils", Mock(resize=res)):
                    # monitora pyzbar
                    with patch.object(main.qrcode_utils, "pyzbar", Mock(decode=dec)):
                        res.return_value = "frame_resize"
                        dec.return_value = []
                        # monitora open
                        with patch("builtins.open", mock_open()) as mock_file:
                            # monitora csv.readlines
                            sk = Mock()
                            rdlns = Mock()
                            rdlns.return_value = []
                            csv = Mock(seek=sk, readlines=rdlns)
                            mock_file.return_value = csv
                            # monitora cv2.imshow
                            with patch.object(main.qrcode_utils.cv2, "imshow", Mock()) as ims:
                                # monitora cv2.waitKey
                                with patch.object(main.qrcode_utils.cv2, "waitKey", MagicMock()) as wk:
                                    wk.return_value = 27
                                    # Executa loop_principal()
                                    ret = main.loop_principal()
                                    # testa videosource chamado com parametos certos
                                    VS.assert_called_once_with(src=0)
                                    # testa se o cv2.imshow foi chamado com parametos certos
                                    ims.assert_called_once_with(
                                        "Ajuste o QRCODE na janela ('ESC' p/ sair)", "frame_resize")
                                    self.assertEqual(ret, 0)

    def test_loop_principal_retorna_0_nao_encontrou_nenhum_qrcode_e_found_vazio_e_entra_em_cria_relatorio(self):
        # impede e monitora a abertura do videostream
        with patch.object(main.qrcode_utils, "VideoStream", MagicMock()) as VS:
            # impede sleep
            with patch.object(main.qrcode_utils.time, "sleep", MagicMock()):
                st = MagicMock()
                rd = MagicMock()
                st.return_value = Mock(read=rd)
                VS.return_value = Mock(start=st)
                res = MagicMock()
                dec = MagicMock()
                # monitora imutils
                with patch.object(main.qrcode_utils, "imutils", Mock(resize=res)):
                    # monitora pyzbar
                    with patch.object(main.qrcode_utils, "pyzbar", Mock(decode=dec)):
                        res.return_value = "frame_resize"
                        dec.return_value = []
                        # monitora open
                        with patch("builtins.open", mock_open()) as mock_file:
                            # monitora csv.readlines
                            sk = Mock()
                            rdlns = Mock()
                            rdlns.return_value = []
                            csv = Mock(seek=sk, readlines=rdlns)
                            mock_file.return_value = csv
                            # monitora cv2.imshow
                            with patch.object(main.qrcode_utils.cv2, "imshow", Mock()) as ims:
                                # monitora cv2.waitKey
                                with patch.object(main.qrcode_utils.cv2, "waitKey", MagicMock()) as wk:
                                    with patch.object(main.csv_utils, "cria_relatorio", MagicMock()) as cr:
                                        wk.side_effect = [ord("r"), 27]
                                        # Executa loop_principal()
                                        ret = main.loop_principal()
                                        # testa videosource chamado com parametos certos
                                        VS.assert_called_once_with(src=0)
                                        # testa se o cv2.imshow foi chamado com parametos certos
                                        ims.assert_called_with(
                                            "Ajuste o QRCODE na janela ('ESC' p/ sair)", "frame_resize")
                                        # testa se loop_principal retornou 0
                                        self.assertEqual(ret, 0)
                                        # testa se cria_relatorio foi chamado
                                        cr.assert_called_once_with(csv)
