##################################################
#
# Python: BIメトリック自動収集ツール
# Version: Draft 1.0A
#
# Arguments:
#    1. WLS_HOST
#    2. WLS_PORT
#    3. WLS_USER
#    4. WLS_PASSWD
#    5. Metric Table(start, stop or restart)
#    6. Metric of Interest
#    7. No. of Loop
#
##################################################

# import
import sys
import os
from java.util import Date
from java.text import SimpleDateFormat
from java.lang.Thread import sleep

# check for no. of arguments
argLen = len(sys.argv)
if argLen -1 != 7:
   print "Error: got ", argLen -1, " args."
   print "Usage: wlst DMSMetric.py WLS_HOST WLS_PORT WKS_USER WLS_PASSWORD METRIC_TABLE METRIC NO_OF_LOOP"
   exit()

# set Arguments
WLS_HOST = sys.argv[1]
WLS_PORT = sys.argv[2]
WLS_USER = sys.argv[3]
WLS_PASSWD = sys.argv[4]
MET_TBL = sys.argv[5]
MET_IN = sys.argv[6]
LOOP_LEN = int(sys.argv[7])

# Connecting to WLS
print 'Connecting to ' + WLS_HOST + ':' + WLS_PORT + ' with userid ' + WLS_USER + ' ...'
connect(WLS_USER,WLS_PASSWD,WLS_HOST + ':' + WLS_PORT)

# DATE & TIME formatting
ST_TIME = str(SimpleDateFormat("yyyyMMdd_HHmmss").format(Date()))

# OUTPUT
output_file = ST_TIME + "_" + MET_IN + "_dmp.log"
file = open(output_file,'w')
print >>file, "Start Metric Dump of " + str(MET_TBL) + ": " + str(MET_IN) + " at " + str(SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(Date()))

# Connecting to BI Domain
counter = 0

while counter <= LOOP_LEN:
   results = displayMetricTables(MET_TBL)

   for table in results:
      name = table.get('Table')
      rows = table.get('Rows')
      rowCollection = rows.values()
      iter = rowCollection.iterator()

      while iter.hasNext():
         row = iter.next()
         rowType = row.getCompositeType()
         keys = rowType.keySet()
         keyIter = keys.iterator()

         while keyIter.hasNext():
            colname = keyIter.next()
            value = row.get(colname)

            if (colname == MET_IN):
               print >>file, str(SimpleDateFormat("yyyy/MM/dd HH:mm:ss:SSS").format(Date())) + "\t" + str(value)
               counter = counter + 1
               Thread.sleep(700)

file.close()
disconnect()

# exit
exit()
