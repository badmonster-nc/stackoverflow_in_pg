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

filename = "Posts.xml"
posts = ElementTree.iterparse(filename) 
tags = {}
tag_id = 1
print "COPY posts (id, type, title, body, creation, owner, accepted_answer) FROM stdin;"
for event, post in posts:
    if event == "end" and post.tag == "row":
        id = int(post.attrib["Id"])
        if post.attrib.has_key("PostTypeId"):
            type = int(post.attrib["PostTypeId"])
        else:
            type = "\\N"
        creation = post.attrib["CreationDate"]
        if post.attrib.has_key("OwnerUserId"):
            owner = post.attrib["OwnerUserId"]
        else:
            owner = "\\N"
        if post.attrib.has_key("Title"):
            title = escape(post.attrib["Title"])
        else:
            title = "\\N"
        if post.attrib.has_key("Body"):
            body = escape(post.attrib["Body"])
        else:
            body = "\\N"

        if post.attrib.has_key("AcceptedAnswerId"):
            accepted_answer = post.attrib["AcceptedAnswerId"]
        else:
            accepted_answer = "\\N"
        print "%i\t%s\t%s\t%s\t%s\t%s\t%s" % (id, type, title.encode(encoding), body.encode(encoding), creation, owner, accepted_answer)
        post.clear()
    
print "\."

