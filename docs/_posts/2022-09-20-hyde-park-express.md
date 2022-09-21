---
layout: post
title: "Summer on the Hyde Park Express"
---

## Motivation
Every Tuesday and Thursday this summer, I rode the Hyde Park Express (#2) bus to and from the UChicago Urban Labs office in downtown Chicago. The bus winds through Hyde Park and Kenwood, then runs express up Lake Shore Drive to reach the Loop. As a tribute to the scenic route and the incredible time I had as a summer data intern, I decided to gather some data on the northbound Hyde Park Express's ridership during the last morning (September 1) I went to the Urban Labs office.[^1]

[^1]: Data gathered with full respect for privacy.

## Mapping the Hyde Park Express
The two maps below represent my best shot at visualizing this data and at practicing my GIS skills.[^2] The bubbles on the **first map** are colored and sized differently to depict the **net entries** (entries minus exits) at each stop on the 2 route; purple corresponds to the most negative amount of net entries, blue and green to a moderate positive amount, and yellow to the most extreme positive amount. This provides visual information (that is hopefully clear) on which stops are popular mass entry or mass exit stops.

[^2]: Shapefiles for the Hyde Park Express stops and route were gathered using QGIS, and the maps were produced using the `mapview` package in R. 

The bubbles on the **second map** differ only in size, with larger bubbles corresponding to higher **passenger traffic** (entries plus exits). Hover over or click the bubbles on either map to see the corresponding data for each stop!

<div class="container">

    <iframe width="100%" height="500" frameborder="0" scrolling="no" src="{{ 'assets/hpe_map.html' | relative_url }}"></iframe>

</div> <!-- /.container -->

<div class="container">

    <iframe width="100%" height="500" frameborder="0" scrolling="no" src="{{ 'assets/hpe_map_traffic.html' | relative_url }}"></iframe>

</div> <!-- /.container -->

## Takeaways

* The first map lends itself to no surprises: most stops where passengers enter are in Hyde Park/Kenwood, and likewise in the Loop for exits. A particularly popular entry point is at the boundary between Hyde Park and Kenwood at Lake Park & E Hyde Park.
* Similarly, the second map shows that the busiest stops are located at the intersections of Lake Park with East Hyde Park and 47th.
  - On the day of, I remember being surprised at how few people were exiting at State & Madison, a popular exit point on the other days that I rode the bus. The small size of the bubble for State & Madison reflects this.
* If I had to make one improvement to the route of the northbound 2 bus, I would cut out the stop at Payne & Cottage Grove. This stop with zero passengers entering/exiting is almost right next to another that recorded one passenger entry (Drexel Square & Cottage Grove).
