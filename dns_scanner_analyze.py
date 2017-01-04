#!/usr/bin/python

import copy

class DnsScannerAnalyze(object):
    def __init__(self):
        pass

    def print_count_fields_at_path(self, records, paths, results = {}):
        results = self.count_fields_at_path(records, paths, 0, results)
        for result in results:
            print result + "\t" + str(results[result])

    def count_fields_at_path(self, records, paths, depth = 0, results = {}):
        nextpath = paths[depth]
        #print "at " + str(depth) + ": "+ nextpath + " in " + str(paths)
        if depth == len(paths)-1:
            self.count_fields2(records, nextpath, results)
        else:
            for record in records:
                if nextpath not in record:
                    pass
                    #print "location: " + str(record)
                    #print "ERROR: the '" + nextpath + "' field could not be found"
                    #exit(1)
                else:
                    if type(record[nextpath]) != list:
                        record[nextpath] = [ record[nextpath] ]
                    self.count_fields_at_path(record[nextpath], paths, depth + 1, results)
        return results

    def count_fields2(self, records, field = 'ttl', results = {}):
        for record in records:
            if field not in record:
                pass
            elif record[field] not in results:
                results[record[field]] = 1
            else:
                results[record[field]] = results[record[field]] + 1
        return results

    def count_fields(self, records, field = 'ttl', results = {}):
        for record in records:
            for subrecord in record['records']:
                if subrecord[field] not in results:
                    results[subrecord[field]] = 1
                else:
                    results[subrecord[field]] = results[subrecord[field]] + 1
        return results

    def print_count_fields(self, records, field = 'ttl'):
        results = self.count_fields(records, field)
        for result in results:
            print result + "\t" + str(results[result])

if __name__ == "__main__":
    import dns_scanner_reader
    dsr = dns_scanner_reader.DnsScannerReader()
    results = dsr.read_directory_of_files('dns_scanner_results')
    
    dsa = DnsScannerAnalyze()
    print "TTLs:"
    dsa.print_count_fields(results)

    print ""
    print "type:"
    dsa.print_count_fields(results, 'type')

    print ""
    print "section:"
    dsa.print_count_fields(results, 'section')
    
    print ""
    print "do:"
    returnpath = {}
    print dsa.count_fields_at_path(results, ["do"], returnpath)
    print returnpath

    print ""
    print "ttl:"
    returnpath = {}
    print dsa.count_fields_at_path(results, ["records", "ttl"], returnpath)
    print returnpath

    print ""
    print "nsdname:"
    returnpath = {}
    print dsa.count_fields_at_path(results, ["records", "rrdata", "nsdname"], returnpath)
    print returnpath

    print ""
    print "nsdname via return:"
    returnpath = dsa.count_fields_at_path(results, ["records", "rrdata", "nsdname"], {})
    print returnpath

    print ""
    print "ipv4 address via return:"
    returnpath = dsa.count_fields_at_path(results, ["records", "rrdata", "ipv4_address"], {})
    print returnpath
    
