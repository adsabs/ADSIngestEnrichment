import json
import os
import unittest

from mock import Mock, patch

from adsenrich.references import ReferenceWriter


class TestRefwriter(unittest.TestCase):
    def setUp(self):
        self.inputdir = os.path.join(os.path.dirname(__file__), "data/input/")
        self.outputdir = os.path.join(os.path.dirname(__file__), "data/output/")

    def test_refwriter(self):
        filenames_dict = {
            "jats_iop_apj_923_1_47.json": {
                "refsource": "iop",
                "publisher": "IOP",
                "bibcode": "2021ApJ...923...47B",
            },
            "jats_aip_aipc_2470_040010.json": {
                "refsource": "aip",
                "publisher": "AIP",
                "bibcode": "2022AIPC.2470d0010S",
            },
            "jats_aip_amjph_90_286.json": {
                "refsource": "aip",
                "publisher": "AIP",
                "bibcode": "2022AmJPh..90d.286G",
            },
        }

        for f in filenames_dict.keys():
            test_infile = os.path.join(self.inputdir, f)

            with open(test_infile, "r") as fp:
                record = json.load(fp)

            # Mocking the publisher name and bibcode to avoid API calls in testing
            mock_publisher = Mock()
            mock_publisher.return_value = filenames_dict[f]["publisher"]

            mock_bibcode = Mock()
            mock_bibcode.return_value = filenames_dict[f]["bibcode"]
            with patch("adsenrich.utils.issn2info", mock_publisher):
                with patch("adsenrich.bibcodes.BibcodeGenerator.make_bibcode", mock_bibcode):
                    refs = ReferenceWriter(
                        data=record,
                        reference_directory=self.outputdir,
                        reference_source=filenames_dict[f]["refsource"],
                        url="http://devapi.adsabs.harvard.edu/v1/",
                    )
                    refs.output_file = refs._create_output_file_name()
                    refs.write_references_to_file()
