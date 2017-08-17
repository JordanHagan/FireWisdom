import unittest
import intake
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql

class TestIntake(unittest.TestCase):

    def setUp(self):
        self.con = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')

    def test_intake_can_save_to_the_database(self):
        worked = intake.save_to_db('/Users/jordanhelen/galvanize/capstone/FireWisdom/tests/Sample Intake.csv')
        df = pd.read_sql_table('sample_intake', self.con)
        self.assertEqual(len(df.index), 4)
        self.assertEqual(df.columns[7], 'year_2004')
        self.assertEqual(df.year_2003[0], 0)
        self.assertEqual(df.year_2012[3], 3310)
        self.assertEqual(df.vehicle_mileage[0], 0)

    def tearDown(self):
        sql.execute('DROP TABLE IF EXISTS sample_intake', self.con)

if __name__ == '__main__':
    unittest.main()
