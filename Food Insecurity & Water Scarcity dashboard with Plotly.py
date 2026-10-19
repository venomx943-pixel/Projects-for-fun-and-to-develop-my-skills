import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

np.random.seed(42)

countries = ["Country_A", "Country_B", "Country_C", "Country_D", "Country_E", "Country_F", "Country_G", "Country_H"]
regions = ["North", "South", "East", "West", "Central"]
n = 120

df = pd.DataFrame({
    "Country": np.random.choice(countries, n),
    "Region": np.random.choice(regions, n),
    "Year": np.random.choice([2023, 2024, 2025, 2026], n),
    "WaterScarcityIndex": np.random.uniform(10, 95, n),
    "FoodInsecurityRate": np.random.uniform(5, 60, n),
    "AgriculturalYield": np.random.uniform(1000, 50000, n),
    "FoodPriceInflation": np.random.uniform(-2, 45, n),
    "Population": np.random.randint(1000000, 150000000, n),
    "ISO": np.random.choice(["USA", "IND", "BRA", "EGY", "NGA", "KEN", "AUS", "CAN"], n)
})

fig1 = px.scatter(
    df, 
    x="WaterScarcityIndex", 
    y="FoodInsecurityRate", 
    size="Population", 
    color="Country", 
    hover_name="Region", 
    title="Water Scarcity vs Food Insecurity Analysis"
)

fig2 = px.bar(
    df.groupby("Country")["AgriculturalYield"].mean().reset_index(), 
    x="Country", 
    y="AgriculturalYield", 
    color="Country", 
    title="Average Agricultural Yield by Country"
)

fig3 = px.line(
    df.groupby(["Year", "Country"])["FoodPriceInflation"].mean().reset_index(), 
    x="Year", 
    y="FoodPriceInflation", 
    color="Country", 
    title="Food Price Inflation Trends Over Years"
)

fig4 = px.box(
    df, 
    x="Region", 
    y="WaterScarcityIndex", 
    color="Region", 
    notched=True, 
    title="Water Scarcity Distribution Across Regions"
)

fig5 = px.histogram(
    df, 
    x="FoodInsecurityRate", 
    nbins=25, 
    marginal="rug", 
    color="Country", 
    title="Food Insecurity Rate Distribution"
)

fig6 = px.pie(
    df.groupby("Country")["Population"].sum().reset_index(), 
    values="Population", 
    names="Country", 
    title="Population Share of Analyzed Countries", 
    hole=0.4
)

fig7 = px.density_contour(
    df, 
    x="WaterScarcityIndex", 
    y="FoodInsecurityRate", 
    color="Country", 
    title="Density Contour of Scarcity and Insecurity"
)

fig8 = px.scatter_3d(
    df, 
    x="WaterScarcityIndex", 
    y="FoodInsecurityRate", 
    z="AgriculturalYield", 
    color="Country", 
    size="Population", 
    title="3D Analysis of Scarcity, Insecurity and Yield"
)

fig9 = px.choropleth(
    df, 
    locations="ISO", 
    color="FoodInsecurityRate", 
    hover_name="Country", 
    color_continuous_scale=px.colors.sequential.Reds, 
    title="Global Food Insecurity Map"
)

sub_fig = make_subplots(
    rows=2, 
    cols=2, 
    subplot_titles=("Scarcity vs Yield", "Inflation Trends", "Yield Distribution", "Insecurity vs Scarcity")
)
sub_fig.add_trace(go.Scatter(x=df["WaterScarcityIndex"], y=df["AgriculturalYield"], mode="markers"), row=1, col=1)
sub_fig.add_trace(go.Bar(x=df["Country"], y=df["FoodPriceInflation"]), row=1, col=2)
sub_fig.add_trace(go.Box(y=df["AgriculturalYield"]), row=2, col=1)
sub_fig.add_trace(go.Scatter(x=df["WaterScarcityIndex"], y=df["FoodInsecurityRate"], mode="lines"), row=2, col=2)
sub_fig.update_layout(height=800, width=1000, title_text="Food and Water Crisis Dashboard")

indicator_fig = go.Figure(go.Indicator(
    mode="delta+number",
    value=df["FoodInsecurityRate"].mean(),
    delta={'reference': 25.0},
    title={"text": "Average Global Food Insecurity Rate"}
))

matrix_data = np.random.rand(5, 5)
fig_heat = px.imshow(
    matrix_data, 
    x=['W1', 'W2', 'W3', 'W4', 'W5'], 
    y=['R1', 'R2', 'R3', 'R4', 'R5'],
    text_auto=True,
    title="Water Resource Correlation Matrix"
)

fig1.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig6.show()
fig7.show()
fig8.show()
fig9.show()
sub_fig.show()
indicator_fig.show()
fig_heat.show()