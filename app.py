import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gapminder World Development Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling following taste-skill "framed-sheet" design system
# Palette: Ground #f9fbfc, Surface #ffffff, Border #e8eaec, Accent #1b6c80, Text #131416
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* App background */
    .stApp {
        background-color: #f9fbfc;
        color: #131416;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e8eaec;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        border-color: #1b6c80;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #5d5f60;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 600;
        color: #131416;
        font-family: 'IBM Plex Sans', sans-serif;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 11px;
        color: #8c8f92;
        margin-top: 4px;
    }

    /* Section Headers */
    .section-title {
        font-size: 17px;
        font-weight: 600;
        color: #131416;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    .section-subtitle {
        font-size: 13px;
        color: #5d5f60;
        margin-bottom: 16px;
    }
    
    /* Insight pill */
    .insight-box {
        background-color: #ffffff;
        border-left: 3px solid #1b6c80;
        border-top: 1px solid #e8eaec;
        border-right: 1px solid #e8eaec;
        border-bottom: 1px solid #e8eaec;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 10px 0 20px 0;
        font-size: 13px;
        color: #353736;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("exp10_gapminder.csv")
    df['year'] = df['year'].astype(int)
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading dataset `exp10_gapminder.csv`: {e}")
    st.stop()

# Consistent continent colors
CONTINENT_COLORS = {
    'Asia': '#1b6c80',       # Primary teal
    'Europe': '#2f70bb',     # Blue
    'Africa': '#a86f0c',     # Amber
    'Americas': '#1e7b4f',   # Forest green
    'Oceania': '#c4242a'     # Crimson
}

all_continents = sorted(df_raw['continent'].unique().tolist())
all_years = sorted(df_raw['year'].unique().tolist())
all_countries = sorted(df_raw['country'].unique().tolist())

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🌍 Global Filters")
st.sidebar.markdown("<p style='font-size: 12px; color: #5d5f60;'>Control data slice across all sections</p>", unsafe_allow_html=True)

selected_continents = st.sidebar.multiselect(
    "Continents",
    options=all_continents,
    default=all_continents,
    help="Filter countries belonging to specific continents"
)

# Robust fallback if empty
if not selected_continents:
    selected_continents = all_continents
    st.sidebar.caption("*(Showing all continents)*")

selected_year = st.sidebar.select_slider(
    "Snapshot Year",
    options=all_years,
    value=2007,
    help="Target year for KPIs, Bubble Chart, and Top-N Ranking"
)

country_search = st.sidebar.text_input(
    "Search Country",
    value="",
    placeholder="e.g. India, Brazil, Japan...",
    help="Filter records matching country name"
).strip()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Dataset Scope")
st.sidebar.markdown(f"""
- **Total Countries:** 142
- **Time Range:** 1952 – 2007 (5-yr steps)
- **Observations:** 1,704 rows
- **Source:** Gapminder Foundation
""")

# -----------------------------------------------------------------------------
# 4. FILTERED DATASETS
# -----------------------------------------------------------------------------
# Global continent filter
df_cont_filtered = df_raw[df_raw['continent'].isin(selected_continents)]

# Search filter
if country_search:
    df_filtered_all_years = df_cont_filtered[df_cont_filtered['country'].str.contains(country_search, case=False, na=False)]
else:
    df_filtered_all_years = df_cont_filtered

# Year snapshot
df_snapshot = df_filtered_all_years[df_filtered_all_years['year'] == selected_year]

# -----------------------------------------------------------------------------
# 5. HEADER & TOP BANNER
# -----------------------------------------------------------------------------
st.title("Gapminder World Development Explorer")
st.markdown(
    "An interactive visual workspace tracking **Life Expectancy**, **GDP per Capita**, and **Population** "
    "across 142 countries from **1952 to 2007**."
)

# -----------------------------------------------------------------------------
# 6. KPI METRIC CARDS
# -----------------------------------------------------------------------------
num_countries = df_snapshot['country'].nunique()
avg_life_exp = df_snapshot['lifeExp'].mean() if num_countries > 0 else 0
total_pop = df_snapshot['pop'].sum() if num_countries > 0 else 0
median_gdp = df_snapshot['gdpPercap'].median() if num_countries > 0 else 0

# Benchmark comparison against baseline year 1952 for the same filter
df_base = df_filtered_all_years[df_filtered_all_years['year'] == 1952]
base_avg_life = df_base['lifeExp'].mean() if len(df_base) > 0 else avg_life_exp
delta_life = avg_life_exp - base_avg_life

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Countries Represented</div>
        <div class="kpi-value">{num_countries:,}</div>
        <div class="kpi-sub">in {len(selected_continents)} selected continent(s)</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    sign = "+" if delta_life >= 0 else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Life Expectancy</div>
        <div class="kpi-value">{avg_life_exp:.1f} <span style="font-size:16px; font-weight:400; color:#5d5f60;">yrs</span></div>
        <div class="kpi-sub">{sign}{delta_life:.1f} yrs vs. 1952 baseline</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    if total_pop >= 1e9:
        pop_str = f"{total_pop / 1e9:.2f} Billion"
    elif total_pop >= 1e6:
        pop_str = f"{total_pop / 1e6:.1f} Million"
    else:
        pop_str = f"{total_pop:,}"
        
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Population</div>
        <div class="kpi-value">{pop_str}</div>
        <div class="kpi-sub">Combined selected region</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Median GDP per Capita</div>
        <div class="kpi-value">${median_gdp:,.0f}</div>
        <div class="kpi-sub">Inflation-adjusted US dollars</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_overview, tab_trends, tab_ranking, tab_compare, tab_animation, tab_data = st.tabs([
    "📊 Overview & Correlation",
    "📈 Multi-Country Trends",
    "🏆 Top-N Rankings",
    "⚖️ Head-to-Head Comparison",
    "🎬 Animated Bubble World",
    "📋 Data Explorer & Export"
])

# -----------------------------------------------------------------------------
# TAB 1: OVERVIEW & BUBBLE CHART
# -----------------------------------------------------------------------------
with tab_overview:
    st.markdown(f"<div class='section-title'>Health vs. Wealth ({selected_year})</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='section-subtitle'>Relationship between GDP per Capita (log scale) and Life Expectancy. "
        f"Bubble radius corresponds to country population.</div>",
        unsafe_allow_html=True
    )
    
    if df_snapshot.empty:
        st.warning("No data found for the current filter criteria.")
    else:
        fig_bubble = px.scatter(
            df_snapshot,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            color_discrete_map=CONTINENT_COLORS,
            hover_name="country",
            hover_data={
                "gdpPercap": ":$,.0f",
                "lifeExp": ":.1f",
                "pop": ":,",
                "continent": True
            },
            size_max=50,
            log_x=True,
            labels={
                "gdpPercap": "GDP per Capita (USD, Log Scale)",
                "lifeExp": "Life Expectancy (Years)",
                "pop": "Population",
                "continent": "Continent"
            }
        )
        
        # Add benchmark lines
        fig_bubble.add_hline(
            y=avg_life_exp,
            line_dash="dot",
            line_color="#5d5f60",
            annotation_text=f"Avg Life Exp: {avg_life_exp:.1f}y",
            annotation_position="bottom right"
        )
        fig_bubble.add_vline(
            x=median_gdp,
            line_dash="dot",
            line_color="#5d5f60",
            annotation_text=f"Median GDP: ${median_gdp:,.0f}",
            annotation_position="top left"
        )
        
        fig_bubble.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=20, b=40),
            height=540,
            font=dict(family="IBM Plex Sans, sans-serif"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        
        # High GDP but Below Average Life Expectancy Outliers
        outliers = df_snapshot[(df_snapshot['gdpPercap'] > median_gdp) & (df_snapshot['lifeExp'] < avg_life_exp)]
        if not outliers.empty:
            outlier_names = ", ".join(outliers['country'].sort_values().tolist())
            st.markdown(f"""
            <div class="insight-box">
                <strong>Notable Outliers ({selected_year}):</strong> Countries with above-median GDP per capita but below-average life expectancy: 
                <strong>{outlier_names}</strong>. This often reflects income concentration from mineral/oil wealth alongside healthcare disparities or epidemics (such as HIV/AIDS impact in southern Africa).
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: MULTI-COUNTRY TREND LINES
# -----------------------------------------------------------------------------
with tab_trends:
    st.markdown("<div class='section-title'>Longitudinal Trend Explorer (1952–2007)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Analyze how key metrics evolved over 55 years across selected countries.</div>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t2:
        metric_choice = st.selectbox(
            "Select Metric",
            options=["lifeExp", "gdpPercap", "pop"],
            format_func=lambda x: {
                "lifeExp": "Life Expectancy (years)",
                "gdpPercap": "GDP per Capita (USD)",
                "pop": "Total Population"
            }[x]
        )
        
        # Suggested presets
        preset = st.radio(
            "Quick Presets",
            options=["Custom", "BRICS Highlights", "East Asian Tigers", "Major Declines (Health Shocks)"],
            index=0
        )
    
    with col_t1:
        if preset == "BRICS Highlights":
            default_countries = [c for c in ["Brazil", "China", "India", "South Africa"] if c in df_cont_filtered['country'].unique()]
        elif preset == "East Asian Tigers":
            default_countries = [c for c in ["Japan", "Korea, Rep.", "Singapore", "Hong Kong, China"] if c in df_cont_filtered['country'].unique()]
        elif preset == "Major Declines (Health Shocks)":
            default_countries = [c for c in ["Rwanda", "Cambodia", "Zimbabwe", "Botswana", "China"] if c in df_cont_filtered['country'].unique()]
        else:
            default_countries = [c for c in ["India", "China", "United States", "Rwanda"] if c in df_cont_filtered['country'].unique()]
            
        selected_trend_countries = st.multiselect(
            "Choose Countries to Plot",
            options=sorted(df_cont_filtered['country'].unique()),
            default=default_countries
        )
    
    if not selected_trend_countries:
        st.info("Select at least one country to view longitudinal trends.")
    else:
        df_trends = df_cont_filtered[df_cont_filtered['country'].isin(selected_trend_countries)]
        
        metric_labels = {
            "lifeExp": "Life Expectancy (Years)",
            "gdpPercap": "GDP per Capita (Inflation-Adjusted USD)",
            "pop": "Total Population"
        }
        
        fig_trend = px.line(
            df_trends,
            x="year",
            y=metric_choice,
            color="country",
            markers=True,
            labels={"year": "Year", metric_choice: metric_labels[metric_choice], "country": "Country"},
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        
        fig_trend.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=20, b=40),
            height=500,
            font=dict(family="IBM Plex Sans, sans-serif"),
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: TOP-N RANKINGS
# -----------------------------------------------------------------------------
with tab_ranking:
    st.markdown(f"<div class='section-title'>Top & Bottom Performers in {selected_year}</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Rank countries across continents by selected development indicators.</div>", unsafe_allow_html=True)
    
    r_c1, r_c2, r_c3 = st.columns([2, 1, 1])
    with r_c1:
        rank_metric = st.selectbox(
            "Ranking Indicator",
            options=["lifeExp", "gdpPercap", "pop"],
            format_func=lambda x: {
                "lifeExp": "Life Expectancy (Years)",
                "gdpPercap": "GDP per Capita (USD)",
                "pop": "Population"
            }[x],
            key="rank_metric"
        )
    with r_c2:
        top_n = st.slider("Number of Countries (N)", min_value=5, max_value=30, value=10, step=5)
    with r_c3:
        sort_order = st.radio("Order", options=["Top Highest", "Bottom Lowest"], horizontal=True)
    
    ascending = (sort_order == "Bottom Lowest")
    df_ranked = df_snapshot.sort_values(by=rank_metric, ascending=ascending).head(top_n)
    
    if df_ranked.empty:
        st.warning("No data available for ranking with current filter selection.")
    else:
        # Plot horizontal bar chart
        fig_bar = px.bar(
            df_ranked.sort_values(by=rank_metric, ascending=not ascending),
            x=rank_metric,
            y="country",
            orientation="h",
            color="continent",
            color_discrete_map=CONTINENT_COLORS,
            text_auto=True if rank_metric == "lifeExp" else False,
            labels={
                rank_metric: metric_labels[rank_metric],
                "country": "Country",
                "continent": "Continent"
            }
        )
        
        fig_bar.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=20, b=40),
            height=max(380, top_n * 28),
            font=dict(family="IBM Plex Sans, sans-serif")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: HEAD-TO-HEAD COMPARISON (BONUS FEATURE)
# -----------------------------------------------------------------------------
with tab_compare:
    st.markdown("<div class='section-title'>Two-Country Head-to-Head Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Directly contrast two nations across all health, economic, and demographic dimensions.</div>", unsafe_allow_html=True)
    
    cmp1, cmp2 = st.columns(2)
    with cmp1:
        country_a = st.selectbox("Country A", options=all_countries, index=all_countries.index("India") if "India" in all_countries else 0)
    with cmp2:
        country_b = st.selectbox("Country B", options=all_countries, index=all_countries.index("China") if "China" in all_countries else 1)
        
    df_a = df_raw[df_raw['country'] == country_a].sort_values('year')
    df_b = df_raw[df_raw['country'] == country_b].sort_values('year')
    df_compare = pd.concat([df_a, df_b])
    
    c_col1, c_col2, c_col3 = st.columns(3)
    
    with c_col1:
        fig_c1 = px.line(
            df_compare, x="year", y="lifeExp", color="country", markers=True,
            title="Life Expectancy (Years)",
            color_discrete_sequence=["#1b6c80", "#a86f0c"]
        )
        fig_c1.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=320)
        st.plotly_chart(fig_c1, use_container_width=True)
        
    with c_col2:
        fig_c2 = px.line(
            df_compare, x="year", y="gdpPercap", color="country", markers=True,
            title="GDP per Capita (USD)",
            color_discrete_sequence=["#1b6c80", "#a86f0c"]
        )
        fig_c2.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=320)
        st.plotly_chart(fig_c2, use_container_width=True)
        
    with c_col3:
        fig_c3 = px.line(
            df_compare, x="year", y="pop", color="country", markers=True,
            title="Total Population",
            color_discrete_sequence=["#1b6c80", "#a86f0c"]
        )
        fig_c3.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=320)
        st.plotly_chart(fig_c3, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: ANIMATED BUBBLE CHART (BONUS FEATURE)
# -----------------------------------------------------------------------------
with tab_animation:
    st.markdown("<div class='section-title'>Hans Rosling Animated Bubble Simulation (1952–2007)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Hit the Play button to watch half a century of global human development unfold.</div>", unsafe_allow_html=True)
    
    fig_anim = px.scatter(
        df_cont_filtered,
        x="gdpPercap",
        y="lifeExp",
        animation_frame="year",
        animation_group="country",
        size="pop",
        color="continent",
        hover_name="country",
        color_discrete_map=CONTINENT_COLORS,
        log_x=True,
        size_max=55,
        range_x=[150, 120000],
        range_y=[20, 90],
        labels={
            "gdpPercap": "GDP per Capita (USD, Log Scale)",
            "lifeExp": "Life Expectancy (Years)",
            "pop": "Population",
            "continent": "Continent"
        }
    )
    
    fig_anim.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=40),
        height=580,
        font=dict(family="IBM Plex Sans, sans-serif")
    )
    st.plotly_chart(fig_anim, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 6: DATA EXPLORER & CSV DOWNLOAD
# -----------------------------------------------------------------------------
with tab_data:
    st.markdown("<div class='section-title'>Filtered Raw Data Explorer</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>Inspecting {len(df_filtered_all_years):,} records matching active continent and search parameters.</div>", unsafe_allow_html=True)
    
    # Download Button
    csv_bytes = df_filtered_all_years.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (.CSV)",
        data=csv_bytes,
        file_name=f"gapminder_export_{selected_year}.csv",
        mime="text/csv",
        help="Export current tabular selection as CSV"
    )
    
    st.dataframe(
        df_filtered_all_years.style.format({
            "lifeExp": "{:.2f}",
            "gdpPercap": "${:,.2f}",
            "pop": "{:,}"
        }),
        use_container_width=True,
        height=450
    )

# -----------------------------------------------------------------------------
# 8. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: #5d5f60;'>"
    "Data Source: Gapminder Foundation (gapminder.org) · CSSE301 Data Science Lab Experiment 10 · Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True
)
