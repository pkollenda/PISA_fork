import geopandas as gpd
import pytest
from shapely.geometry import MultiPolygon, Polygon

from gpbp.layers import AdmArea


@pytest.fixture
def mock_country_gdf() -> gpd.GeoDataFrame:
    """Create a level=0 administrative area (country) GeoDataFrame"""
    # Create two simple square polygons
    polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    polygon2 = Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])

    # Combine them into a MultiPolygon
    multipolygon = MultiPolygon([polygon1, polygon2])

    data = {
        'id': [0],
        'COUNTRY': ["Mock Country"],
        'geometry': [multipolygon],
    }

    gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')

    return gdf

@pytest.fixture
def mock_region_gdf():
    """Create a level=1 administrative area (region) GeoDataFrame"""
    # Create two simple square polygons
    polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    polygon2 = Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])

    # Combine them into a MultiPolygon
    multipolygon = MultiPolygon([polygon1, polygon2])

    data = {
        'id': [0, 1],
        'COUNTRY': ["Mock Country", "Mock Country"],
        'NAME_1': ["Mock Region 1", "Mock Region 2"],
        'geometry': [multipolygon, multipolygon],
    }

    gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')

    return gdf

class TestAdmAreaGetCountryData:
    def test_get_country_data_level_0(self, mocker, mock_country_gdf):
        mocker.patch("layers.GADMDownloader.get_shape_data_by_country_name", return_value=mock_country_gdf)
        adm_area = AdmArea(country="Timor-Leste", level=0)

        assert type(adm_area.geometry) is MultiPolygon
        assert adm_area.adm_name == "Timor-Leste"

    def test_get_country_data_level_1(self, mocker, mock_region_gdf, capsys):
        mocker.patch("layers.GADMDownloader.get_shape_data_by_country_name", return_value=mock_region_gdf)
        AdmArea(country="Timor-Leste", level=1)

        printed_output = capsys.readouterr().out.strip().split('\n')
        for line_nr, line in enumerate(printed_output):
            if line.startswith("Administrative areas for level "):
                assert printed_output[line_nr + 1] == "['Mock Region 1' 'Mock Region 2']"
                break
