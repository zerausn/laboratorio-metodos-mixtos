import geopandas as gpd
import pandas as pd

class SpatialProcessor:
    def __init__(self):
        """Inicializa el módulo de análisis espacial."""
        pass

    def load_vector_data(self, filepath):
        """Carga un archivo vectorial (Shapefile, GeoJSON) usando GeoPandas."""
        try:
            gdf = gpd.read_file(filepath)
            return gdf
        except Exception as e:
            raise ValueError(f"Error al cargar la capa espacial: {str(e)}")

    def calculate_buffer(self, gdf, distance):
        """Calcula áreas de influencia (buffers) a una distancia dada."""
        # Nota: Es crucial que el GeoDataFrame esté en un CRS proyectado (metros/pies)
        # y no geográfico (lat/lon) para calcular buffers en unidades métricas.
        if gdf.crs and gdf.crs.is_geographic:
            print("Advertencia: El CRS es geográfico. El buffer se calculará en grados.")
            
        buffered_gdf = gdf.copy()
        buffered_gdf['geometry'] = buffered_gdf.geometry.buffer(distance)
        return buffered_gdf

    def spatial_join(self, target_gdf, join_gdf, how="inner", predicate="intersects"):
        """Realiza una unión espacial (spatial join) entre dos capas."""
        return gpd.sjoin(target_gdf, join_gdf, how=how, predicate=predicate)

    def get_summary_stats(self, gdf):
        """Devuelve estadísticas básicas del GeoDataFrame."""
        return {
            "num_features": len(gdf),
            "crs": str(gdf.crs),
            "geometry_types": gdf.geometry.type.value_counts().to_dict(),
            "columns": list(gdf.columns)
        }
