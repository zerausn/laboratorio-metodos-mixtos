import unittest
import pandas as pd
import sys
import os

# Agregamos la ruta principal para importar el backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.nlp_module import NLPProcessor

class TestNLPModule(unittest.TestCase):
    def setUp(self):
        # Para pruebas, podríamos mockear el modelo si no queremos descargarlo, 
        # pero para el backend real esperamos que funcione
        self.processor = NLPProcessor("es_core_news_sm")

    def test_extract_entities(self):
        if not self.processor.nlp:
            self.skipTest("Modelo es_core_news_sm no instalado.")
            
        texto = "Juan Pérez visitó la ciudad de Madrid el pasado viernes junto a la ONU."
        df_entities = self.processor.extract_entities(texto)
        
        # Deberíamos tener al menos 'Juan Pérez', 'Madrid' y 'ONU'
        self.assertGreater(len(df_entities), 0)
        self.assertIn('Juan Pérez', df_entities['text'].values)
        self.assertIn('Madrid', df_entities['text'].values)

    def test_word_frequencies(self):
        if not self.processor.nlp:
            self.skipTest("Modelo es_core_news_sm no instalado.")
            
        texto = "La comunidad indicó que la comunidad tiene problemas con el agua."
        df_freq = self.processor.word_frequencies(texto, remove_stopwords=True)
        
        # 'comunidad' debería ser la palabra más frecuente
        self.assertGreater(len(df_freq), 0)
        self.assertEqual(df_freq.iloc[0]['Word'], 'comunidad')

if __name__ == '__main__':
    unittest.main()
