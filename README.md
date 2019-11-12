# NearlyFreeSpeech.net Dynamic DNS Script

This is a python script that will automatically update your NearlyFreeSpeech.net domain name (or subdomain) to point to the desired dynamic IP address. This script supports Python 3.7.

Usage:
1. Clone the git repository: `git clone https://github.com/iwalton3/nfsn-dynamic-dns`
2. Install the dependencies: `pip3 install dnspython requests`
3. Request an API key. (The request is free.)
4. Configure `upd-nfsn-dns.py` with the domain and user credentials.
5. Configure NTP on the server, as if clock drifts further than 5 seconds the request will fail.
6. Configure a cron job such as `*/5 * * * * /path/to/upd-nfsn-dns.py`.

Based on:
 - https://www.mitsake.net/2016/04/nfsn-and-ddns-take-2/
 - https://github.com/joshkunz/nfsn.py

