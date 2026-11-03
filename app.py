from pathlib import Path
import io
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

ROOT = Path(__file__).resolve().parent
PROJECTIONS = {'Plate Carree (geographic)': 'EPSG:4326', 'Equal Earth': 'EPSG:8857', 'Mollweide': '+proj=moll +datum=WGS84 +units=m +no_defs', 'Robinson': '+proj=robin +datum=WGS84 +units=m +no_defs'}

@st.cache_data
def load_data():
    gdf = gpd.read_file(ROOT / 'natural_earth.zip')
    gdf['country'] = gdf['NAME']
    gdf['population'] = gdf['POP_EST'].where(gdf['POP_EST'] >= 0)
    # Equal-area projection gives square metres, converted to square kilometres.
    gdf['area_km2'] = gdf.to_crs('EPSG:8857').area / 1_000_000
    gdf['density'] = gdf['population'] / gdf['area_km2'].where(gdf['area_km2'] > 0)
    return gdf

st.set_page_config(page_title='Lab 7 | World Maps', page_icon='🌍', layout='wide')
st.title('World Maps | Lab 7')
st.markdown('Name: Abdullah Fouzi Saleh Ahmed Naji  \nID: 22012364  \nLab: 7')
gdf = load_data()
mode = st.sidebar.radio('Select Map Type', ['Map Cosmetics', 'Map Visual Hierarchy', 'Choropleth Map', 'Geo Projection'])
st.sidebar.caption('Source: Natural Earth, 1:110m cultural vectors. Population estimates reflect the source dataset, not a live census.')
st.subheader(mode)
fig, ax = plt.subplots(figsize=(13, 6.5))
fig.patch.set_facecolor('#f8fafc')
ax.set_facecolor('lightgrey')
if mode == 'Map Cosmetics':
    fill = st.color_picker('Country fill', '#87CEEB')
    ocean = st.color_picker('Background', '#D3D3D3')
    width = st.slider('Boundary width', 0.0, 1.5, 0.5, 0.1)
    ax.set_facecolor(ocean)
    gdf.plot(ax=ax, color=fill, edgecolor='black', linewidth=width)
    title = 'Styled world map'
    st.write('Country fill, boundaries and background control contrast and visual separation.')
elif mode == 'Map Visual Hierarchy':
    selected = st.multiselect('Select countries to highlight in red', sorted(gdf.country), default=['Brazil', 'India', 'China', 'Australia', 'South Africa', 'Russia'])
    gdf.plot(ax=ax, color=np.where(gdf.country.isin(selected), '#dc2626', '#cbd5e1'), edgecolor='white', linewidth=0.5)
    title = f'Visual hierarchy | {len(selected)} countries highlighted'
    st.write('Red draws attention to the selected countries; the neutral background preserves geographic context.')
else:
    projection = st.selectbox('Select a Projection', list(PROJECTIONS), index=1) if mode == 'Geo Projection' else 'Plate Carree (geographic)'
    palette = st.selectbox('Choose Color Scheme', ['OrRd', 'YlGn', 'Blues', 'Purples', 'Greens'])
    log = st.checkbox('Use Log Transformation', value=True)
    plotted = gdf.copy()
    plotted['value'] = np.log1p(plotted.density) if log else plotted.density
    label = 'ln(1 + density), density in people/km²' if log else 'Population density (people/km²)'
    plotted.to_crs(PROJECTIONS[projection]).plot(column='value', cmap=palette, ax=ax, edgecolor='#64748b', linewidth=0.3, legend=True, legend_kwds={'label': label, 'shrink': 0.65}, missing_kwds={'color': '#d1d5db', 'label': 'No data'})
    title = f'Population density | {projection}'
    st.write('Log transformation reduces the influence of extreme densities. Area is calculated once in Equal Earth, so changing the display projection does not change density.')
    if mode == 'Geo Projection':
        st.info('Equal Earth and Mollweide preserve relative area. Robinson balances shape and area distortion. Geographic coordinates stretch high latitudes; no flat world map preserves every property.')
ax.set_title(title, fontsize=16, fontweight='bold', pad=16)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
fig.tight_layout()
st.pyplot(fig)
buffer = io.BytesIO()
fig.savefig(buffer, format='png', dpi=180, bbox_inches='tight')
st.download_button('Download map image', buffer.getvalue(), 'lab7_map.png', 'image/png')
plt.close(fig)
with st.expander('Data and methodology'):
    st.write('Density uses population estimates divided by equal-area polygon area. Coastlines are generalized at 1:110m, so small-country densities are approximate. Antarctica is included as represented in the source. Borders and names follow Natural Earth.')
    st.dataframe(gdf[['country', 'population', 'POP_YEAR', 'area_km2', 'density']].rename(columns={'POP_YEAR': 'population_year'}), hide_index=True)
    st.download_button('Download data', gdf[['country', 'population', 'area_km2', 'density']].to_csv(index=False), 'lab7_density.csv', 'text/csv')


