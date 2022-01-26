# What is this?
This repo hosts an hourly updated list of image MD5 hashes scraped from
4channel's /vt/ board in 4chan X's image MD5 filter format, for the purpose 
of building a comprehensive filter of images containing the vtuber Amelia Watson.

## How can I help?
PRs which make the list more comprehensive are accepted, however, as commits
are automated hourly it's impossible for your PR's `filter.txt` to sync up with
the upstream -- as a conquence, place the image MD5 hashes you would like to
add in a seperate file `pr.txt` so they can be merged into `filter.txt` manually.
Note that MD5 hashes in PRs will be checked against warosu via script, to
ensure there is no "poisoning the well".

If you think this dumbass python trollware somehow warrants implementing 
smarter image checking (i.e. using computer vision to detect Amelia Watson's 
model and colorscheme) and implement it in a working PR, I will personally 
come to your house and suck your dick.
