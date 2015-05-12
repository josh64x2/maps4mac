# Searching OSM data in Maps4Mac #

### Simple searches by name: ###
You can do simple searches by name by just putting the name in the search box:
<br><code>Safeway</code>

Will do a case insensitive search for any name that contains the word "safeway".<br>
If you want to search for a name that contains keywords like "Jack in the Box" you need to put it in quotes:<br>
<br><code>"Jack in the Box"</code>

You can also limit a simple search to the visible map by adding "in view" to the end:<br>
<br><code>Safeway in view</code>
<br><code>"Jack in the Box" in view</code>

<h3>Searching for tags:</h3>
To search for objects where a tag is exactly a value you can use:<br>
<br><code>tag = value</code>
<br><code>tag is value</code>

For example:<br>
<br><code>shop = books</code>
<br><code>amenity is cafe</code>

To search for a tag that contains a value you can use:<br>
<br><code>tag contains value</code>

Note that "contains" may get optimized to only search for whole words depending on the database structure.<br>
<br>
For example:<br>
<br><code>name contains Barnes</code><br>
Would find "Barnes and Noble" or "Barnes Bakery" but might not find "Barnstore".<br>
<br>
<h3>Any value for tag:</h3>
To search for anything that has a given tag you can use:<br>
<br><code>tag is not null</code>

For example:<br>
<br><code>place is not null</code>

Will find objects with place=city, place=locality, place=town, etc.<br>
<br>
<h3>Multiple search terms:</h3>
You can join search terms with "and" or "or", if you don't use either "and" will be assumed. You can also use () to group terms.<br>
<br>
For example:<br>
<br><code>shop = book and (name contains Barnes or name contains Borders) in view</code><br>
Will search for all the Barnes and Noble or Borders bookstores in the current view.<br>
<br>
<h3>Raw SQL search:</h3>
If you want to do some operation unsupported by the search syntax you can put "sql" at the start of your search string, this will cause the rest of the string to be used as the where clause without parsing it.<br>
<br><code>sql boundary='national park' and name like '%National Forest'</code><br>

<h3>Search keywords:</h3>
The reserved search keywords are <code>and, or, =, is, contains, within, view, not, null</code>