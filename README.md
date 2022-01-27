# Jenkins Job parser

```
usage: jj.py [-h] [-t TIMEDELTA] [-l LOWID] [-i HIGHID] [-d DURATION] [-u USER]
             [-j JENKINSURL] [-b JENKINSJOB] [-q JENKINSQUERY] [-k JENKINSTOKEN]

Parse Jenkins job base on duration or date

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEDELTA, --timedelta TIMEDELTA
                        Get jobs from since this value to now
  -l LOWID, --lowid LOWID
                        Specify job id range, must have -i or --highid
  -i HIGHID, --highid HIGHID
                        Specify job id range, must have -l or --lowid
  -d DURATION, --duration DURATION
                        Specify job duration in milliseconds, default around 70,000ms
  -u USER, --user USER  Your name/token for querying jenkins
  -j JENKINSURL, --jenkinsurl JENKINSURL
                        Your jenkins url
  -b JENKINSJOB, --jenkinsjob JENKINSJOB
                        Your jenkins job name
  -q JENKINSQUERY, --jenkinsquery JENKINSQUERY
                        Your jenkins job query, default to all builds
  -k JENKINSTOKEN, --jenkinstoken JENKINSTOKEN
                        Your jenkins api token
```
