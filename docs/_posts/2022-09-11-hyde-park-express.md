---
layout: post
title: "Summer on the Hyde Park Express"
---

## Motivation
Every Tuesday and Thursday this summer, I rode the Hyde Park Express (#2) bus to and from the UChicago Urban Labs office in downtown Chicago. The bus winds through Hyde Park and Kenwood, then runs express up Lake Shore Drive to reach the Loop. As a tribute to the scenic route and the incredible time I had as a summer data intern, I decided to gather some data on the Hyde Park Express's ridership during the last morning (September 1) I went to the Urban Labs office.

## Mapping the Hyde Park Express
The two maps below represent my best shot at visualizing this data and at practicing my GIS skills. The size and color of the bubbles on the **first map** depict the net entries (entries minus exits) at each stop on the 2 route; purple corresponds to the most negative amount of net entries, blue and green to a moderate positive amount, and yellow to the most extreme positive amount. Rephrased slightly, its goal is to allow the beholder to inspect which stops are popular mass entry or mass exit stops.

The bubbles on the **second map** only differ in size, with larger bubbles corresponding to higher passenger traffic (entries plus exits). You can **hover over** the bubbles on both maps or **click** them to see the corresponding data for each stop.

<div class="container">

    <iframe width="100%" height="500" frameborder="0" scrolling="no" src="{{ 'assets/hpe_map.html' | relative_url }}"></iframe>

</div> <!-- /.container -->

<div class="container">

    <iframe width="100%" height="500" frameborder="0" scrolling="no" src="{{ 'assets/hpe_map_traffic.html' | relative_url }}"></iframe>

</div> <!-- /.container -->

## Takeaways

* First map: no surprises, most entries are in Hyde Park/Kenwood; with a popular one being Lake Park & E Hyde Park; most exits are in the Loop
* Second map: Lake Park & 47th, Lake Park & East Hyde Park; remember being surprised that not many people exited State & Madison and the bubble reflects that
* Cut out stop on Payne & Cottage Grove ... right next to stop on Drexel Square & Cottage Grove 
