# DATA 551 Project Proposal: Billionaire Landscape Exploring

Huan He, Qijia Zheng, Yuzhu Han

### Motivation and Purpose

**Our role**: Research team at an educational institution focused on career development and success studies.

**Target audience**: Students, career counselors, and aspiring professionals
Understanding the pathways to success and the factors that contribute to achieving extraordinary wealth can inspire and guide individuals in their career and personal development. To address this, we propose building a data visualization dashboard that explores the Billionaires Statistics Dataset (2023). The dashboard will allow our target audience to analyze the demographics, industries, and geographic distribution of billionaires. By visualizing trends such as age, gender, industry dominance, and country, our dashboard will empower users to identify patterns of success, explore potential career paths, and gain insights into the global landscape of achievement.


### Description of the Data

We will visualize the Billionaires Statistics Dataset (2023), which offers a comprehensive view of the global billionaire landscape, encompassing their wealth, industries, and demographic details. The dataset consists of approximately 2,650 entries, each representing a billionaire, with 7 key variables capturing their personal and professional attributes. These variables include the billionaire's name (`personName`), age (`age`), gender (`gender`), net worth in U.S. dollars (`finalWorth`), the source of their wealth (`source`), country of residence (`country`), and the industries associated with their business ventures (`industries`).

Among these variables:
- `personName` and `source` are **string (text) type** variables, representing the billionaire's full name and the origin of their wealth, respectively.
- `age` and `finalWorth` are **numeric** variables, with age being a discrete integer and finalWorth a continuous value indicating their net worth.
- `gender`, `country`, and `industries` are **categorical** variables, capturing demographic details such as gender identity, geographic location, and the sectors tied to their business activities.



### Research Questions and Usage Scenarios

**User Story:**

Alex is a 22-year-old business student who dreams of becoming a successful entrepreneur. Alex wants to explore the Billionaires Statistics Dataset to learn which industries and regions produce the most billionaires and understand the factors that lead to extraordinary success.

When Alex opens the "Billionaires Success Insights" dashboard, they see an overview of the data, including the most common industries and the average age of billionaires. Alex filters the data to focus on the tech industry and notices that many tech billionaires are based in the U.S. and achieved significant wealth in their 30s and 40s.

Using the interactive map, Alex visualizes the geographic distribution of tech billionaires and sees hotspots like Silicon Valley. Alex also compares net worth across industries and discovers that tech billionaires tend to accumulate wealth faster than those in traditional industries like manufacturing.</n>
By exploring the dashboard, Alex gains confidence in pursuing a career in tech and starts looking for internship opportunities in startups. This simplified user story highlights how the dashboard helps Alex make informed decisions about their career path.

**Research Questions**:
- What industries have produced the most billionaires, and how do these industries vary by geographic region?
- What demographic trends (e.g., age, gender) are associated with extraordinary wealth accumulation?
- How does the net worth of billionaires vary across different industries and countries?
- What are the most common sources of wealth among billionaires, and how have these trends evolved over time?

These research questions guide the design of the dashboard, ensuring that it provides actionable insights for users like Alex. By addressing these questions, the dashboard will empower students, career counselors, and aspiring professionals to make informed decisions about their career paths and personal development.
