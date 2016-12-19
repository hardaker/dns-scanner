import getdns

class Scan_Records(object):

    def __init__(self, debug = False):
        self.context = getdns.Context()
        self.extensions = { "dnssec_return_status": getdns.EXTENSION_TRUE }
        self.context.edns_do_bit = 1
        self.debug = debug
        self.count = 0

    def query(self, name, type):
        self.count = self.count + 1
        self.__debug("[" + str(self.count) + "] scanning " + name + " for type " + str(type))
        results = self.context.general(name = name, request_type = type,
                                       extensions = self.extensions)
        return results

    def query_typelist(self, name, typelist):
        all_results = []
        for type in typelist:
            results = self.query(name, type)
            textstatus = "good"
            if results.status == getdns.RESPSTATUS_GOOD:
                all_results.append(results)
            else:
                textstatus = "bad"
            self.__debug("[" + str(self.count) + "]%-4s: %-30.30s %d" % (textstatus, name, type))
        return all_results
    
    def query_domains_with_each_typelist(self, names, typelist):
        all_results = []
        for name in names:
            for type in typelist:
                results = self.query(name, type)
                textstatus = "good"
                if results.status == getdns.RESPSTATUS_GOOD:
                    all_results.append(results)
                else:
                    textstatus = "bad"
                self.__debug("[" + str(self.count) + "]%-4s: %-30.30s %d" % (textstatus, name, type))
        return all_results

    def query_domains_with_individual_typelists(self, todolist):
        all_results = []
        for name in todolist:
            for rtype in todolist[name]:
                results = self.query(name, rtype)
                textstatus = "good"
                if results.status == getdns.RESPSTATUS_GOOD:
                    all_results.append(results)
                else:
                    textstatus = "bad"
                self.__debug("[" + str(self.count) + "]%-4s: %-30.30s %d" % (textstatus, name, rtype))
        return all_results

    def __debug(self, output):
        if (self.debug):
            print(output)

def dump_records(results):
    for result in results:  # dict
        print "----"
        print result
        data = result.replies_full
        for reply in data['replies_tree']:  # data.replies_tree is an array
            for record in reply['answer']:
                print ("> %30s %8d %4d %s" % (record['name'], record['ttl'], record['type'], "ugh"))
            for record in reply['authority']:
                print ("A %30s %8d %4d %s" % (record['name'], record['ttl'], record['type'], "ugh"))
            for record in reply['additional']:
                if 'name' in record: # don't do EDNS0 records
                    print ("+ %30s %8d %4d %s" % (record['name'], record['ttl'], record['type'], "ugh"))
                else:
                    print "# do=" + str(record['do']) + ", udp_payload_size: " + str(record['udp_payload_size'])


def main():
    it = Scan_Records(debug = True)
    print it
    results = it.query_typelist("b.root-servers.net", [getdns.RRTYPE_A, getdns.RRTYPE_AAAA])
    results = it.query_many_with_typelist(["b.root-servers.net",
                                           "hardakers.net"],
                                          [getdns.RRTYPE_A, getdns.RRTYPE_NS])
    dump_records(results)
            

    # RRTYPE_DSq

if __name__ == "__main__":
    main()
