import unittest
import geopandas as gpd
from shapely.geometry import Point
import sys
import os

# Agregamos la ruta principal para importar el backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.spatial_module import SpatialProcessor

class TestSpatialModule(unittest.TestCase):
    def setUp(self):
        self.processor = SpatialProcessor()
        # Creamos un GeoDataFrame de prueba (ej. dos puntos geográficos)
        # EPSG:3857 es proyectado (para buffers en metros)
        data = {'name': ['Punto A', 'Punto B']}
        geometry = [Point(0, 0), Point(100, 100)]
        self.gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:3857")

    def test_calculate_buffer(self):
        buffered_gdf = self.processor.calculate_buffer(self.gdf, distance=50)
        
        # Verificamos que ahora sean polígonos (el buffer crea áreas)
        self.assertEqual(buffered_gdf.geometry.type.iloc[0], 'Polygon')
        self.assertEqual(len(buffered_gdf), 2)

    def test_get_summary_stats(self):
        stats = self.processor.get_summary_stats(self.gdf)
        
        self.assertEqual(stats['num_features'], 2)
        self.assertEqual(stats['crs'], 'EPSG:3857')

if __name__ == '__main__':
    unittest.main()
