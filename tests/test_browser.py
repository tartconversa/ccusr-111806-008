"""真实浏览器验证本地可控页面。"""
import threading
import unittest
from app.site import DATA,start_server
from app.browser import read_visible_entry

class BrowserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=start_server();cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.origin=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)
    def test_navigation(self):
        item=DATA['items'][0];entry=read_visible_entry(self.origin,item['id'])
        self.assertEqual(entry['name'],item['name']);self.assertIn('/detail.html?',entry['url'])
