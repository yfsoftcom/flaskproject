#### It's for fun

It can search xxx from a xxxx.video.com.

We can only reach the mirror website http://xvideos.sexcache.net insteat of the target https://www.xvideos.com in CN.( Yeah, so bad!!) 

But the website http://xvideos.sexcache.net fills of ~advs~. Emmmmmmm~~~~

We Need This.



## TODO:
- [x] Add Top 3 Hot Search Keywords
- ~[ ] Drop the last entry if length > 500 of the search_keywords map~ Use Sqlite3
- [x] Cache The Search Result For 6 hours
- [x] Add Star Button For Video
- [ ] The MP4 src unused after 1 hours


## Use Redis?
No! Use Sqlite3

- [x] Use Sqlite3 To Save Datas

## Use Docker Environment Domain 

Define an docker environment `NET_MODE`, GLOBAL => www.xvideos.com , CN => xvideos.sexcache.net


```python
os.getenv('NET_MODE', 'GLOBAL')
```