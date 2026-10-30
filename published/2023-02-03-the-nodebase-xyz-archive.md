![The nodebase.xyz Archive](/images/2023/02/Screenshot-at-2023-02-03-08-18-29.png)

[**nodebase.xyz**](https://web.archive.org/web/20221204054748/http://nodebase.xyz/) was my first blog I built from the ground up on [OpenBSD](https://www.openbsd.org/). It was comprised of HTML, CSS and a very small amount of JavaScript, along with some shell scripts in the back end. Ran on `httpd`, and included a hit counter/visit counter (the JS part).

![](/images/2023/02/puffy.png)

I built `nodebase.xyz` so that I could share some learnings about financial markets with the world.

I maintained this blog for about 2 years, and last published in April of 2021.

Here is an archive of my posts, as I wind it down now.

## Post Archive

**Call Options: A Short Story on How I Went Long**  
Published: April 13, 2021  
<https://web.archive.org/web/20220205034256/http://nodebase.xyz/call-option.html>

- first experience trading options, buying call options on the gold miners ETF, `$GDX`

**ETF Selection Guide: Liquidity and Legal Structure**  
Published: November 2, 2020  
<https://web.archive.org/web/20220218061931/http://nodebase.xyz/etf-selection.html>

- looking at counterparty risk and rehypothecation of stocks within ETFs and Unit Trusts

**Why You Should Open a Taxable Brokerage Account**  
Published: October 7, 2020  
<https://web.archive.org/web/20220218132844/http://nodebase.xyz/taxable-account.html>

- comparing tax implications of holding stocks and bonds in a non-retirement vs. a retirement account

**The Four Dimensions of Asset Analysis**  
Published: June 11, 2020 (Updated: August 6, 2020)  
<https://web.archive.org/web/20220205004855/http://nodebase.xyz/4d-asset-analysis.html>

- a framework for investing and building a portfolio taking into consideration Past Performance, Risk Profile, Fundamentals and Time (Preference

## Some technical learnings

- don't ban IP addresses forever (I built a custom set of scripts for this, see below)
- OpenBSD, become root: `doas su` (instead of `sudo su`)
- don't trust investing.com to continue to serve your screenshots of charts forever

## Breadcrumbs and Scripts

block an IP address using Packet Filter, `pfctl`; `blockip.sh` script:

```
#!/bin/sh
# BLOCK SPECIFIED IP ADDRESS (first command line argument)
export IP_TO_BLOCK="$1"
pfctl -t blockedips -T add $IP_TO_BLOCK ; 			# ADD TO BLACKLIST ON THE FLY
echo $IP_TO_BLOCK >> /etc/pf.blocked.ip.conf ;
echo "Added $IP_TO_BLOCK to /etc/pf.blocked.ip.conf.\n" ;
# TO MANUALLY UNBLOCK AN IP ADDRESS, RUN:
# pfctl -t blockedips -T delete <$IP_TO_UNBLOCK>
# SHOW ALL BLOCKED IPs:
export ALL_BLOCKED_IPS="$(pfctl -t blockedips -T show)"
echo "List of all blocked IPs:\n" + $ALL_BLOCKED_IPS ;
echo "\nEND\n"
```

**different ways to list IPs of standard/non-standard visitors/hits/scanning attempts:**

`unique-ips.sh`

```
#!/bin/sh
awk '{ print $2 }' /var/www/logs/access.log* | grep -v openbsd | sort -n | uniq -c | sort -nr | awk '{ print $2 }'
```

`newodd2.sh`:

```
#!/bin/sh
cat /var/www/logs/access.log | grep -v "GET / HTTP" | grep -v "GET /robots.txt " | grep -v "POST / HTTP" \
	| grep -v "HEAD / HTTP" | grep -v "<UNKNOWN> " | grep -v "GET /puffy.png" | grep -v "GET /favicon.ico" \
	| grep -v openbsd | grep -v -f /etc/pf.blocked.ip.conf | grep -v "GET /images" | grep -v "4d-asset" \
	| grep -v "GET /cgi-bin/views-4daa.js" | grep -v "GET /cgi-bin/ip-count.js" | grep -v "GET /cgi-bin/hits-all.js" \
	| grep -v "GET /cgi-bin/hits-4daa.js" | grep -v "GET /cgi-bin/ip-count.txt" | grep -v "GET /cgi-bin/views-4daa.txt" \
	| awk {' print $2, $5, $6, $7, $8, $9, $10, $11 '} | sed 's/ \+0000//g'
```

`newodd.sh`

```
#!/bin/sh
cat /var/www/logs/access.log | grep -v "GET / HTTP" | grep -v "GET /robots.txt " | grep -v "POST / HTTP" \
	| grep -v "HEAD / HTTP" | grep -v "<UNKNOWN> " | grep -v "GET /puffy.png" | grep -v "GET /favicon.ico" \
	| grep -v openbsd | awk {' print $2, $5, $6, $7, $8, $9, $10, $11 '} | sed 's/ \+0000//g' \
```

`odd.sh`

```
#!/bin/sh
cat /var/www/logs/access.log* | grep -v "GET / HTTP" | grep -v "GET /robots.txt " | grep -v "POST / HTTP" \
	| grep -v "HEAD / HTTP" | grep -v "<UNKNOWN> " | grep -v "GET /puffy.png" | grep -v "GET /favicon.ico" \
	| grep -v openbsd | awk {' print $2, $5, $6, $7, $8, $9, $10, $11 '} | sed 's/ \+0000//g' \
```

`odd-unique.sh`

```
#!/bin/sh
cat /var/www/logs/access.log* | grep -v "GET / HTTP" | grep -v "GET /robots.txt " | grep -v "POST / HTTP" \
	| grep -v "HEAD / HTTP" | grep -v "<UNKNOWN> " | grep -v "GET /puffy.png" | grep -v "GET /favicon.ico" \
	| grep -v openbsd | awk {' print $7, $8, $9, $10, $11 '} | uniq -c | sort -nr | uniq -u
```

examples of "odd" requests:

```
   6 "GET /YesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScanningForResearchPurposePleaseHaveALookAtTheUserAgentTHXYesThisIsAReallyLongRequestURLbutWeAreDoingItOnPurposeWeAreScann HTTP/1.1" 301 0
   3 "GET /wp-admin HTTP/1.1" 404 0
   3 "GET /adv,/cgi-bin/weblogin.cgi?username=admin%27%3Bls%20%23&password=asdf HTTP/1.1" 301 0
   3 "GET /.well-known/acme-challenge/pmyV-XSEoLfdxCuA6auw_sXXSV6ABojS_mr1iVuk8j8 HTTP/1.1" 200 87
   2 "POST /xx.php HTTP/1.1" 301 0
   2 "POST /cgi-bin/mainfunction.cgi HTTP/1.1" 301 0
   2 "GET /rss/ HTTP/1.1" 301 0
   2 "GET /pmd/ HTTP/1.1" 301 0
   2 "GET /pma/ HTTP/1.1" 301 0
   2 "GET /phpmyadmin4.8.5/ HTTP/1.1" 301 0
```

`refresh_pf_blacklist.sh`

```
#!/bin/sh
pfctl -nf /etc/pf.conf ;
pfctl -f /etc/pf.conf ;
echo "\nblacklist refreshed. list of all blacklisted ips:\n" ;
pfctl -t blockedips -T show
```

show blacklisted IPs: `pfctl -t blockedips -T show`

`robots.txt`

```
User-agent: * 
Disallow: /cgi-bin/
```

**Building the Hit Counters:**

`hits-all.sh`:

```
#!/bin/sh
# filter out ip addresses that have been banned:
# grep -v -f /etc/pf.blocked.ip.conf
UNIQUE="$(cat /var/www/logs/access.log* | grep "nodebase" | grep -v -f /etc/pf.blocked.ip.conf | awk '{ print $2 }' | sort -n | uniq | wc -l | tr -d " ")"
HITS="$(cat /var/www/logs/access.log* | grep "GET / " | grep -v -f /etc/pf.blocked.ip.conf | awk '{ print $2 }' | sort -n | wc -l | tr -d " ")"
echo "document.writeln (\"unique visitors by ip address: $UNIQUE | total hits: $HITS\")"
```

`lastcount.sh`:

```
#!/bin/sh
COUNT="$(cat /var/www/logs/access.log* | grep nodebase | awk '{ print $2 }' | sort -n | uniq | wc -l | tr -d " ")"
echo "document.writeln (\"unique visitors by ip address: $COUNT\")"
```

cron jobs:

```
### LOGGING IP ADDRESSES AND VISITORS

# log all IPs from /var/www/logs/access.log* including archives, every Sunday at 11:00 PM
0	23	*	*	sun	/var/www/htdocs/ARCHIVE/uniqueIPs.sh > /var/www/htdocs/ARCHIVE/ip-log-archives/ip-log-$(date "+%y%m%d%_%H%M%S").txt
# log total count of all unique IPs from /var/www/logs/access.log* including archives, every Sunday at 11:01 PM
1	23	*	*	sun	/var/www/htdocs/ARCHIVE/lastcount.sh > /var/www/htdocs/ARCHIVE/ip-log-archives/last-count-$(date "+%y%m%d%_%H%M%S").js
# log total count of all unique IPs from access.log* that visited '4d-asset-analysis.html', every Sunday at 11:02 PM
2	23	*	*	sun	/var/www/htdocs/ARCHIVE/views-4daa.sh > /var/www/htdocs/ARCHIVE/ip-log-archives/views-4daa-$(date "+%y%m%d%_%H%M%S").js
# log all unique IPs every five minutes using access.log* files, including archives
*/5 * * * * /var/www/htdocs/ARCHIVE/uniqueIPs.sh > /var/www/htdocs/ARCHIVE/ip-log.txt

### COUNTING TOTAL VISITORS & UNIQUE IP ADDRESSES

# refresh total count of all unique IPs logged once a minute using access.log* files, including archives
* * * * * /var/www/htdocs/nodebase.xyz/cgi-bin/hits-all.sh > /var/www/htdocs/nodebase.xyz/cgi-bin/hits-all.js
# refresh total count of all unique visitors to '4d-asset-analysis.html' once a minute
* * * * * /var/www/htdocs/nodebase.xyz/cgi-bin/hits-4daa.sh > /var/www/htdocs/nodebase.xyz/cgi-bin/hits-4daa.js
# refresh total count of all unique visitors to 'taxable-account.html' once a minute
* * * * * /var/www/htdocs/nodebase.xyz/cgi-bin/hits-tba.sh > /var/www/htdocs/nodebase.xyz/cgi-bin/hits-tba.js
# refresh total count of all unique visitors to 'etf-selection.html' once a minute
* * * * * /var/www/htdocs/nodebase.xyz/cgi-bin/hits-etf.sh > /var/www/htdocs/nodebase.xyz/cgi-bin/hits-etf.js
# refresh total count of all unique visitors to 'call-option.html' once a minute
* * * * * /var/www/htdocs/nodebase.xyz/cgi-bin/hits-call.sh > /var/www/htdocs/nodebase.xyz/cgi-bin/hits-call.js
```

**MISC**

some links on creating a vpn server:

```
https://networkfilter.blogspot.com/2017/04/be-your-own-vpn-provider-with-openbsd-v2.html

https://www.openbsdhandbook.com/services/webserver/ssl/
```

some notes on installing solr (search engine):

```
~~~ START: 05/27/2020

# pkg_add solr

~~~ CONTINUE: 05/28/2020

# solr start

*** [WARN] *** Your open file limit is currently 128.  
 It should be set to 65000 to avoid operational disruption. 
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
*** [WARN] ***  Your Max Processes Limit is currently 1310. 
 It should be set to 65000 to avoid operational disruption. 
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
*** [WARN] ***  Your Virtual Memory limit is 33562624. 
 It should be set to 'unlimited' to avoid operational disruption. 
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
*** [WARN] ***  Your Max Memory Size limit is 986056. 
 It should be set to 'unlimited' to avoid operational disruption. 
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
WARNING: Starting Solr as the root user is a security risk and not considered best practice. Exiting.
         Please consult the Reference Guide. To override this check, start with argument '-force'

openbsd# free
                     total              used              free
Mem:                 1007M              416M              591M
Swap:                 255M                0B              255M

openbsd$ solr start

*** [WARN] *** Your open file limit is currently 512.  
 It should be set to 65000 to avoid operational disruption. 

*** [WARN] ***  Your Max Processes Limit is currently 128. 
 It should be set to 65000 to avoid operational disruption. 

*** [WARN] ***  Your Virtual Memory limit is 790528. 
 It should be set to 'unlimited' to avoid operational disruption. 

*** [WARN] ***  Your Max Memory Size limit is 986056. 
 It should be set to 'unlimited' to avoid operational disruption. 

 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh

ERROR: Logs directory /usr/local/share/solr/server/logs could not be created. Exiting

SEE: https://lucene.apache.org/solr/guide/8_5/configuring-logging.html#configuring-logging

openbsd$ pwd
/usr/local/share/solr/server/resources

openbsd$ cat log4j2.xml | grep "sys:solr.log.dir"                                                                                                                                                                   
        fileName="${sys:solr.log.dir}/solr.log"
        filePattern="${sys:solr.log.dir}/solr.log.%i" >
        fileName="${sys:solr.log.dir}/solr_slow_requests.log"
        filePattern="${sys:solr.log.dir}/solr_slow_requests.log.%i" >
        fileName="${sys:solr.log.dir}/solr.log"
        filePattern="${sys:solr.log.dir}/solr.log.%i" >
        fileName="${sys:solr.log.dir}/solr_slow_requests.log"
        filePattern="${sys:solr.log.dir}/solr_slow_requests.log.%i" >

openbsd$ cat /etc/passwd | grep solr
_solr:*:801:801:solr user:/nonexistent:/sbin/nologin

openbsd$ doas rcctl enable solr

openbsd$ rcctl ls on  
check_quotas
cron
httpd
library_aslr
ntpd
pf
pflogd
slaacd
smtpd
sndiod
solr
sshd
syslogd

openbsd$ doas rcctl ls stopped | grep solr
solr

OK: solr service is not enabled but is stopped

~~~

$ solr start 
...
ERROR: Logs directory /usr/local/share/solr/server/logs could not be created. Exiting
```

<!--
title: The nodebase.xyz Archive
slug: the-nodebase-xyz-archive
status: published
type: post
date: '2023-02-03'
updated: '2023-02-03'
author: bc1984adam
canonical: https://bc1984.com/the-nodebase-xyz-archive/
feature_image: /images/2023/02/Screenshot-at-2023-02-03-08-18-29.png
excerpt: Reflections on building nodebase.xyz on OpenBSD. Post archive and technical
  learnings.
-->
