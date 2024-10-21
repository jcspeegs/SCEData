# SCEData
Parse energy usage data extracted from [Southern California Edison](https://www.sce.com/).
SCEData will parse multiple files and dedup any overlapping data along the way
resulting in a tidy dataset ready for further analysis.

## HowTo
1. `git clone https://github.com/jcspeegs/SCEData.git`
1. Login to your SCE account at https://www.sce.com
1. Download your energy usage from https://www.sce.com/sma/ESCAA/EscGreenButtonData
    1. Select your account, start date, end date, and _.csv_ format
    1. Complete the CAPTCHA
    1. Click _Download_
1. ```python
   from scedata import SCEData

   # List of paths to usage data
   data = [
       "SCE_Usage_8001026149_12-02-22_to_01-02-24.csv",
       "SCE_Usage_8001026149_09-03-23_to_10-03-24.csv",
   ]

   # Output file
   fl = "energy.csv"
   
   # Convert energy usage data to a usable csv file
   scedata = SCEData(data).load().to_csv(fl)
   ```
