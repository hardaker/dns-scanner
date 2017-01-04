#!/usr/bin/python

import copy

class DnsScannerAnalyze(object):
    """
    Takes output from the `DnsScannerReader` class and analyzes it for patterns.

    Example:
        import dns_scanner_reader
        import dns_scanner_analyze

        dsr = dns_scanner_reader.DnsScannerReader()
        results = dsr.read_directory_of_files('dns_scanner_results')

        dsa = dns_scanner_analyze.DnsScannerAnalyze()
        dsa.print_count_fields_at_path(results, ["records","ttl"])

    """ 

    def __init__(self):
        pass

    def print_count_fields_at_path(self, records, paths, results = {}):
        """
        Calls count_fields_at_path() and then prints the results to stdout
        """
        results = self.count_fields_at_path(records, paths, results, 0)

        for result in results:
            print result + "\t" + str(results[result])

    def count_fields_at_path(self, records, paths, results = {}, depth = 0):
        """
        For a given set of `records`, count each `path` in `paths` 
        within the dataset.  Return a list of counted results in the opassed
        `results`.

        Example paths might include ['records', 'ttl'] or
        ['records']['rrdata']['ipv4_address'].

        Example:
        results = scannerAnalyzer.count_fields_at_path(records, ['records','ttl'])
        """

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
                    self.count_fields_at_path(record[nextpath], paths, results, depth + 1)
        return results

    def find_paths(self, records, prefix = "", results = {}):
        """
        Find all the names of the path hierarchy found in the `records`.

        Example:
        results = scannerAnalyzer.find_paths(records)

        """

        for field in records:
            if type(field) == dict: # records was an array
                results = self.find_paths(field, prefix, results)
            else:
                fullpath = prefix + "/" + field
                if type(records[field]) == list:
                    # sub array
                    self.find_paths(records[field], fullpath, results)
                elif type(records[field]) == str:
                    if fullpath not in results:
                        results[fullpath] = 1
                else: # type is a dictionary
                    self.find_paths(records[field], fullpath, results)

        return results

    def print_paths(self, records, results = {}):
        results = self.find_paths(records, results = results)
        keys = results.keys()
        keys.sort()
        for result in keys:
            print result

    def count_fields2(self, records, field = 'ttl', results = {}):
        """
        For a given set of `records`, count each `field` name in each
        record adding them all together and optionally storing them in
        the `results` dictonary.

        Example:
        results = scannerAnalyzer.count_fields(records, 'ttl')
        """

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
        """
        Executes `count_fields()` and then prints the resuls to stdout
        """

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
    print "paths:"
    dsa.print_paths(results)

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
    
