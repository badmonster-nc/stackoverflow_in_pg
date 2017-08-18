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

filename = "Tags.xml"
tags = ElementTree.iterparse(filename) 
print "COPY tags (id, name, count, excerptpost, wikipost) FROM stdin;"
for event, tag in tags:
    if event == "end" and tag.tag == "row":
        id = int(tag.attrib["Id"])

        name = tag.attrib["TagName"]

        count = int(tag.attrib["Count"])
        
        if tag.attrib.has_key("ExcerptPostId"):
            excerptpost = tag.attrib["ExcerptPostId"]
        else:
            excerptpost = "\N"
        
        if tag.attrib.has_key("WikiPostId"):
            wikipost = tag.attrib["WikiPostId"]
        else:
            wikipost = "\N"

        print "%i\t%s\t%s\t%s\t%s" % (id, name, count, excerptpost, wikipost)
        tag.clear()
print "\."