import spacy
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

try:
    from wordcloud import WordCloud
except ImportError:
    WordCloud = None

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

try:
    from bertopic import BERTopic
except ImportError:
    BERTopic = None

class NLPProcessor:
    def __init__(self, model="es_core_news_sm"):
        """
        Inicializa el procesador de lenguaje natural.
        Requiere haber descargado el modelo: python -m spacy download es_core_news_sm
        """
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"[{model}] no encontrado. Se necesita instalarlo.")
            self.nlp = None

    def process_text(self, text):
        """Procesa un bloque de texto y devuelve el objeto Doc de Spacy."""
        if not self.nlp:
            raise ValueError("El modelo de Spacy no está cargado.")
        return self.nlp(text)

    def extract_entities(self, text):
        """Extrae entidades nombradas (personas, lugares, organizaciones) del texto."""
        doc = self.process_text(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        return pd.DataFrame(entities)

    def word_frequencies(self, text, remove_stopwords=True):
        """Calcula la frecuencia de palabras, opcionalmente eliminando stop words."""
        doc = self.process_text(text)
        words = [
            token.text.lower() for token in doc 
            if token.is_alpha and (not remove_stopwords or not token.is_stop)
        ]
        freq = Counter(words)
        return pd.DataFrame(freq.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)

    def generate_wordcloud(self, text, remove_stopwords=True):
        """Genera un gráfico WordCloud y devuelve la figura para renderizar."""
        if not WordCloud:
            raise ImportError("Librería WordCloud no instalada.")
            
        doc = self.process_text(text)
        words = " ".join([
            token.text for token in doc 
            if token.is_alpha and (not remove_stopwords or not token.is_stop)
        ])
        
        wc = WordCloud(width=800, height=400, background_color='white').generate(words)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        return fig

    def analyze_sentiment(self, text):
        """Devuelve un análisis de sentimiento básico usando TextBlob."""
        if not TextBlob:
            raise ImportError("Librería TextBlob no instalada.")
        
        blob = TextBlob(text)
        # Note: TextBlob default is English, but works basic for others or via translation.
        # En un entorno robusto, usaríamos transformers multilingüe, pero esto ilustra el método mixto.
        return {"Polaridad": blob.sentiment.polarity, "Subjetividad": blob.sentiment.subjectivity}

    def topic_modeling(self, docs_list):
        """Ejecuta BERTopic sobre una lista de documentos/textos."""
        if not BERTopic:
            raise ImportError("Librería BERTopic no instalada.")
        if len(docs_list) < 5:
            raise ValueError("BERTopic requiere una lista de varios documentos para identificar patrones estadísticos (Mínimo 5).")
            
        topic_model = BERTopic(language="multilingual")
        topics, probs = topic_model.fit_transform(docs_list)
        return topic_model.get_topic_info()
