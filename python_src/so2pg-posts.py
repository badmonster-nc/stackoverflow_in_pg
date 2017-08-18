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
print "COPY posts (id, type, creation, score, viewcount, title, body, userid, lastactivity, tags, answercount, commentcount) FROM stdin;"

for event, post in posts:
    if event == "end" and post.tag == "row":
        id = int(post.attrib["Id"])

        if post.attrib.has_key("PostTypeId"):
            type = int(post.attrib["PostTypeId"])
        else:
            type = "\N"

        creation = post.attrib["CreationDate"]

        if post.attrib.has_key("Score"):
            score = int(post.attrib["Score"])
        else:
            score = "\N"

        if post.attrib.has_key("ViewCount"):
            viewcount = int(post.attrib["ViewCount"])
        else:
            viewcount = "\N"

        if post.attrib.has_key("Title"):
            title = escape(post.attrib["Title"])
        else:
            title = "\N"

        if post.attrib.has_key("Body"):
            body = escape(post.attrib["Body"])
        else:
            body = "\N"

        if post.attrib.has_key("OwnerUserId"):
            owner = post.attrib["OwnerUserId"]
        else:
            owner = "\N"

        if post.attrib.has_key("LastActivityDate"):
            lastactivity = post.attrib["LastActivityDate"]
        else:
            lastactivity = "\N"
        
        if post.attrib.has_key("Tags"):
            tags = escape(post.attrib["Tags"])
        else:
            tags = "\N"
        
        if post.attrib.has_key("AnswerCount"):
            answercount = int(post.attrib["AnswerCount"])
        else:
            answercount = "\N"

        if post.attrib.has_key("CommentCount"):
            commentcount = int(post.attrib["CommentCount"])
        else:
            commentcount = "\N"

        print "%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (id, type, creation, score, viewcount, title.encode(encoding), body.encode(encoding), owner, lastactivity, tags.encode(encoding), answercount, commentcount)
        post.clear()
    
print "\."

