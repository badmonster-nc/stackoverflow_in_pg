
# Work In Progress
## Requirement

### install postgres 

On ubuntu, [install postgres on ubuntu](install_pg/install_ubuntu.md)\
On centos, [install postgres on centos](install_pg/install_centos.md)

### Import Stackover database in pg
Original source: http://www.bortzmeyer.org/stackoverflow-to-postgresql.html

The social network Stackoverflow regularly publishes a dump of its database under a Creative Commons free licence. We can find dump file here:
Main download link: https://archive.org/download/stackexchange
File download link:
https://archive.org/download/stackexchange/stackoverflow.com-Badges.7z
https://archive.org/download/stackexchange/stackoverflow.com-Comments.7z
https://archive.org/download/stackexchange/stackoverflow.com-PostHistory.7z
https://archive.org/download/stackexchange/stackoverflow.com-PostLinks.7z
https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z
https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z
https://archive.org/download/stackexchange/stackoverflow.com-Users.7z
https://archive.org/download/stackexchange/stackoverflow.com-Votes.7z

Extract the XML file of each downloaded file.

At the time of writing this document, the dump files are from June 2017
Each XML file store a class of Stack Overflow objects:
- Badges: 22 997 200 lines ( 1 658 MB )
- Comments: 58 187 400 lines ( 11 GB )
- PostHistory: 93 512 900 lines ( 54 GB )
- PostLinks: 4 214 710 lines ( 242 MB )
- Posts: 36 149 100 lines ( 31 GB )
- Tags: 49 306 lines ( 2 808 kB )
- Users: 7 246 590 lines ( 773 MB )
- Votes: 128 369 000 lines ( 5 422 MB )

The python_src directory contains a python file per file to be parsed
To launch the parser
```bash
python so2pg-<xml_to_parse>.py <where/my/xml/are> > <path_to_result>/<parsed_xml>.sql
```
If you want test it, in python directory there is a subdirectory named sample_xml.
```bash
#change to directory python_src
#launch 
python so2pg-badges.py ./sample_xml > badges.sql

#you obtain a sql file ready to load to postgres
```