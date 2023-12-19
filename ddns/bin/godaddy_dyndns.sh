#!/bin/bash


gdapikey="<%= gdapikey %>"
logdest="local7.info"

myip=`curl -s "https://api.ipify.org"`
set_dyndns() {
    mydomain="$1"
    recordname="$2"
    dnsdata=`curl -s -X GET -H "Authorization: sso-key ${gdapikey}" "https://api.godaddy.com/v1/domains/${mydomain}/records/A/${recordname}"`
    gdip=`echo $dnsdata | cut -d ',' -f 1 | tr -d '"' | cut -d ":" -f 2`
    echo "`date '+%Y-%m-%d %H:%M:%S'` - $recordname.$mydomain points to $gdip, this host is $myip"

    if [ "$gdip" != "$myip" -a "$myip" != "" ]; then
        echo "IP has changed! Updating $mydomain to $myip"
        curl -s -X PUT "https://api.godaddy.com/v1/domains/${mydomain}/records/A/${recordname}" -H "Authorization: sso-key ${gdapikey}" -H "Content-Type: application/json" -d "[{\"data\": \"${myip}\"}]"
        logger -p $logdest "Changed IP on ${hostname}.${mydomain} from ${gdip} to ${myip}"
        dnsdata=`curl -s -X GET -H "Authorization: sso-key ${gdapikey}" "https://api.godaddy.com/v1/domains/${mydomain}/records/A/${myhostname}"`
        gdip=`echo $dnsdata | cut -d ',' -f 1 | tr -d '"' | cut -d ":" -f 2`
        echo "Changed IP on $hostname.$mydomain to $gdip"
    fi
}

set_dyndns "site.tld" "@";
