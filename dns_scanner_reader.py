#!/usr/bin/python

import re

class DnsScannerReader(object):

    def __init__(self):
        # we use statse to decrease the regexp matches needed
        self.STARTING = 0
        self.INRECORD = 1

        self.state = self.STARTING

        self.startMatch = re.compile("^# t=([0-d]+)")
        self.endMatch   = re.compile("^E (.*)")
        # linetype, name, ttl, rrtype, rrdata
        self.lineMatch  = re.compile("^([>A\+])\s+(\S+)\s+(\d+)\s+(\S+)\s+(.*)")
        self.tokenMatch = re.compile("([^=]+)=(.*)")

        self.records    = []

    def parse_attributes(self, tokens):
        results = {}
        for token in tokens.split(" "):
            match = self.tokenMatch.match(token)
            results[match.group(1)] = match.group(2)
        return results

    def read_file(self, file, output = None):

        if not output:
            output = []

        fh = open(file, "r")
        for line in fh:
            if self.state == self.STARTING:
                result = self.startMatch.match(line)
                if result:
                    self.state = self.INRECORD
                    self.data = { 't':       result.group(1),
                                  'records': [] }
                else:
                    self.warning("unrecognized line: " + line)
            else:
                result = self.endMatch.match(line)
                if result:
                    self.state = self.STARTING
                    self.data.update(self.parse_attributes(result.group(1)))
                    output.append(self.data)
                    self.data = { 'records': [] } # shouldn't be needed but done for safety
                else:
                    result = self.lineMatch.match(line)
                    if result:
                        record = {}
                        record['section'] = result.group(1)
                        record['name'] = result.group(2)
                        record['ttl'] = result.group(3)
                        record['type'] = result.group(4)
                        record['rrdata'] = self.parse_attributes(result.group(5))
                        self.data['records'].append(record)
                    else:
                        self.warning("unknown line in record: " + line)
        return output

    def warning(self, line):
        print "WARNING: " + line
            
if __name__ == "__main__":
    dsr = DnsScannerReader()
    result = dsr.parse_attributes("a=b cde=efg/abc")
    print(result)

    results = dsr.read_file('dns_scanner_results/capturedonearth.com./A/2016/12/20.txt')
    print results
