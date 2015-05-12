Missing Features:
  * General:
    * Enable the auto download code for the OSM support shapefiles
  * KML:
    * Use the icon and label styles
    * Load polygons
    * HTTP KML layers
  * Searching:
    * Limit results by distance from the map center
    * Style the search results so each search can be distinguished on the map
    * Show all the tags attached to searched nodes, parse opening\_hours
    * Search by address
    * Non-map specific search providers (e.g. search a tiger address database)
  * Styles:
    * Document current style syntax
    * Support multi file styles (most likely by parsing the XML file and handling entities)
    * Dynamically exclude layers based on what tags are in the database
  * MapView:
    * Add popup notification of things like gained/lost GPS fix
  * Layers window:
    * Right click menu for layers & layers objects
  * HTTP Tiles:
    * Implement the HTTP Tiles layer to browse tile based internet maps

osm2spatialite Missing Features:
  * Allow user specified tags to import all the tags in a namespace (e.g. "addr:" would import "addr:housenumber", "addr:street", etc.)