---
layout: post
title: "Test Post"
---

In China, high school students seeking admission to domestic universities face the daunting
task of taking national college entrance examinations known as the *gaokao* (高考) at the end of their third years. Similar to the United States, there is significant heterogeneity in the location and quality of universities that *gaokao* students end up in. Using <a href="http://gklq.ntzx.cn/index.asp?jlh=4">*gaokao* results data</a> from Nantong High School (南通中学), a relatively selective high school in Jiangsu province, I present three maps that try to unpack some of this heterogeneity.[^1] These maps display the 138 different universities that the 855 *gaokao* examinees from Nantong High School in 2015 ultimately chose to attend.

[^1]: Data was scraped using the Beautiful Soup library in Python. Maps were produced using QGIS (with data acquired from OpenStreetMap) and the `tmap` package in R.

The first map below simply displays bubbles corresponding to the geographical locations of universities that students end up in. Each bubble corresponds to a single university; bubble sizes correspond to the number of graduating students attending that university. I argue that there are two major takeaways:


* **Most students choose to attend universities in major cities** (plotted in semi-transparent gray on the map). This can be seen in the large overlap between the purple bubbles and the points corresponding to cities. This is a slight difference from the United States, where prestigious universities may not necessarily be located in large metropolitan areas.

* **Most students choose to stay in their home province of Jiangsu, and/or home city of Nantong.** This makes sense especially in Jiangsu, since major cities such as Shanghai (上海) and Nanjing (南京) are home to many universities (including very prestigious ones).

<img class="feature-img" src="{{ 'assets/nantong_plot_bubbles.png' | relative_url }}" />

The previous map is slightly misleading due to the purple bubbles having high overlap within a city (eg in Beijing 北京 and Wuhan 武汉). A map that displays variation in the number of students attending colleges across the different provinces would solve this problem, as presented next.

<img class="feature-img" src="{{ 'assets/nantong_plot_provinces.png' | relative_url }}" />

This map adds two more layers to the story:


* **This high school seems to have strong university placement**. From the 855 students, there is a strong concentration of students who end up in Shanghai, Hubei, and Beijing. These locations are home to some of the best universities in China, such as Shanghai Jiaotong University (上海交通大学), Wuhan University (武汉大学), and Peking University (北京大学 or 北大 for short). Also, as noted previously, a large number of students do indeed choose to stay in Jiangsu.

* **There are provinces where no students chose to attend university in.** These seem to be mainly in the interior of China. Although I haven't explored the data, these provinces appear to be *poorer* and/or *ethnic minority* provinces relative to Jiangsu.

Finally, how prestigious are the universities that students are placing into? To answer this, I plot the number of students placing into "double first class" (双一流) universities across China. "Double first class" (hereafter, DFC) universities are elite universities <a href="https://en.wikipedia.org/wiki/Double_First_Class_University_Plan">specially designated by the Chinese government</a> in 2015 for funding and development through 2050.[^2] Therefore, DFC status is a good indicator of university prestige. The top map depicts DFC universities by geographical location and the number of students who chose to attend. The bottom map depicts the same for non-DFC universities.

[^2]: As of 2022, there are currently 147 universities designated as DFC. In coding DFC status, I only include main university campuses (and so exclude satellite campuses).

<img class="feature-img" src="{{ 'assets/nantong_plot_dfc.png' | relative_url }}" />  |

As seen from this panel,


* **Students staying in Jiangsu/Shanghai appear to be evenly split between between DFC and non-DFC schools.** This makes sense, given that these regions are both home to elite universities but also non-elite, more vocationally focused local universities. I suspect that this is the reason for this split.

* **Outside Jiangsu/Shanghai, many more students end up in DFC schools compared to non-DFC ones**. This reinforces the strength/competitiveness of Nantong High School in placing its graduates.

Overall, students from Nantong High School seem to have strong *gaokao* results both inside and outside Jiangsu. While students from Nantong High School and Jiangsu might not be representative of the "average" Chinese student, this mapping nevertheless provides a useful snapshot of where students end up after the *gaokao*.
