#!/usr/bin/env python3

from nfsn import NFSNAuth

import requests
from time import strftime, localtime
import dns.resolver
import socket

user = "username" # Your NFSN username (not the one used to ssh into your site)
api_key = "API_KEY" # API key (contact NFSN support for one - it's a free request)
domain = "example.com" # Your NFS-hosted domain
subdomain = "" # The subdomain you're setting up for dynamic DNS, leave empty if root.
dns_serv = "ns.phx3.nearlyfreespeech.net"

currentip = requests.get('https://checkip.amazonaws.com/').text.replace('\r', '').replace('\n', '')
resolver = dns.resolver.Resolver()
resolver.nameservers = [socket.gethostbyname(dns_serv)]
full_domain = domain if subdomain == "" else subdomain + "." + domain
listedip = resolver.query(full_domain).response.answer[0].items[0].address

class nfsn_api:
    def __init__(self, user, key):
        self.session = requests.session()
        self.session.auth = NFSNAuth(key, user)

    def get_ip(self, domain, subdomain):
        resp = self.session.post("https://api.nearlyfreespeech.net/dns/{}/listRRs".format(domain))
        if resp.status_code != 200:
            raise RuntimeError('Could not get IP address for {}.{}.'.format(subdomain,domain))
        for item in resp.json():
            if item["name"] == subdomain and item["type"] == "A":
                return item["data"]
        return None

    def del_record(self, domain, subdomain, data, rtype='A'):
        resp = self.session.post("https://api.nearlyfreespeech.net/dns/{}/removeRR".format(domain), data={
            'name':subdomain,
            'type':rtype,
            'data':data})
        if resp.status_code != 200:
            raise RuntimeError('Could not del {} record {} for {}.{}.'.format(rtype, data, subdomain, domain))

    def put_record(self, domain, subdomain, data, rtype='A', ttl='300'):
        resp = self.session.post("https://api.nearlyfreespeech.net/dns/{}/addRR".format(domain), data={
            'name':subdomain,
            'type':rtype,
            'data':data,
            'ttl':ttl})
        if resp.status_code != 200:
            raise RuntimeError('Could not put {} record {} for {}.{}.'.format(rtype, data, subdomain, domain))

logtime = strftime("%Y-%m-%d %H%M", localtime())

if currentip != listedip:
    nfsn = nfsn_api(user, api_key)
    listedip = nfsn.get_ip(domain, subdomain)

    if currentip != listedip:   # Check to see if we need to update the record; if so:
        if listedip:
            nfsn.del_record(domain, subdomain, listedip) # a) remove the old entry,
        nfsn.put_record(domain, subdomain, currentip)   # b) add a new entry with the new IP
        print("{} DNS record updated from {} to {}".format(logtime, listedip, currentip))
    else:
        print(logtime + " Update is pending.")
else:
    print(logtime + " No update needed.")

