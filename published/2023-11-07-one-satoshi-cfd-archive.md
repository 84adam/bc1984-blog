![onesatoshi.cfd Archive](/images/2023/11/final-screenshot-110723.png)

A simple site that tracked the price of bitcoin in terms of satoshis per dollar, where 1 BITCOIN = 100,000,000 SATOSHIS.

## onesatoshi.cfd

<https://archive.ph/XkB3k>  
<https://web.archive.org/web/20230501172907/https://onesatoshi.cfd/>

## Notes

I used a view counter I built using a simple bash script and one line of javascript:

## hitcount.sh

This was run on a cron job and updated the latest 'unique hit count' every 5 minutes.

```
#!/bin/bash

# get all the unique IP addresses that have hit the server today
# write these to the uniq-ips.txt file
echo "$(cat /var/log/caddy/onesatoshi.cfd-access.log | fgrep '"host":"onesatoshi.cfd","uri":"/"' | while read line ; do echo $line | cut -d "{" -f 3 | cut -d "," -f 1 | cut -d '"' -f 4 ; done ;)" | sort | uniq >> /var/log/caddy/uniq-ips.txt

sleep 2 ;
# count the total number of unique IPs from all time that have visited the site
# save total visitor count to visitor-count.txt
cat /var/log/caddy/uniq-ips.txt | sort | uniq | wc -l > /var/log/caddy/visitor-count.txt

sleep 2 ;

COUNT="$(cat /var/log/caddy/visitor-count.txt)" ;

#echo "Current Hit Count = $COUNT" ;

echo "document.writeln (\"<code>UNIQUE VISITORS: $COUNT</code>\")" > /var/www/visitors.js
```

## /var/www/visitors.js

This was the javascript one-liner that was pulled directly into the index.html page:

```
document.writeln ("<code>UNIQUE VISITORS: 3540</code>")
```

Within index.html, this script was called as follows:

```
<p style="font-size: 0.7em;color:#555555;"><script src="visitors.js" type="text/javascript"></script></p>
```

<!--
title: onesatoshi.cfd Archive
slug: one-satoshi-cfd-archive
status: published
type: post
date: '2023-11-07'
updated: '2023-11-07'
author: bc1984adam
canonical: https://bc1984.com/one-satoshi-cfd-archive/
feature_image: /images/2023/11/final-screenshot-110723.png
-->
