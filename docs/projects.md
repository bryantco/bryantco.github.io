---
layout: page
title: Projects
permalink: /projects/
--- 
# Trends in Chinese Primary School Enrollment, 2000-2019
This quick graph was made for my final paper in PLSC 42701: Seminar in Chinese Politics (Winter 2022).
<div class="image">
	<img src="{{ 'assets/education_plot.png' | relative_url }}" height="auto" width="500%"/>
</div>

# Minority Languages Data Visualization
Below is a mini-data visualization of "politically relevant" minority languages across the world. I collected this data for my thesis. <br> <br>
The coding rules that I used to determine the "politically relevant" minority languages in a country can be found
<a href="{{ 'assets/minlang-coderules.pdf' | relative_url}}" target="_blank">here</a>.
<div class="container">

    <iframe width="100%" height="450" frameborder="0" scrolling="no" src="{{ 'mapsite.html' | relative_url }}"></iframe>

</div> <!-- /.container -->

Here is another map that depicts the countries where legal protections for minority languages are likely to be lower in 
2022, as compared to 2017. Hover over the colored countries to get the predicted probability that such linguistic backsliding
will take place. <br>

I'm personally skeptical of some of these predictions though; my procedure didn't allow me to calculate standard errors/confidence intervals
for the predicted probabilities. 

<div class="container">

    <iframe width="100%" height="450" frameborder="0" scrolling="no" src="{{ 'riskmap.html' | relative_url }}"></iframe>

</div> <!-- /.container -->