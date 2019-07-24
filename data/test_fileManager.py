from unittest import TestCase
from data.fileman import FileManager
import os


class TestFileManager(TestCase):
    def setUp(self):
        self.fm = FileManager('..\\data_external')
        self.fm.add_file('apikey.txt')
        
    def tearDown(self):
        del self.fm
    
    def test_change_dir(self):
        self.fm.directory = '..\\geometry'
        self.assertTrue(os.path.exists(self.fm.directory))
        
    def test_file_does_not_exist(self):
        file_name = "data1.xlsx"
        self.assertFalse(self.fm.add_file(file_name))
        
    def test_add_file(self):
        file_name = 'data.xlsx'
        self.fm.add_file(file_name)
        expected_path = '..\\data_external' + '\\' + file_name
        self.assertEqual(expected_path, self.fm.get_file(file_name))
    
    def test_get_file(self):
        file_name = 'apikey.txt'
        expected_path = '..\\data_external' + '\\' + file_name
        self.assertEqual(expected_path, self.fm.get_file(file_name))
        
    def test_invalid_path(self):
        """ See if the program catches an invalid path"""
        path = "C:\\Users\\jlillywhite\\GarbageCan\\"
        try:
            self.fm.directory = path
        except Exception:
            pass
        else:
            self.fail('Expected Exception not raised')
