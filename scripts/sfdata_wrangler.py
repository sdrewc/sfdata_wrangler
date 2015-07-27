__author__      = "Gregory D. Erhardt"
__copyright__   = "Copyright 2013 SFCTA"
__license__     = """
    This file is part of sfdata_wrangler.

    sfdata_wrangler is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    sfdata_wrangler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with sfdata_wrangler.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import datetime

sys.path.append('C:/CASA/Workspace/sfdata_wrangler/sfdata_wrangler')
from SFMuniDataHelper import SFMuniDataHelper
from GTFSHelper import GTFSHelper
from SFMuniDataAggregator import SFMuniDataAggregator
from TransitReporter import TransitReporter
from ClipperHelper import ClipperHelper


USAGE = r"""

 python sfdata_wrangler.py [stepsToRun]
   
 e.g.

 python sfdata_wrangler clean expand aggUnweighted aggWeighted cleanClipper
 
 Notes: - steps should choose from list of valid steps
        - file names should be edited directly in this script. 
 
"""

    
# VALID STEPS-- list of allowable steps to run
VALID_STEPS = [ 'clean', 
                'expand', 
                'aggregate', 
                'report', 
                'cleanClipper'
                ]    
                

# INPUT FILES--change as needed
ROUTE_EQUIV = "D:/Input/routeEquiv_20150626.csv"

RAW_STP_FILES =["D:/Input/SFMTA Data/Raw STP Files/0803.stp",
                "D:/Input/SFMTA Data/Raw STP Files/0906.stp",
                "D:/Input/SFMTA Data/Raw STP Files/0912.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1001.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1005.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1009.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1101.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1110.stp",    
                "D:/Input/SFMTA Data/Raw STP Files/1201.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1203.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1206.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1209.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1212.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1303.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1304.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1306.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1308.stp",
                "D:/Input/SFMTA Data/Raw STP Files/1310.stp"
                ]
    
# these should be ordered from old to new, and avoid gaps or overlaps
RAW_GTFS_FILES = [
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20090402_0310_1.zip",  # 20090221 to 20090612 (originally 20090626)
                                                                                           # above file modified to avoid overlap of 13 days
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20091106_0310_1.zip",  # 20090613 to 20091204   (removed trailing sapced from file)
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20100415_0222.zip",  # 20091205 to 20100507
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20100812_0223_1.zip",  # 20100508 to 20100903
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20100908_0243_1.zip",  # 20100904 to 20110102 (originally 20101231)
                                                                                           # above file modified to avoid gap of 2 days
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20110104_0839.zip",  # 20110103 to 20110121
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20110420_0243_1.zip",  # 20110122 to 20110612 (originally 20110610)
                                                                                           # above file modified to avoid gap of 2 days
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20110910_0449.zip",  # 20110613 to 20111014
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20111210_0410.zip",  # 20111015 to 20120120
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20120319_0337_1.zip",  # 20120121 to 20120608 (originally 20120615)
                                                                                           # above file modified to avoid overlap of 6 days
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20120908_0325.zip",  # 20120609 to 20120928
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20130302_0432_1.zip",  # 20120929 to 20130329 (originally 20130322)
                                                                                           # above file modified to avoid gap of 8 days
  #"D:/Input/GTFS/san-francisco-municipal-transportation-agency_20130612_0307.zip",  # 20130330 to 20130628
  "D:/Input/GTFS/san-francisco-municipal-transportation-agency_20130910_2349.zip",  # 20130629 to 20131025
  "D:/Input/GTFS/san-francisco-municipal-transportation-agency_20140117_0111.zip"   # 20131026 to 20140131  
  ]


RAW_CLIPPER_FILES =[#"D:/Input/Clipper/2013_-_3_Anonymous_Clipper.csv",
                    "D:/Input/Clipper/2013_-_5_Anonymous_Clipper.csv",
                    "D:/Input/Clipper/2013_-_6_Anonymous_Clipper.csv",
                   # "D:/Input/Clipper/2013_-_7_Anonymous_Clipper.csv"
                   ]

# OUTPUT FILES--change as needed
CLEANED_OUTFILE       = "D:/Output/sfmuni_cleaned.h5"    

EXPANDED_TRIP_OUTFILE = "D:/Output/sfmuni_expanded_trip_YYYY.h5"    
EXPANDED_TS_OUTFILE   = "D:/Output/sfmuni_expanded_ts_YYYY.h5" 

DAILY_TRIP_OUTFILE = "D:/Output/sfmuni_daily_trip.h5"
DAILY_TS_OUTFILE   = "D:/Output/sfmuni_daily_ts.h5"

MONTHLY_TRIP_OUTFILE = "C:/CASA/DataExploration/sfmuni_monthly_trip.h5"
MONTHLY_TS_OUTFILE   = "C:/CASA/DataExploration/sfmuni_monthly_ts.h5"

REPORT_DAY_XLSFILE = "C:/CASA/DataExploration/PerfReport_SystemDay.xlsx"
REPORT_AM_XLSFILE = "C:/CASA/DataExploration/PerfReport_SystemAMPeak.xlsx"
REPORT_PM_XLSFILE = "C:/CASA/DataExploration/PerfReport_SystemPMPeak.xlsx"

CLIPPER_OUTFILE = "D:/Output/clipper.h5"


# main function call

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print USAGE
        print 'Valid steps include: ', VALID_STEPS
        sys.exit(2)

    STEPS_TO_RUN = sys.argv[1:]
    for step in STEPS_TO_RUN: 
        if not (step in VALID_STEPS): 
            print step, ' is not a valid step to run'
            print 'Valid steps include: ', VALID_STEPS
            sys.exit(2)

    # convert the AVL/APC data
    if 'clean' in STEPS_TO_RUN: 
        startTime = datetime.datetime.now()  
        sfmuniHelper = SFMuniDataHelper()
        sfmuniHelper.readRouteEquiv(ROUTE_EQUIV) 
        for infile in RAW_STP_FILES: 
            sfmuniHelper.processRawData(infile, CLEANED_OUTFILE)
        print 'Finished cleaning SFMuni data in ', (datetime.datetime.now() - startTime)

    # process GTFS data, and join AVL/APC data to it, also aggregate trip_stops to trips
    if 'expand' in STEPS_TO_RUN: 
        startTime = datetime.datetime.now()   
        gtfsHelper = GTFSHelper(sfmuni_file=CLEANED_OUTFILE, 
                                trip_outfile=EXPANDED_TRIP_OUTFILE, 
                                ts_outfile=EXPANDED_TS_OUTFILE, 
                                daily_trip_outfile=DAILY_TRIP_OUTFILE, 
                                daily_ts_outfile=DAILY_TS_OUTFILE, 
                                dow=[1], 
                                startDate='2013-10-09')
        for infile in RAW_GTFS_FILES: 
            gtfsHelper.expandAndWeight(infile)   
        print 'Finished expanding to GTFS in ', (datetime.datetime.now() - startTime)

    # aggregate to monthly totals
    if 'aggregate' in STEPS_TO_RUN: 
        startTime = datetime.datetime.now()   
        aggregator = SFMuniDataAggregator()
        aggregator.aggregateTripsToMonths(DAILY_TRIP_OUTFILE, MONTHLY_TRIP_OUTFILE)
        aggregator.aggregateTripStopsToMonths(DAILY_TS_OUTFILE, MONTHLY_TS_OUTFILE)
        print 'Finished aggregations in ', (datetime.datetime.now() - startTime) 

    # create performance reports
    if 'report' in STEPS_TO_RUN: 
        startTime = datetime.datetime.now()   
        reporter = TransitReporter(trip_file=MONTHLY_TRIP_OUTFILE, ts_file=MONTHLY_TS_OUTFILE)
        reporter.writeSystemReport(REPORT_DAY_XLSFILE, dow=1, tod='Daily')
        reporter.writeSystemReport(REPORT_AM_XLSFILE, dow=1, tod='0600-0859')
        reporter.writeSystemReport(REPORT_PM_XLSFILE, dow=1, tod='1600-1859')
        print 'Finished performance reports in ', (datetime.datetime.now() - startTime) 


    # process Clipper data.  
    if 'cleanClipper' in STEPS_TO_RUN: 
        startTime = datetime.datetime.now()   
        clipperHelper = ClipperHelper()
        for infile in RAW_CLIPPER_FILES: 
            clipperHelper.processRawData(infile, CLIPPER_OUTFILE)   
        print 'Finished processing Clipper data ', (datetime.datetime.now() - startTime) 
        
        
    print 'Run complete!  Time for a pint!'
    
    