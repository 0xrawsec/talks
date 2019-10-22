#!/usr/bin/env python

import argparse
import json
import sys
import logging
import re

logger = logging.Logger(__file__)

class Query(object):

    def __init__(self, update=False):
        self.guids = set()
        self.hashes = set()
        self.regexes = {}
        self.update = update
        self.filter_in = set()
        self.filter_out = set()
    
    def add_guids(self, guids):
        for guid in guids:
            # guid normalization
            guid = "{{{0}}}".format(guid.strip("{}"))
            if len(guid) != 38:
                logger.error("Bad guid length for: {0}".format(guid))
                continue
            self.guids.add(guid)
    
    def add_hashes(self, hashes):
        for hash in hashes:
            self.hashes.add(hash)

    def add_regexp(self, regexes):
        for regex in regexes:
            self.regexes[regex] = re.compile(regex, re.I)
    
    def add_filters(self, filters):
        for f in filters:
            f = int(f)
            if f > 0:
                self.filter_in.add(f)
            else:
                self.filter_out.add(-f)

    
    def _update(self, event):
        '''
        Update query object from an event
        '''
        if self.update:
            if "Event" in event:
                if "EventData" in event["Event"]:
                    eventdata = event["Event"]["EventData"]
                    if "ParentProcessGuid" in eventdata and "ProcessGuid" in eventdata:
                        guid = eventdata["ProcessGuid"]
                        self.add_guids([guid])

    def _match_regex(self, s):
        for k, r in self.regexes.items():
            if r.search(s):
                return True
        return False
    
    def _filtered(self, eventid):
        if len(self.filter_in):
            if eventid not in self.filter_in:
                return True
        if len(self.filter_out):
            if eventid in self.filter_out:
                return True
        return False

    
    def match(self, event):
        if "Event" in event:

            if "System" in event["Event"]:
                if "EventID" in event["Event"]["System"]:
                    eid = int(event["Event"]["System"]["EventID"])
                    if self._filtered(eid):
                        return False

            if "EventData" in event["Event"]:
                eventdata = event["Event"]["EventData"]
                # if create process
                if "ParentProcessGuid" in eventdata and "ProcessGuid" in eventdata:
                    ppguid = eventdata["ParentProcessGuid"]
                    guid = eventdata["ProcessGuid"]
                    if guid in self.guids or ppguid in self.guids:
                        self._update(event)
                        return True

                # check for Hashes
                if "Hashes" in eventdata:
                    if eventdata["Hashes"] != '':
                        hashes = [ha.rsplit("=", 1)[1].strip() for ha in eventdata["Hashes"].split(",")]
                        for h in hashes:
                            if h in self.hashes:
                                self._update(event)
                                return True

                # if another kind of event
                for k in eventdata:
                    if "processguid" in k.lower() :
                        if event["Event"]["EventData"][k] in self.guids:
                            self._update(event)
                            return True
                
                for k, v in eventdata.items():
                    if self._match_regex(v):
                        self._update(event)
                        return True
        return False

def gen_events(fd):
    for line in fd.readlines():
        yield json.loads(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recurse", action="store_true", help="Does a recursive search (goes to child processes as well)")
    parser.add_argument("-g", "--guids", type=str, help="Search by ProcessGUIDs (comma split)")
    parser.add_argument("-P", "--regexes", type=str, help="Search by regexp (comma split)")
    parser.add_argument("-c", "--hashes", type=str, help="Search by Hash (comma split)")
    parser.add_argument("-f", "--filters", type=int, nargs="*", help="Filters output to display or not (- prefix) some event ids. Example: -f -10 would filter out ProcessAccess events")
    parser.add_argument("sysmon_json_input", help="Input file in json format or stdin with -")

    args = parser.parse_args()

    query = Query(args.recurse)

    if args.sysmon_json_input == "-":
        eg = gen_events(sys.stdin)
    else:
        eg = gen_events(open(args.sysmon_json_input, "r"))

    if args.guids:
        query.add_guids(args.guids.split(","))
    if args.hashes:
        query.add_hashes(args.hashes.split(","))
    if args.regexes:
        query.add_regexp(args.regexes.split(","))
    if args.filters:
        query.add_filters(args.filters)
    
    for event in eg:
        if query.match(event):
            print(json.dumps(event))
