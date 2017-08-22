import unittest
import intake
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql

class TestIntake(unittest.TestCase):

    def setUp(self):
        self.con = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')

    def test_float_intake_can_save_to_the_database(self):
        worked = intake.save_to_db('/Users/jordanhelen/galvanize/capstone/FireWisdom/tests/Sample Float Intake.csv')
        df = pd.read_sql_table('sample_float_intake', self.con)
        self.assertEqual(len(df.index), 4)
        self.assertEqual(df.columns[7], 'year_2004')
        self.assertEqual(df.year_2003[0], 0)
        self.assertEqual(df.year_2012[3], 3310)
        self.assertEqual(df.lifetime_investment[3], 18775)

    def test_int_intake_can_save_to_the_database(self):
        worked = intake.save_to_db('/Users/jordanhelen/galvanize/capstone/FireWisdom/tests/Sample Int Intake.csv')
        df = pd.read_sql_table('sample_int_intake', self.con)
        self.assertEqual(df.approvalyear[0], 2010)
        self.assertEqual(df.residentcount[1], 266)

    def tearDown(self):
        sql.execute('DROP TABLE IF EXISTS sample_float_intake', self.con)
        sql.execute('DROP TABLE IF EXISTS sample_int_intake', self.con)

if __name__ == '__main__':
    unittest.main()
