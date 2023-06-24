import unittest
from flask import Flask
from app import app

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_put_kv_should_create_new_kv(self):
        response = self.app.put('/kv-store?key=123&value=a')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"message":"Key 123 updated with value a"}\n')

        response = self.app.get('/kv-store?key=123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"123":"a"}\n')

    def test_update_kv_should_update_new_kv(self):
        response = self.app.put('/kv-store?key=123&value=a')
        response = self.app.put('/kv-store?key=123&value=b')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"message":"Key 123 updated with value b"}\n')

        response = self.app.get('/kv-store?key=123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '{"123":"b"}\n')
    
    def test_get_non_existing_key_should_return_http_404(self):
        response = self.app.get('/kv-store?key=123')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, '{"error":"Key not found"}\n')
    
    def test_delete_non_existing_key_should_return_http_404(self):
        response = self.app.delete('/kv-store?key=123')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, '{"error":"Key not found"}\n')

    def test_delete_kv_should_delete_kv(self):
        self.app.put('/kv-store?key=123&value=a')
        response = self.app.delete('/kv-store?key=123')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, '{"error":"Key 123 with value a was deleted"}\n')
        response = self.app.get('/kv-store?key=123')
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
