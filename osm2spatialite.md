osm2spatialite is a python script that converts an OSM xml or pbf file into a [SpatiaLite](http://www.gaia-gis.it/spatialite/) database with approximately the same format as an [osm2pgsql](http://wiki.openstreetmap.org/wiki/Osm2pgsql) database.

Usage:
`python osm2spatialite.py output.sqlite input.osm`

## Dependencies ##
osm2spatialite requires Shapely and a SQLite module with SpatiaLite built in. If you need to run a command to load the SpatiaLite module you should add it to the `trydb` function.

## Mapnik datasource-settings.xml.inc ##
```
<Parameter name="type">sqlite</Parameter>
<Parameter name="file">Your filename here</Parameter>
<Parameter name="key_field">rowid</Parameter>
<Parameter name="geometry_field">way</Parameter>
<Parameter name="wkb_format">spatialite</Parameter>
<Parameter name="estimate_extent">false</Parameter>
<Parameter name="extent">180.0,89.0,-180.0,-89.0</Parameter>
```

## Changes needed to a osm2pgsql mapnik style ##

Remove all `::text` directives.

Any sql that accesses world\_roads needs  `way` changed to `CastToMulti(way) as way`

I don't know why but addr:housenumber offends sqlite, so in layer-addressing.xml.inc change:<br>
<code>&lt;TextSymbolizer name="addr:housenumber"</code><br>
to<br>
<code>&lt;TextSymbolizer name="addr_housenumber"</code><br>
and<br>
<code>(select way,"addr:housenumber"</code><br>
to<br>
<code>(select way,"addr:housenumber" as addr_housenumber</code>

<h2>Changes Needed to Use Spatial Index</h2>
Because of the way mapnik modifies SQL queries to use the SpatiaLite spatial indexes a the where clause needs to be enclosed in ()s:<br>
<pre><code>      &lt;Parameter name="table"&gt;<br>
      (select way,"natural",waterway,landuse,name<br>
      from &amp;prefix;_polygon<br>
      where waterway in ('dock','mill_pond','riverbank','canal')<br>
         or landuse in ('reservoir','water','basin')<br>
         or "natural" in ('lake','water','land','marsh','scrub','wetland','glacier')<br>
      order by z_order,way_area desc<br>
      ) as water_areas&lt;/Parameter&gt;<br>
</code></pre>
becomes<br>
<pre><code><br>
      &lt;Parameter name="table"&gt;<br>
      (select way,"natural",waterway,landuse,name<br>
      from &amp;prefix;_polygon<br>
      where (waterway in ('dock','mill_pond','riverbank','canal')<br>
         or landuse in ('reservoir','water','basin')<br>
         or "natural" in ('lake','water','land','marsh','scrub','wetland','glacier'))<br>
      order by z_order,way_area desc<br>
      ) as water_areas&lt;/Parameter&gt;<br>
</code></pre>
because when mapnik processes the table block it will replace "where" with "where (spatial index stuff) and ".<br>
<br>
<h2>Technical differences</h2>
Because SpatialLite has no wildcard geometry type world_roads is populated with GEOMETRYCOLLECTION objects, for mapnik to understand these they need to be cast to polygons or linestrings.<br>
<br>
The world_roads and world_polygon tables have a column called osm_type so that the original osm_id can be stored for relations, therefor osm_id is not guaranteed to be unique in these tables.