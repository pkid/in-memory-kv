from csv import reader
from io import StringIO
import unittest
from flask import Flask
from dotenv import load_dotenv
from unittest import mock
from app import app, sync_kvs_from_file, kv_store


load_dotenv()

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.new_kvs1 = [{"key": "123", "value": "a"}]
        self.new_kvs2 = [{"key": "123", "value": "b"}]
        self.new_kvs3 = [{"key": "456", "value": "c"}]
    
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_put_kv_should_create_new_kv_and_write_to_file(self, mock_open):
        response = self.app.put('/kvs', json=self.new_kvs3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"message":"PUT successful"}\n')

        expected_kvs_to_put = '456,c,false\n'
        handle = mock_open.return_value.__enter__.return_value
        handle.write.assert_called_once_with(expected_kvs_to_put)

        response = self.app.get('/kvs/456')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"456":"c"}\n')
        response = self.app.delete('/kvs', json=self.new_kvs3)


    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_update_kvs_should_update_new_kvs_and_write_to_file(self, mock_open):
        response = self.app.put('/kvs', json=self.new_kvs1)
        response = self.app.put('/kvs', json=self.new_kvs2)      
        self.assertEqual(response.status_code, 200)
        
        expected_kvs_to_put1 = '123,a,false\n'
        expected_kvs_to_put2 = '123,b,false\n'
        handle = mock_open.return_value.__enter__.return_value
        handle.write.assert_has_calls([
            mock.call(expected_kvs_to_put1),
            mock.call(expected_kvs_to_put2)
        ])

        response = self.app.get('/kvs/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"123":"b"}\n')
    
    def test_get_non_existing_key_should_return_http_404(self):
        response = self.app.get('/kvs/123')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, '{"error":"Key not found"}\n')
    
    def test_delete_non_existing_key_should_return_http_404(self):
        response = self.app.delete('/kvs', json=self.new_kvs1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, '{"error":"Key not found"}\n')

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_delete_kv_should_delete_kv_and_write_to_file(self, mock_open):
        self.app.put('/kvs', json=self.new_kvs1)
        response = self.app.delete('/kvs', json=self.new_kvs1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"message":"DELETE successful"}\n')
        
        expected_kvs_to_put = '123,a,false\n'
        expected_kvs_to_delete = '123,a,true\n'
        handle = mock_open.return_value.__enter__.return_value
        handle.write.assert_has_calls([
            mock.call(expected_kvs_to_put),
            mock.call(expected_kvs_to_delete)
        ])

        response = self.app.get('/kvs/123')
        self.assertEqual(response.status_code, 404)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_sync_kvs_from_file(self, mock_open):
        in_mem_csv = StringIO(
        "123,a,false\n"
        "123,b,false\n"
        "234,b,false\n"
        "234,b,true\n"
        )

        with mock.patch('csv.reader', mock.MagicMock(return_value=reader(in_mem_csv, delimiter=',', quotechar='|'))):
             sync_kvs_from_file()
        self.assertEqual(len(kv_store), 1)
        self.assertEqual(kv_store['123'], 'b')

if __name__ == '__main__':
    unittest.main()
