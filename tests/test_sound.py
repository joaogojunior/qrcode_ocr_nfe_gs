from unittest import TestCase
from unittest.mock import patch, MagicMock

import sound


class Test(TestCase):
    def test_has_toca_som(self):
        self.assertIsNotNone(sound.toca_som)

    def test_toca_som(self):
        # substitui funcao load de pygame em sound.py por mock
        with patch.object(sound.pygame.mixer.music, "load", MagicMock()) as mock_load:
            with patch.object(sound.pygame.mixer.music, "play", MagicMock()) as mock_play:
                sound.toca_som("teste")
        # Assert
        mock_load.assert_called_once_with("teste")
        mock_play.assert_called_once()
