import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Activa la conversión automática de DataFrames de Pandas a DataFrames de R
pandas2ri.activate()

class StatsProcessor:
    def __init__(self):
        """
        Inicializa la interfaz con R usando rpy2.
        Importa los paquetes base de R.
        """
        self.r_base = importr('base')
        self.r_stats = importr('stats')

    def run_linear_model(self, df, formula_str):
        """
        Ejecuta un modelo de regresión lineal en R (lm) dada una fórmula.
        Ejemplo formula_str: 'VariableDependiente ~ VarIndep1 + VarIndep2'
        """
        try:
            # Convierte el string de la fórmula a objeto Fórmula de R
            r_formula = robjects.Formula(formula_str)
            
            # Ejecuta lm() en R
            model = self.r_stats.lm(r_formula, data=df)
            
            # Obtiene el resumen del modelo
            summary = self.r_base.summary(model)
            
            # Extrayendo coeficientes desde la representación R (depende de la estructura de summary.lm)
            # Para propósitos del prototipo, devolvemos el string representativo
            return str(summary)
            
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar el modelo multivariado en R: {str(e)}")

    def run_anova(self, df, formula_str):
        """Ejecuta un análisis de varianza y devuelve los resultados."""
        try:
             # Ejecuta aov() en R
            r_formula = robjects.Formula(formula_str)
            aov_model = self.r_stats.aov(r_formula, data=df)
            summary = self.r_base.summary(aov_model)
            return str(summary)
        except Exception as e:
             raise RuntimeError(f"Error al ejecutar ANOVA en R: {str(e)}")
