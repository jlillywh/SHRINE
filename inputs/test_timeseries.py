from unittest import TestCase
from inputs.time_series import TimeSeries
import datetime
from datetime import timedelta


# dir_path = '..\data_external'
# fileman = FileManager(dir_path)
#
# file_name = 'data.xlsx'
# fileman.add_file(file_name)
# fileman.add_file('timeseries_data1.csv')
#
# xls_file = pd.ExcelFile(fileman.file_list[file_name])
#
# # table = xls_file.parse(sheet_name='Monthly', name='monthly data').to_dict()
#
# df = pd.read_excel(xls_file, 'Monthly')
#
# xls_file.close()
# print(type(df['Evap']))
#
# v1 = Vector('Evaporation', 'in', df['Evap'])
#
# b = Bar('Evap')
# b.add_output(v1)
#
# ts1 = TimeSeries('Rainfall')
# ts1.load_csv(fileman.file_list['timeseries_data1.csv'])
# ts2 = ts1
#
# th1 = TimeHistoryChart('Rainfall')
# th1.add_result(ts1)
# th1.add_result(ts2)
#
# b.show()
# th1.show()


class TestTimeSeries(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.ts = TimeSeries('1/1/19', periods=365)
        self.dec_places = 3
    
    def tearDown(self):
        """Destroy the object after running tests"""
        del self.ts
    
    def test_num_of_records(self):
        nr = 365
        self.assertEqual(self.ts.num_of_records(), nr)

    def test_start_date(self):
        sd = datetime.date(2019, 1, 1)
        self.assertEqual(self.ts.start_date(), sd)
    
    def test_end_date(self):
        ed = datetime.date(2019, 12, 31)
        self.assertEqual(self.ts.end_date(), ed)
        
    def test_end_date(self):
        ed = datetime.date(2019, 12, 31)
        self.assertEqual(self.ts.end_date(), ed)
        
    def test_duration(self):
        dur = timedelta(days=365)
        self.assertEqual(self.ts.duration(), dur)