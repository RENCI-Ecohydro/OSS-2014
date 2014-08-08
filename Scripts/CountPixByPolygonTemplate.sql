-- Template of code to extract numbers of pixels with specific values from raster within individual polygons, as new table.

CREATE TABLE public.ForChYr_CountInt1 AS --Create a New Table ("ForChYr_CountInt1")
  SELECT
    gage_id, (value_count).value, SUM((value_count).count) AS count
  FROM
    (
    SELECT
      gage_id,
      rid,
      ST_ValueCount(
        ST_Union(ST_Clip(rast, geom, TRUE)), 1, FALSE, ARRAY[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
              ) value_count
    FROM
      (SELECT gage_id, geom FROM basinsse) v, --'basinse' represents the basins from the southeast
      (SELECT rid, rast FROM forch_base90pct_int) r --'forch_base90pct_int' represents a raster from which we wanted to count he number of pixels with values listed above in the 'ARRAY' statement (line 12).
    WHERE ST_Intersects(rast, geom)
    GROUP BY gage_id, rid, geom
    ) i
  GROUP BY gage_id, value
  ORDER BY gage_id, value ;