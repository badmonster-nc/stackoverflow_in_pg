#!/usr/bin/env python

import xml.etree.cElementTree as ElementTree
import os
import sys
import re

db = "so"
encoding = "UTF-8"

def escape(str):
    str = re.sub("\s", " ", str)
    # \ are special for Python strings *and* for regexps. Hence the
    # multiple escaping. Here,we just replace every \ by \\ for
    # PostgreSQL
    str = re.sub("\\\\", "\\\\\\\\", str)
    return str

def tag_parse(str):
    index = 0
    while index < len(str):
        if str[index] == '<':
            try:
                end_tag = str[index:].index('>')
                yield str[(index+1):(index+end_tag)]
                index += end_tag + 1
            except ValueError:
                raise Exception("Tag parsing error in \"%s\"" % str);
        else:
            raise Exception("Tag parsing error in \"%s\"" % str);

if len(sys.argv) != 2:
    raise Exception("Usage: %s so-files-directory" % sys.argv[0])

os.chdir(sys.argv[1])

filename = "Users.xml"
users = ElementTree.iterparse(filename) 
print "COPY users (id, reputation, creation, name, lastaccess, website, location, aboutme, views, upvotes, downvotes, age) FROM stdin;"
for event, user in users:
    if event == "end" and user.tag == "row":
        id = int(user.attrib["Id"])

        reputation = int(user.attrib["Reputation"])

        creation = user.attrib["CreationDate"]

        if user.attrib.has_key("DisplayName"): # Yes, some users have no name, for instance 155 :-(
            name = escape(user.attrib["DisplayName"])
        else:
            name = "\N"

        if user.attrib.has_key("LastAccessDate"): 
            lastaccess = escape(user.attrib["LastAccessDate"])
        else:
            lastaccess = "\N"

        if user.attrib.has_key("WebsiteUrl"):
            website = escape(user.attrib["WebsiteUrl"])
        else:
            website = "\N"

        if user.attrib.has_key("Location"):
            location = escape(user.attrib["Location"])
        else:
            location = "\N"
        
        if user.attrib.has_key("AboutMe"):
            aboutme = escape(user.attrib["AboutMe"])
        else:
            aboutme = "\N"

        if user.attrib.has_key("Views"):
            views = user.attrib["Views"]
        else:
            views = "\N"

        if user.attrib.has_key("UpVotes"):
            upvotes = user.attrib["UpVotes"]
        else:
            upvotes = "\N"

        if user.attrib.has_key("DownVotes"):
            downvotes = user.attrib["DownVotes"]
        else:
            downvotes = "\N"
        
        if user.attrib.has_key("Age"):
            age = user.attrib["Age"]
        else:
            age = "\N"

        print "%i\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (id, reputation, creation, name.encode(encoding), lastaccess, website.encode(encoding), location.encode(encoding), aboutme.encode(encoding), views, upvotes, downvotes, age)
        user.clear()
print "\."