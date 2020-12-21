import unittest
from brdm.BaseRefData import BaseRefData
import os, shutil
from Library import Library

class TestNcbiData(unittest.TestCase):

    def setUp(self):
        self.fixture = Library('test_config.yaml')
        self.local_write_dir = '../out/test/'


    def tearDown(self):
        if os.path.exists(self.fixture.destination_dir):
            shutil.rmtree(self.fixture.destination_dir)
        pass


    def test_smth(self):
        self.assertTrue(True, "Supposed to be True")
