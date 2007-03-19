Open-Source OTA Provisioning Platform
First public release notes

Preamble
This tries to be sms-based, web- and sms-driven
tool to do so-called "OTA Provisioning", e.g.
to send WAP-CSD, WAP-GPRS and MMS-{CSD,GPRS} settings
"over-the-air" - via SMS.

Architecture
Main service process should be run, maintaining connections
to SMSCs via SMPP. It accepts various XMLRPC requests, and
do message passing to-from SMSC. It stores requests and DLRs in
database (and gets configuration information for each model from it).

There's also php-based web frontend to OTA-configurator, intended
to be run at service desk.

