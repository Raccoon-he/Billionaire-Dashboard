# Billionaire Dashboard - Reflection

### Usability

- Based on the feedback received, the dashboard is very easy to use and navigate from tab to tab.
- Some users requested more explanation on variable meaning, variable label and unit were updated to clarify.

### Reoccurring Themes

- Keeping the format consistent with the headers, colors, and spacing/layout to be visually aesthetic.
- Avoid using black background for the plots.

### Valuable Insights

- The header now updates dynamically based on the selected country – implemented in Tab 1.
- A "Select All Countries" option has been added for the map – implemented in Tab 1.
- Introduced filter dropboxes, allowing users to select specific countries and industries for detailed analysis - implemented in Tab 2.


### Tab 1 - Overlook

#### What has been done:

**Improvements from Milestone 2**
- Updated the background color to black for a more modern and visually appealing design.
- Enabled dynamic updates to the "Key Metric" column on the right when a user selects a country.
- Switched the map style to OpenStreetMap for more detailed and accurate geographical information.
- Added a fallback to global data: if a selected country has no billionaires, the map and key metrics will display global statistics.

**Improvements from Milestone 3**
- Introduced a "Back to Global" button, allowing users to effortlessly return to the global view with a single click.
- Implemented dynamic zoom level adjustments based on the area of the selected country, ensuring optimal visibility and clarity when focusing on specific regions.


### Tab 2 - More Info

#### What has been done:

**Improvements from Milestone 2**
- Divided the dashboard into two tabs, moving plots of demographics and industry insights to the second tab.
- Added filter dropboxes in Tab 2, allowing users to select specific countries and industries for the displayed plots. 
- Replaced the line chart with a scatter plot to better illustrate the wealth distribution across different ages.
- Added text labels for the top 3 industries in the pie chart.

**Improvements from Milestone 3**
- Established a fixed color scheme for industries in Tab 2 to ensure color consistency across visualizations and added a legend for clear representation.
- Implemented a stacked bar chart comparing male and female counts across age groups.
- Added a horizontal stacked bar chart showing the top 10 sources of wealth. 


### **Dashboard Performance Review**  

#### **Strengths** 

The **Billionaires Landscape Dashboard** effectively presents a comprehensive and visually engaging analysis of the global billionaire ecosystem. Its **interactive visualizations** enable users to explore **wealth distribution, industry dominance, and demographic trends** with ease. The **global heatmap** provides a clear snapshot of billionaire concentrations worldwide, while the **demographic and industry insights** tab offers deep dives into wealth sources, age distributions, and gender representation. Additionally, the integration of **customizable filters** enhances user engagement by allowing tailored data exploration based on country and industry preferences.  

#### **Improvements**  

While the dashboard delivers valuable insights, its **static nature** may limit its ability to reflect real-time billionaire data, which can change rapidly due to economic fluctuations and market dynamics. Incorporating **automated data updates** would improve the dashboard’s accuracy and relevance. Additionally, **predictive analytics and trend forecasting** could enhance its strategic value by offering insights into future wealth distribution patterns. Improving loading performance for complex visualizations and optimizing the user interface for better interactivity would further refine the user experience, ensuring seamless navigation and data interpretation.