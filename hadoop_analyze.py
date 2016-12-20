#!/usr/bin/python

class HadoopAnalyze(object):
    def __init__(self):
        pass

    def count_fields(self, records, field = 'ttl'):
        results = {}
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
    
