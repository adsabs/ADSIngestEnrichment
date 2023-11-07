import json
import os
import unittest

from adsenrich.references import ReferenceWriter


class TestRefwriter(unittest.TestCase):
    def setUp(self):
        self.inputdir = os.path.join(os.path.dirname(__file__), "data/input/")
        self.outputdir = os.path.join(os.path.dirname(__file__), "data/output/")

    def test_refwriter(self):
        filenames_dict = {
            "jats_iop_apj_923_1_47.json": "iop",
            "jats_aip_aipc_2470_040010.json": "aip",
            "jats_aip_amjph_90_286.json": "aip",
        }

        for f in filenames_dict.keys():
            test_infile = os.path.join(self.inputdir, f)

            with open(test_infile, "r") as fp:
                record = json.load(fp)
            refs = ReferenceWriter(
                data=record,
                reference_directory=self.outputdir,
                reference_source=filenames_dict[f],
                url="http://devapi.adsabs.harvard.edu/v1/",
            )
            refs.write_references_to_file()
