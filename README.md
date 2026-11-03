# Lab 7 - Interactive Map Visualization

Run from this folder:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

All four handout sections are implemented: Map Cosmetics, Map Visual Hierarchy, Choropleth Map, and Geo Projection. Controls rerender the maps; this follows the handout's Streamlit/Matplotlib interaction model. PNG and CSV downloads are included.

## Findings and methodology

- Cosmetics: sky-blue land and a light-grey background follow the example. Fill, background and boundary thickness can be changed.
- Visual hierarchy: the six requested countries are selected by default. Red highlights are distinct from neutral surrounding countries. Empty selection is supported.
- Choropleth: five sequential palettes support ordered density values. Linear density emphasizes the highest values; ln(1 + density) exposes variation among lower-density countries. The legend explicitly identifies the transformation.
- Projections: geographic, Equal Earth, Mollweide and Robinson views demonstrate differing shapes and areas. Equal Earth and Mollweide are equal-area projections; Robinson is a compromise projection.

The handout's lowercase population check would create random values despite the real POP_EST field. This implementation uses POP_EST and displays POP_YEAR. It also corrects density calculated in square degrees by measuring area in EPSG:8857 and converting square metres to square kilometres. Density remains constant when display projection changes. The missing projection_options dictionary is supplied.

Natural Earth generalized polygons provide approximate areas, particularly for small countries. Population estimates have source-specific years and are not current measurements. No random population is presented as real data.

## Dataset

Bundled shapefile and supporting files: ne_110m_admin_0_countries/.
Source: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/
Download: https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip
Natural Earth data are public domain. Retain the bundled source metadata.
