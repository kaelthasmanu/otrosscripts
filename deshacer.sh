#!/bin/sh
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -Z # zero counters
iptables -F # flush (delete) rules
iptables -X # delete all extra chains

