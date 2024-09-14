import unittest
from unittest.mock import patch, mock_open
import main
import io


class TestMainFunction(unittest.TestCase):

    @patch('main.method.read_file', return_value='test content')
    @patch('main.method.preprocess_text', return_value={})
    @patch('main.method.simhash', return_value=0)
    @patch('main.method.hamming_distance', return_value=0)
    def test_main(self, mock_hamming_distance, mock_simhash, mock_preprocess_text, mock_read_file):
        with patch('builtins.open', mock_open()) as mocked_file:
            with patch('sys.argv', ['main.py', 'original.txt', 'plagiarized.txt', 'output.txt']):
                main.main()
                mocked_file.assert_called_once_with('output.txt', 'a', encoding='utf-8')
                mocked_file().write.assert_called_once_with('1.00\n')


if __name__ == '__main__':
    unittest.main()