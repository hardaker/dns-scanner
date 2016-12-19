## About

`dns-scanner` is a simple tool to query DNS records and archive the
results in a flat-file structure.  That is given an input file such as
this:

	google.com,A
	google.com,AAAA
	youtube.com,NS

It will produce a directory files such as:

	dns_scanner_results/
	dns_scanner_results/google.com.
	dns_scanner_results/google.com./AAAA
	dns_scanner_results/google.com./AAAA/2016
	dns_scanner_results/google.com./AAAA/2016/12
	dns_scanner_results/google.com./AAAA/2016/12/19.txt
	dns_scanner_results/google.com./A
	dns_scanner_results/google.com./A/2016
	dns_scanner_results/google.com./A/2016/12
	dns_scanner_results/google.com./A/2016/12/19.txt
	dns_scanner_results/youtube.com.
	dns_scanner_results/youtube.com./NS
	dns_scanner_results/youtube.com./NS/2016
	dns_scanner_results/youtube.com./NS/2016/12
	dns_scanner_results/youtube.com./NS/2016/12/19.txt

The contents of the `dns_scanner_results/google.com./A/2016/12/19.txt`
file above may look like this:

	# t=1482184206
	>                    google.com.      300       AAAA  ipv6_address=2607:f8b0:4005:807::200e
	E do=1, udp_payload_size: 4096
	# t=1482184271
	>                    google.com.      300       AAAA  ipv6_address=2607:f8b0:4005:807::200e
	E do=1, udp_payload_size: 4096

Note that the lines starting with `# t=` are delimiters between
consecutive runs, and the `t` value contains the unix epoch stamp of
the record.

## Prerequisites

* The [Python getdns] bindings

[Python getdns]: https://github.com/getdnsapi/getdns-python-bindings

## Author

	Wes Hardaker <hardaker@isi.edu>
	USC/ISI


