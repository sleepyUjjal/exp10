# Gapminder World Development Explorer

Interactive web application built with **Streamlit** and **Plotly** to explore, analyze, and visualize global health, economic, and demographic indicators across 142 countries from 1952 to 2007.

- **Live Public URL**: *Deploying on Streamlit Community Cloud (e.g. `https://gapminder-world-explorer.streamlit.app`)*
- **GitHub Repository**: [https://github.com/sleepyUjjal/exp10](https://github.com/sleepyUjjal/exp10)

---

## 🌟 Key Features

1. **Global Sidebar Filters**:
   - Multi-select continents with auto-fallback to preserve context.
   - Snapshot year slider (1952 – 2007, 5-year intervals).
   - Real-time country text search.

2. **Executive KPI Cards**:
   - Dynamically calculates: Total Countries represented, Average Life Expectancy (with change relative to 1952 baseline), Combined Population, and Median GDP per capita.
   - Styled using modern design tokens (taste-skill *framed-sheet* system).

3. **Interactive Visualizations**:
   - **Health vs. Wealth Bubble Chart**: GDP per Capita (log scale) vs. Life Expectancy with bubble radius proportional to population and continent color mapping, augmented with dynamic median and average reference lines.
   - **Longitudinal Trend Lines**: Compare multi-country trajectories over 55 years across any chosen metric, featuring pre-configured presets (e.g., East Asian Tigers, Major Health Shocks).
   - **Top-N Rankings**: Interactive horizontal bar chart ranking the top or bottom N countries for any year and indicator.
   - **Head-to-Head Comparison (Bonus)**: Contrast two countries side-by-side across Life Expectancy, GDP per Capita, and Population simultaneously.
   - **Animated Bubble World (Bonus)**: Hans Rosling-style animated bubble chart tracking human development over time with play/pause controls.
   - **Data Explorer & Export**: Sortable data table with one-click `.csv` export.

---

## 🛠️ Local Setup & Running

1. **Activate your environment**:
   ```bash
   source ../env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment Instructions (Streamlit Community Cloud)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Build Gapminder Streamlit Web App for Exp 10"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New app"**.
4. Select your repository: `sleepyUjjal/exp10`, branch: `main`, and main file path: `app.py`.
5. Click **"Deploy!"**. Within minutes, your app will be live at a public URL.

---

## 📝 Answers to Exploration Questions

### Q1: Which continent gained the most life expectancy between 1952 and 2007?
- **Asia** gained the most life expectancy:
  - **1952 Average**: 46.31 years
  - **2007 Average**: 70.73 years
  - **Net Gain**: **+24.41 years**
- *Americas* followed in second place (+20.33 yrs: 53.28 → 73.61), followed by *Africa* (+15.67 yrs), *Europe* (+13.24 yrs), and *Oceania* (+11.46 yrs).

### Q2: Is there a relationship between GDP per capita and life expectancy? Does it hold for every continent?
- **Yes**, there is a strong positive non-linear (logarithmic) relationship: as GDP per capita rises, life expectancy increases steeply at low income levels and plateaus beyond ~$10,000–$15,000 USD/capita (the Preston Curve).
- **Does it hold for every continent?**
  - **Generally yes**, the upward curve holds within Europe, Americas, Asia, and Oceania.
  - **Exceptions & Disparities**: In Africa, several mineral/oil-rich nations (e.g., Gabon, Equatorial Guinea, South Africa) exhibit high GDP per capita but significantly suppressed life expectancies due to systemic health crises (e.g., HIV/AIDS epidemic) and high wealth concentration.

### Q3: Which countries saw life expectancy fall at some point? In which period?
Across the 142 countries, 52 experienced at least one 5-year period of falling life expectancy. Notable historical declines include:
1. **Rwanda (1987 → 1992)**: Dropped from 44.02 to 23.60 years (**-20.42 years**) due to civil war and the Rwandan Genocide.
2. **Zimbabwe (1992 → 1997 & 1997 → 2002)**: Fell from 60.38 to 46.81 years (**-13.57 years**) and then further to 39.99 years due to the HIV/AIDS epidemic and economic collapse.
3. **Cambodia (1972 → 1977)**: Dropped from 40.32 to 31.22 years (**-9.10 years**) during the Khmer Rouge regime.
4. **China (1957 → 1962)**: Dropped from 50.55 to 44.50 years (**-6.05 years**) during the Great Leap Forward and subsequent famine.
5. **Southern African Nations (1990s–2000s)**: Botswana, Lesotho, Swaziland, and Namibia suffered 7–11 year drops primarily driven by HIV/AIDS.

### Q4: Which were the 10 most populous countries in 1952, and in 2007? What changed?
- **1952 Top 10**:
  1. China (556.3M)
  2. India (372.0M)
  3. United States (157.6M)
  4. Japan (86.5M)
  5. Indonesia (82.1M)
  6. Germany (69.1M)
  7. Brazil (56.6M)
  8. United Kingdom (50.4M)
  9. Italy (47.7M)
  10. Bangladesh (46.9M)

- **2007 Top 10**:
  1. China (1,318.7M)
  2. India (1,110.4M)
  3. United States (301.1M)
  4. Indonesia (223.5M)
  5. Brazil (190.0M)
  6. Pakistan (169.3M)
  7. Bangladesh (150.4M)
  8. Nigeria (135.0M)
  9. Japan (127.5M)
  10. Mexico (108.7M)

- **What Changed?**
  - European nations (**Germany, UK, Italy**) dropped out of the top 10 due to slower demographic growth and demographic transition.
  - Rapidly developing high-fertility nations entered the top 10: **Pakistan, Nigeria, and Mexico**.
  - Indonesia and Brazil moved up to 4th and 5th position respectively, while Japan dropped from 4th to 9th.

### Q5: How does India compare with China, or any two countries, on all three metrics over time?
Using the **Head-to-Head Comparison** tab:
- **Life Expectancy**: Both started in 1952 at very low life expectancy (India: 37.4 yrs, China: 44.0 yrs). China experienced a sharp drop in 1957–1962 (to 44.5 yrs), followed by an extraordinary rise in the 1960s–1970s reaching 72.96 yrs by 2007. India saw steady, uninterrupted progress from 37.4 yrs to 64.7 yrs by 2007, maintaining an ~8-year gap behind China.
- **GDP per Capita**: India and China had almost identical GDP per capita from 1952 through 1977 (~$550–$1,000 USD). Starting in the late 1970s following Chinese economic reforms, China's GDP per capita accelerated rapidly, reaching $4,959 by 2007, compared to India's $2,452.
- **Population**: China led throughout (556M in 1952 to 1.32B in 2007; 2.37× growth), but India's population grew faster without a one-child policy (372M to 1.11B; 2.98× growth), narrowing the gap.

### Q6: Which countries had high GDP per capita but below-average life expectancy in a given year?
Examining countries with above-median GDP per capita but below-average life expectancy:
- **In 1952** (Median GDP: $1,968.5, Avg Life Exp: 49.1 yrs):
  - *Countries*: Algeria, Angola, Bolivia, Gabon, Iran, Iraq, Libya, Saudi Arabia, South Africa.
  - *Driver*: Early resource/oil revenues alongside underdeveloped healthcare infrastructure.
- **In 1977** (Median GDP: $3,798.6, Avg Life Exp: 59.6 yrs):
  - *Countries*: Algeria, Gabon, Iran, Libya, Oman, Saudi Arabia, South Africa.
- **In 2007** (Median GDP: $6,124.4, Avg Life Exp: 67.0 yrs):
  - *Countries*: **Botswana, Equatorial Guinea, Gabon, South Africa**.
  - *Driver*: Equatorial Guinea and Gabon derived significant wealth from oil, while Botswana and South Africa maintained upper-middle-income status from diamonds and mining, yet both suffered severely reduced life expectancy (~52–54 yrs) from the HIV/AIDS epidemic.
