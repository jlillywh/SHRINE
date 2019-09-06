from unittest import TestCase
from data.file import File
import os


class TestFile(TestCase):
    def setUp(self):
        self.f1 = File('data.txt')
        self.test_file2_name = 'test_data2.txt'
    
    def tearDown(self):
        del self.f1
        
    def test_open_file(self):
        f2 = File(self.test_file2_name)
        try:
            f2.edit()
        except Exception:
            self.fail('File cannot be opened.')
        else:
            os.remove(self.test_file2_name)
            pass
        
    def test_invalid_ext(self):
        """ See if the program catches an invalid ext"""
        file_name = 'Word.rabbit'
        try:
            f4 = File(file_name)
        except Exception:
            pass
        else:
            self.fail('Expected not raised')
            
    
