#!/bin/sh 
# Block all incoming/outgoing traffic except for ssh and rdp

iptables -Z # zero counters 
iptables -F # flush (delete) rules 
iptables -X # delete all extra chains

#Set default filter policy to DROP#
                                  #
iptables -P INPUT DROP            #
iptables -P OUTPUT ACCEPT         #
iptables -P FORWARD DROP          #
# Allow unlimited traffic on loopback (localhost)###
iptables -A INPUT -i lo -j ACCEPT                  #
iptables -A OUTPUT -o lo -j ACCEPT                 #
####################################################

#Permitir solo IPs de los servidores de Telegram####
Permited_IPS="/media/whois/_home/Permited_IPS.txt"       #
                                                   #
for i in `cat $Permited_IPS`; do                   #
                                                   #
    iptables -I INPUT -s $i -j ACCEPT              #
    iptables -I OUTPUT -s $i -j ACCEPT             #
                                                   #
done                                               #
####################################################





