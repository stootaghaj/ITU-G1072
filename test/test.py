#!/usr/bin/env pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import G1072


class TestLibrary:
    def test_library(self):
        MOS, all_results = G1072.test_para(
            bitrate=50,
            framerate=60,
            coding_res="1920x1080",
            packetloss=0.2,
            packetlossUDP=0,
            delay=0,
            Icomplexity="High",
            Vcomplexity="High",
        )

        assert MOS == 4.580889112437288

        assert all_results == {
            "overall_quality": 4.580889112437288,
            "interaction_quality_delay": 4.6229955301830845,
            "interaction_quality_packetloss": 4.64,
            "video_quality_based_on_refitted_g1071": 4.596755274928551,
            "video_unclearness": 4.607621778600887,
            "video_fragmentation": 4.471200161599724,
        }

