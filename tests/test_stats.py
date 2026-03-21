import unittest
import pandas as pd
import sys
import os

# Agregamos la ruta principal para importar el backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.stats_module import StatsProcessor

class TestStatsModule(unittest.TestCase):
    def setUp(self):
        try:
            self.processor = StatsProcessor()
            self.r_installed = True
        except Exception as e:
            self.r_installed = False
            print(f"R no está instalado o rpy2 falló de inicializarse: {e}")
            
        # Creamos un DataFrame de prueba cruzando datos "cualitativos" (categorías) y cuantitativos
        self.df = pd.DataFrame({
            'Satisfaccion': [5, 4, 3, 5, 2, 4, 5, 2],
            'Grupo': ['A', 'A', 'B', 'A', 'B', 'A', 'B', 'B'],
            'Edad': [25, 30, 22, 40, 35, 28, 50, 42]
        })

    def test_run_linear_model(self):
        if not self.r_installed:
            self.skipTest("Entorno R no detectado.")
            
        # Probamos un modelo simple: Satisfacción predicha por Grupo y Edad
        try:
            resumen = self.processor.run_linear_model(self.df, 'Satisfaccion ~ Grupo + Edad')
            self.assertIsInstance(resumen, str)
            self.assertIn("Coefficients:", resumen)
            self.assertIn("GrupoB", resumen) # Debería aparecer como factor tonto (dummy) en R
        except RuntimeError as e:
            self.fail(f"Falla en modelo lineal: {e}")

    def test_run_anova(self):
        if not self.r_installed:
            self.skipTest("Entorno R no detectado.")
            
        try:
            # ANOVA de una vía: Satisfacción vs Grupo
            resumen = self.processor.run_anova(self.df, 'Satisfaccion ~ Grupo')
            self.assertIsInstance(resumen, str)
            self.assertIn("Grupo", resumen)
            self.assertIn("Residuals", resumen)
        except RuntimeError as e:
            self.fail(f"Falla en ANOVA: {e}")

if __name__ == '__main__':
    unittest.main()
