from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock

import qrcode_utils


class Test(TestCase):
    def test_has_abre_videosource(self):
        self.assertIsNotNone(qrcode_utils.abre_videosource)

    def test_has_default_id(self):
        vid = qrcode_utils.default_id
        self.assertEqual(vid, 0)

    def test_abre_videosource(self):
        with patch.object(qrcode_utils, "VideoStream", MagicMock()) as VS:
            with patch.object(qrcode_utils.time, "sleep", MagicMock()) as slp:
                st = MagicMock()
                st.return_value = "vs_teste"
                VS.return_value = Mock(start=st)
                vs = qrcode_utils.abre_videosource()
                VS.assert_called_once_with(src=0)
                slp.assert_called_once_with(2.0)
                st.assert_called_once_with()
                self.assertEqual(vs, "vs_teste")

    def test_read_frame_e_qrcodes_from_videosource(self):
        rd = MagicMock()
        res = MagicMock()
        dec = MagicMock()
        with patch.object(qrcode_utils, "imutils", Mock(resize=res)):
            with patch.object(qrcode_utils, "pyzbar", Mock(decode=dec)):
                rd.return_value = "frame_teste"
                res.return_value = "frame_resize"
                dec.return_value = ["http://teste|0|1"]
                vs = Mock(read=rd)
                saida = qrcode_utils.read_frame_e_qrcodes_from_videosource(vs)
                rd.assert_called_once_with()
                res.assert_called_once_with("frame_teste", width=400)
                dec.assert_called_once_with("frame_resize", symbols=[qrcode_utils.pyzbar.ZBarSymbol.QRCODE])
                self.assertEqual(saida, ("frame_resize", ["http://teste|0|1"]))

    def test_get_barcodedata(self):
        barcode = Mock(data="http://teste|0|1".encode("utf-8"))
        data = qrcode_utils.get_barcodedata(barcode)
        self.assertEqual(data, "http://teste|0|1")

    def test_marca_barcode_no_frame_verde(self):
        with patch.object(qrcode_utils.cv2, "rectangle", Mock()) as rect:
            with patch.object(qrcode_utils.cv2, "putText", Mock()) as putt:
                frame = "frame_teste"
                barcode = Mock(rect=(1, 2, 3, 4))
                qrcode_utils.marca_barcode_no_frame(frame, barcode, True)
                rect.assert_called_once_with("frame_teste", (1, 2), (4, 6), (0, 255, 0), 2)
                putt.assert_called_once_with("frame_teste", 'QRCODE ENCONTRADO', (1, -8),
                                             qrcode_utils.cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def test_marca_barcode_no_frame_vermelho(self):
        with patch.object(qrcode_utils.cv2, "rectangle", Mock()) as rect:
            with patch.object(qrcode_utils.cv2, "putText", Mock()) as putt:
                frame = "frame_teste"
                barcode = Mock(rect=(1, 2, 3, 4))
                qrcode_utils.marca_barcode_no_frame(frame, barcode, False)
                rect.assert_called_once_with("frame_teste", (1, 2), (4, 6), (255, 0, 0), 2)
                putt.assert_called_once_with("frame_teste", 'QRCODE JA CAPTURADO', (1, -8),
                                             qrcode_utils.cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    def test_has_titulo_janela(self):
        tit = qrcode_utils.titulo_janela
        self.assertEqual(tit, "Ajuste o QRCODE na janela ('ESC' p/ sair)")

    def test_mostra_frame(self):
        with patch.object(qrcode_utils.cv2, "imshow", Mock()) as ims:
            qrcode_utils.mostra_frame("teste")
            ims.assert_called_once_with("Ajuste o QRCODE na janela ('ESC' p/ sair)", "teste")

    def test_finaliza_stream(self):
        with patch.object(qrcode_utils.cv2, "destroyAllWindows", Mock()) as dest:
            st = MagicMock()
            vs = Mock(stop=st)
            qrcode_utils.finaliza_stream(vs)
            dest.assert_called_once_with()
            st.assert_called_once_with()

    def test_le_tecla_cv2(self):
        with patch.object(qrcode_utils.cv2, "waitKey", Mock()) as wk:
            wk.return_value = -1
            tecla = qrcode_utils.le_tecla_cv2()
            self.assertEqual(tecla, 255)
            wk.return_value = 256
            tecla = qrcode_utils.le_tecla_cv2()
            self.assertEqual(tecla, 0)
            wk.assert_called_with(1)
