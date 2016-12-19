import getdns
import string
import base64
import socket

class RRTypes(object):
    def __init__(self):
        self.rrtypes = {}
        self.rrtypes['A'] = 1
        self.rrtypes['NS'] = 2
        self.rrtypes['MD'] = 3
        self.rrtypes['MF'] = 4
        self.rrtypes['CNAME'] = 5
        self.rrtypes['SOA'] = 6
        self.rrtypes['MB'] = 7
        self.rrtypes['MG'] = 8
        self.rrtypes['MR'] = 9
        self.rrtypes['NULL'] = 10
        self.rrtypes['WKS'] = 11
        self.rrtypes['PTR'] = 12
        self.rrtypes['HINFO'] = 13
        self.rrtypes['MINFO'] = 14
        self.rrtypes['MX'] = 15
        self.rrtypes['TXT'] = 16
        self.rrtypes['RP'] = 17
        self.rrtypes['AFSDB'] = 18
        self.rrtypes['X25'] = 19
        self.rrtypes['ISDN'] = 20
        self.rrtypes['RT'] = 21
        self.rrtypes['NSAP'] = 22
        self.rrtypes['SIG'] = 24
        self.rrtypes['KEY'] = 25
        self.rrtypes['PX'] = 26
        self.rrtypes['GPOS'] = 27
        self.rrtypes['AAAA'] = 28
        self.rrtypes['LOC'] = 29
        self.rrtypes['NXT'] = 30
        self.rrtypes['EID'] = 31
        self.rrtypes['NIMLOC'] = 32
        self.rrtypes['SRV'] = 33
        self.rrtypes['ATMA'] = 34
        self.rrtypes['NAPTR'] = 35
        self.rrtypes['KX'] = 36
        self.rrtypes['CERT'] = 37
        self.rrtypes['A6'] = 38
        self.rrtypes['DNAME'] = 39
        self.rrtypes['SINK'] = 40
        self.rrtypes['OPT'] = 41
        self.rrtypes['APL'] = 42
        self.rrtypes['DS'] = 43
        self.rrtypes['SSHFP'] = 44
        self.rrtypes['IPSECKEY'] = 45
        self.rrtypes['RRSIG'] = 46
        self.rrtypes['NSEC'] = 47
        self.rrtypes['DNSKEY'] = 48
        self.rrtypes['DHCID'] = 49
        self.rrtypes['NSEC3'] = 50
        self.rrtypes['NSEC3PARAM'] = 51
        self.rrtypes['TLSA'] = 52
        self.rrtypes['HIP'] = 55
        self.rrtypes['NINFO'] = 56
        self.rrtypes['RKEY'] = 57
        self.rrtypes['TALINK'] = 58
        self.rrtypes['CDS'] = 59
        self.rrtypes['CDNSKEY'] = 60
        self.rrtypes['OPENPGPKEY'] = 61
        self.rrtypes['CSYNC'] = 62
        self.rrtypes['SPF'] = 99
        self.rrtypes['UINFO'] = 100
        self.rrtypes['UID'] = 101
        self.rrtypes['GID'] = 102
        self.rrtypes['UNSPEC'] = 103
        self.rrtypes['NID'] = 104
        self.rrtypes['L32'] = 105
        self.rrtypes['L64'] = 106
        self.rrtypes['LP'] = 107
        self.rrtypes['EUI48'] = 108
        self.rrtypes['EUI64'] = 109
        self.rrtypes['TKEY'] = 249
        self.rrtypes['TSIG'] = 250
        self.rrtypes['IXFR'] = 251
        self.rrtypes['AXFR'] = 252
        self.rrtypes['MAILB'] = 253
        self.rrtypes['MAILA'] = 254
        self.rrtypes['ANY'] = 255
        self.rrtypes['URI'] = 256
        self.rrtypes['CAA'] = 257
        self.rrtypes['TA'] = 32768
        self.rrtypes['DLV'] = 32769

        self.rrvals = {v: k for k, v in self.rrtypes.iteritems() }

    def rrtype_to_int(self, name):
        return self.rrtypes[name]

    def int_to_rrtype(self, val):
        return self.rrvals[val]

    def sprint_rdata(self, record):
        result = ""

        if 'rdata' not in record:
            return result

        for key in record['rdata']:
            if key == 'rdata_raw':
                pass
            else:
                result = result + " " + key + "="

                # add the data either straight or base64 if needed
                if all(c in string.printable for c in str(record['rdata'][key])):
                    result = result + str(record['rdata'][key])
                elif key == 'ipv4_address':
                    result = result + socket.inet_ntoa(record['rdata'][key])
                elif key == 'ipv6_address':
                    result = result + socket.inet_ntop(socket.AF_INET6, record['rdata'][key])
                else:
                    result = result + base64.b64encode(str(record['rdata'][key]))

        return result

if __name__ == "__main__":
    ty = RRTypes()
    print "TKEY = " + str(ty.rrtype_to_int('TKEY'))
    print "249  = " + ty.int_to_rrtype(249)
    
