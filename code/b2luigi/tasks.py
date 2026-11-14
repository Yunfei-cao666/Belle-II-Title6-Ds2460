# -*- coding: utf-8 -*-
"""
b2luigi task skeleton for the Ds1 -> Ds pi pi ntuple.

STATUS: skeleton. Import paths and batch_system depend on your b2luigi version.
"""

import luigi
import b2luigi
from b2luigi.contrib.basf2 import Basf2PathTask

# If your b2luigi is older, use:
# from b2luigi.basf2_helper import Basf2Task
# and adapt the class below.

from steering_ntuple import build_path


class Ds1NtupleTask(Basf2PathTask):
    """One input mdst/uDST file -> one ntuple pair."""

    batch_system = "kekcc"  # use "local" for a quick test
    result_dir = "results/ntuple"

    input_file = luigi.Parameter()
    identifier = luigi.Parameter(default="")

    def output(self):
        yield self.add_to_output("ntuple_Bc.root")
        yield self.add_to_output("ntuple_Bn.root")

    def create_path(self):
        return build_path(
            [self.input_file],
            output_bc=self.get_output_file_name("ntuple_Bc.root"),
            output_bn=self.get_output_file_name("ntuple_Bn.root"),
        )


if __name__ == "__main__":
    b2luigi.process(
        Ds1NtupleTask(input_file="/path/to/mdst_or_udst.root"),
        workers=10,
    )
