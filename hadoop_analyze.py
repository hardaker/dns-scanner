#!/usr/bin/python

import copy

class HadoopAnalyze(object):
    def __init__(self):
        pass

    def print_count_fields_at_path(self, records, paths, results = {}):
        results = self.count_fields_at_path(records, paths, results)
        for result in results:
            print result + "\t" + str(results[result])

    def count_fields_at_path(self, records, paths, results = {}):
        nextpath = paths.pop(0)
        if len(paths) == 0:
            self.count_fields2(records, nextpath, results)
        else:
            for record in records:
                if nextpath not in record:
                    print "location: " + str(record)
                    print "ERROR: the '" + nextpath + "' field could not be found"
                    exit(1)
                if type(record[nextpath]) != list:
                    record[nextpath] = [ record[nextpath] ]
                self.count_fields_at_path(record[nextpath], copy.deepcopy(paths), results)
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

    ha = HadoopAnalyze()
    print "TTLs:"
    ha.print_count_fields(results)

    print ""
    print "type:"
    ha.print_count_fields(results, 'type')

    print ""
    print "section:"
    ha.print_count_fields(results, 'section')
    
    print ""
    print "do:"
    returnpath = {}
    print ha.count_fields_at_path(results, ["do"], returnpath)
    print returnpath

    print ""
    print "ttl:"
    returnpath = {}
    print ha.count_fields_at_path(results, ["records", "ttl"], returnpath)
    print returnpath

    print ""
    print "nsdname:"
    returnpath = {}
    print ha.count_fields_at_path(results, ["records", "rrdata", "nsdname"], returnpath)
    print returnpath

    print ""
    print "nsdname via return:"
    returnpath = ha.count_fields_at_path(results, ["records", "rrdata", "nsdname"], {})
    print returnpath

    print ""
    print "ipv4 address via return:"
    returnpath = ha.count_fields_at_path(results, ["records", "rrdata", "ipv4_address"], {})
    print returnpath
    
