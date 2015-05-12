# Dependencies #

First you need to download and install the
GDAL\_Complete-1.7 framework from http://www.kyngchaos.com/software:frameworks.

Next install "Mapnik 7.1 for Snow Leopard" from http://dbsgeo.com/downloads/. You need to install the package from it called Mapnik\_Framework.pkg, which uses the system python install.

Now you should be able to launch Maps4Mac and get an empty map of the world.

# World Boundaries for OSM #

In order to render OSM data you'll need to download the following files:

http://tile.openstreetmap.org/world_boundaries-spherical.tgz<br>
<a href='http://tile.openstreetmap.org/processed_p.tar.bz2'>http://tile.openstreetmap.org/processed_p.tar.bz2</a><br>
<a href='http://tile.openstreetmap.org/shoreline_300.tar.bz2'>http://tile.openstreetmap.org/shoreline_300.tar.bz2</a><br>

Extract all the files and move their contents into the same directory, so you have the following files in one directory:<br>
<br>
<pre><code>builtup_area.dbf<br>
builtup_area.index<br>
builtup_area.prj<br>
builtup_area.shp<br>
builtup_area.shx<br>
places.dbf<br>
places.prj<br>
places.shp<br>
places.shx<br>
processed_p.dbf<br>
processed_p.index<br>
processed_p.shp<br>
processed_p.shx<br>
shoreline_300.dbf<br>
shoreline_300.index<br>
shoreline_300.shp<br>
shoreline_300.shx<br>
world_bnd_m.dbf<br>
world_bnd_m.index<br>
world_bnd_m.prj<br>
world_bnd_m.shp<br>
world_bnd_m.shx<br>
world_boundaries_m.dbf<br>
world_boundaries_m.index<br>
world_boundaries_m.prj<br>
world_boundaries_m.shp<br>
world_boundaries_m.shx<br>
</code></pre>

Open the Maps4Mac Preferences window and set "Shapefiles path" to the directory you put the files in.<br>
<br>
<h1>Rendering with SpatiaLite (The Easy Option)</h1>
Rendering with SpatiaLite no additional setup, but the current import program is limited in the size of files it can handle. For rendering a map of a single US state or anything smaller it will work fine.<br>
<br>
The only additional step you need to take it to convert your .osm file into a SpatiaLite database by using the osm2spatialite app included with Maps4Mac.<br>
<br>
<h1>Rendering with PostGIS (The Hard Option)</h1>
Setting up PostGIS can be a pain, but if you want really large maps (say, 1/2 the United States in one map) it's necessary. Instructions can be found here <a href='http://wiki.openstreetmap.org/wiki/Mapnik/PostGIS'>http://wiki.openstreetmap.org/wiki/Mapnik/PostGIS</a>. If you go this route the PostGIS provided by <a href='http://www.kyngchaos.com/software:frameworks'>http://www.kyngchaos.com/software:frameworks</a>] has the most features, and <a href='http://dbsgeo.com/downloads/'>http://dbsgeo.com/downloads/</a> provides a precompiled version of osm2pgsql.<br>
<br>
For Maps4Mac to access your database you'll need to install PyGreSQL, you can do this by running:<br>
<pre><code>sudo easy_install pygresql<br>
</code></pre>

<h2>Faster search with PostGIS</h2>
You can get much faster name based searches if you add full text indexes to your PostGIS database, to do this you can use the following SQL commands (replace <code>&lt;dbname&gt;</code> with the appropriate prefix):<br>
<pre><code>create index &lt;dbname&gt;_point_names on &lt;dbname&gt;_point using gin(to_tsvector('simple',name));<br>
create index &lt;dbname&gt;_line_names on &lt;dbname&gt;_line using gin(to_tsvector('simple',name));<br>
create index &lt;dbname&gt;_polygon_names on &lt;dbname&gt;_polygon using gin(to_tsvector('simple',name));<br>
</code></pre>