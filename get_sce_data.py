#!/usr/bin/env python

import sys
import logging
from scedata import SCEData

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

data = [
    "SCE_Usage_8001026149_12-02-22_to_01-02-24.csv",
    "SCE_Usage_8001026149_09-03-23_to_10-03-24.csv",
]
scedata = SCEData(data).load().to_csv("energy.csv")
logger.info(scedata.data.describe())
