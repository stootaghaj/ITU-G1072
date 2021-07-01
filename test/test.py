#!/usr/bin/env pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import G1072


class TestLibrary:
    def test_library(self):
        assert (
            G1072.test_para(
                bitrate=50,
                framerate=60,
                coding_res="1920x1080",
                packetloss=0.2,
                packetlossUDP=0,
                delay=0,
                Icomplexity="High",
                Vcomplexity="High",
            )
            == 4.140085244657
        )
