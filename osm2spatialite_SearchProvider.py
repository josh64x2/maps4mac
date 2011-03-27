#
#  osm2spatialite_SearchProvider.py
#  Maps4Mac
#
#  Created by Daniel Sabo on 1/17/11.
#  Copyright (c) 2011 Daniel Sabo. All rights reserved.
#

from Foundation import *

from pysqlite2 import dbapi2 as sqlite

import SearchParse

def parsedToSQLite(parsed, center = None, viewBounds = None):
    sqlString = ""
    spatialIndexQuery = None
    for rule in parsed:
        if type(rule) == list:
            sqlString += "(" + parsedToSQLite(rule, center, viewBounds) + ") "
        elif rule[0] == "tagEquals":
            sqlString += "\"%s\" = '%s' " % rule[1]
        elif rule[0] == "tagContains":
            sqlString += "\"%s\" like '%%%s%%' " % rule[1]
        elif rule[0] == "tagNotNull":
            sqlString += "\"%s\" is not null " % rule[1]
        elif rule[0] == "withinView" and viewBounds:
            if spatialIndexQuery:
                raise SearchParse.SearchStringParseException("Can't have multiple spatial queries", rule)
            spatialIndexQuery = "(spatial_idx.xmin >= %f and spatial_idx.ymin >= %f and spatial_idx.xmax <= %f and spatial_idx.ymax <= %f and osm.rowid = spatial_idx.pkid)" % \
                         (viewBounds.minx, viewBounds.miny, viewBounds.maxx, viewBounds.maxy)
            if sqlString.endswith(" and "):
                sqlString = sqlString[:-5]
            elif sqlString.endswith(" or "):
                raise SearchParse.SearchStringParseException("Can't join spatial queries with an \"or\"")
        #elif rule[0] == "WithinMeters" and center:
        # BBOX: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
        # PtDistWithin ?
        elif rule == "or":
            sqlString += "or "
        elif rule == "and":
            sqlString += "and "
        elif rule[0] == "sql":
            sqlString += rule[1]
        else:
            raise SearchParse.SearchStringParseException("Rule type not supported by SQLite Search", rule)
    
    if spatialIndexQuery:
        sqlString = "(%s) and (%s)" % (spatialIndexQuery, sqlString)
    
    return sqlString

import math

def GeoDistanceSphere(x1, y1, x2, y2):
    lon_1 = math.radians(float(x1))
    lat_1  = math.radians(float(y1))

    lon_2 = math.radians(float(x2))
    lat_2  = math.radians(float(y2))

    dlon = lon_2 - lon_1
    dlat = lat_2 - lat_1
    a = (math.sin(dlat / 2))**2 + math.cos(lat_1) * math.cos(lat_2) * (math.sin(dlon / 2) ** 2)
    #c = 2 * math.asin(min(1, math.sqrt(a)))
    c = 2 * math.asin(math.sqrt(abs(a)))
    
    dist = 6370986 * c # Radius of spherical earth in meters
    return dist

class osm2spatialite_SearchProvider(NSObject):
    layer = objc.ivar()

    def initWithLayer_(self, layer):
        self = super(self.__class__, self).init()
        if self is None:
            return None
        
        self.layer = layer
        
        return self

    def doSearch(self, commands, center, viewBounds = None):        
        results = None
        
        db = sqlite.connect(self.layer.filename)
        db.create_function("GeoDistanceSphere",4,GeoDistanceSphere)
        sqlite.enable_callback_tracebacks(True)
        
        cursor = db.cursor()
        
        print "Search Query:", commands
        
        # We assume that all the tables have the same tag set
        knownTags = [x[1] for x in cursor.execute("pragma table_info(world_point)").fetchall()]
        del knownTags[knownTags.index("way")]
        #del knownTags[knownTags.index("way_area")]
        #del knownTags[knownTags.index("z_order")]
        
        parser = SearchParse.SearchParser(knownTags)
        tokens = parser.parse(commands)
        
        print "Parsed search:", str(tokens)
        
        query = parsedToSQLite(tokens, center, viewBounds)
        
        print "SQL:", query
        
        results = list()
        
        #TODO: Keep lines instead of centroid
        sql = \
"""select name, ST_AsText(Transform(point, 4326)), type, distance, ST_AsText(Transform(geom, 4326)) from (
select name, point, GeoDistanceSphere(X(Transform(point, 4326)), Y(Transform(point, 4326)), X(ST_GeomFromText('%(center)s', 4326)), Y(ST_GeomFromText('%(center)s', 4326))) as distance, type, way as geom from (
select name, way as point, way, 'point' as type from %(mapName)s_point as osm, idx_%(mapName)s_point_way as spatial_idx where %(query)s
union
select name, ST_StartPoint(way) as point, way, 'line' as type from %(mapName)s_line as osm, idx_%(mapName)s_point_way as spatial_idx where %(query)s
union
select name, ST_Centroid(way) as point, way, 'polygon' as type from %(mapName)s_polygon as osm, idx_%(mapName)s_point_way as spatial_idx where %(query)s
)
) order by distance
""" % {"mapName":"world", "query":query, "center":"POINT(%f %f)" % (center.x, center.y)}
        cursor.execute(sql)
    
        rows = cursor.fetchall()
        
        for row in rows:
            loc = row[1]
            try:
                loc = loc.split("(")[1].split(")")[0].split(" ")
            except IndexError:
                print "Bad geometry for \"%s\": %s" % (row[0], loc)
                break
            loc = map(float, loc)
            
            result = {"type":row[2], "name":row[0], "loc":loc, "distance":row[3]}
            
            if row[2] == "line":
                if not row[4]:
                    print "Bad geometry for \"%s\": %s" % (row[0], loc)
                    continue
                try:
                    points = row[4].split("(")[1].split(")")[0].split(",")
                    points = [map(float, p.strip().split(" ")) for p in points]
                except IndexError:
                    print "Bad geometry for \"%s\": %s" % (row[0], loc)
                except:
                    print row[4]
                    raise
                result["line"] = points
            
            results.append(result)
        db.close()
        
        return results