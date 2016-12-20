from __future__ import print_function

import io
import time
import datetime
import os
import rrtypes

class Archive_Results(object):
    def __init__(self, directory = "./results"):
        self.directory = directory
        self.dateinfo = datetime.date.today()
        self.rrtypes = rrtypes.RRTypes()

    def get_directory(self, subdir = ""):
        return ("%s%s/%04d/%02d" %
                (self.directory, subdir, self.dateinfo.year, self.dateinfo.month))

    def get_made_directory(self, subdir = ""):
        dir = self.get_directory(subdir)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        return dir
    
    def get_filename(self, subdir = "", suffix = ""):
        return ("%s/%02d%s" %
                (self.get_directory(subdir),  self.dateinfo.day, suffix))

    def get_made_filename(self, subdir = "", suffix = ""):
        dir = self.get_made_directory(subdir)
        return self.get_filename(subdir, suffix)

    def archive_results(self, results):
        for result in results:  # dict
            # get the filename to append to
            
            filename = self.get_made_filename("/" + str(result) +
                                              "/" + self.rrtypes.int_to_rrtype(result.replies_full['replies_tree'][0]['question']['qtype']),
                                              ".txt")
            saveto = open(filename, "a")

            print("# t=" + str(int(time.time())), file=saveto)

            # loop through the data and send it tot the file
            data = result.replies_full
            for reply in data['replies_tree']:  # data.replies_tree is an array
                for record in reply['answer']:
                    print(("> %30s %8d %10s %s" % (record['name'], record['ttl'],
                                                   self.rrtypes.int_to_rrtype(record['type']),
                                                   self.rrtypes.sprint_rdata(record))),
                          file=saveto)
                for record in reply['authority']:
                    print(("A %30s %8d %10s %s" % (record['name'], record['ttl'],
                                                   self.rrtypes.int_to_rrtype(record['type']),
                                                   self.rrtypes.sprint_rdata(record))),
                          file=saveto)
                for record in reply['additional']:
                    if 'name' in record: # don't do EDNS0 records
                        print(("+ %30s %8d %10s %s" % (record['name'], record['ttl'],
                                                       self.rrtypes.int_to_rrtype(record['type']),
                                                       self.rrtypes.sprint_rdata(record))),
                              file=saveto)
                    else:
                        print(("E do=" + str(record['do']) + " udp_payload_size=" + str(record['udp_payload_size'])), file=saveto)
    
def main():
    ar = Archive_Results()
    print("test directory: " + ar.get_directory())
    print("test filename:  " + ar.get_filename())
    print("test filename2: " + ar.get_filename("-foo.csv"))
         
    print("test directory: " + ar.get_directory("/zone"))
    print("test filename:  " + ar.get_filename("/zone"))
    print("test filename2: " + ar.get_filename("/zone", "-foo.csv"))
    
    ar = Archive_Results("/tmp/results")
    print("test directory: " + ar.get_made_directory("/zone"))

if __name__ == "__main__":
    main()
