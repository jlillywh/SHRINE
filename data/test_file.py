from unittest import TestCase
from data.file import File


class TestFile(TestCase):
    def setUp(self):
        self.f1 = File('data.xlsx', "C:\\Users\\jlillywhite\\Goldsim Technology Group LLC\\Model Library - Documents\\Applications\\Hydrology and Water Management\\Runoff and Routing\\Sacramento\\SACSMA Fortran\\")
        self.f2 = File('data.csv', 'C:\\')
        self.f3 = File('data.xls', 'C:\\')
    
    def tearDown(self):
        del self.f1, self.f2, self.f3
        
    def test_invalid_ext(self):
        """ See if the program catches an invalid ext"""
        file_name = 'Word.doc'
        try:
            self.f1.name = file_name
        except Exception:
            pass
        else:
            self.fail('Expected Exception not raised')
            
    
