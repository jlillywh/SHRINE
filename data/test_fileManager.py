from unittest import TestCase
from data.fileman import FileManager
import os


class TestFileManager(TestCase):
    def setUp(self):
        self.fm = FileManager('data_external')
        self.fm.add_file('apikey.txt')
        
    def tearDown(self):
        del self.fm
    
    def test_change_dir(self):
        self.fm.directory = 'geometry'
        new_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\' + 'geometry' + '\\'))
        self.assertEqual(self.fm.directory, new_directory)
        
    def test_file_does_not_exist(self):
        file_name = "data1.xlsx"
        nickname = 'd1'
        self.assertRaises(FileNotFoundError, self.fm.add_file, file_name, nickname)
        
    def test_add_file(self):
        file_name = 'data.xlsx'
        self.fm.add_file(file_name)
        path = os.path.join(self.fm.directory + file_name)
        self.assertEqual(path, self.fm.files[file_name])
    
    def test_get_file(self):
        file_name = 'apikey.txt'
        path = os.path.join(self.fm.directory + file_name)
        self.assertEqual(path, self.fm.files[file_name])
