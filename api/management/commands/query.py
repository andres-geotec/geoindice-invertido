import os
import math

from django.core.management.base import BaseCommand

from .inverted_index import InvertedIndex, tokenize, contarTokens
from .utils import readJSON

query = 'información de ciudades en México'

class Command(BaseCommand):
  help = "Descarga resources de GeoNode y los guarda en un archivo JSON"

  def handle(self, *args, **options):
    self.invertedIndex = InvertedIndex()

    self.stdout.write("Leyendos archivos")
    self.invertedIndex.tokens = self.loadJSON('tokens.json')
    self.invertedIndex.index = self.loadJSON('index.json')

    top_k = 3
    print(f'Buscando ({top_k}): "{query}"')
    q_score = self.score_query(query)
    print(q_score)

  def score_query(self, query):
    tfs = self.invertedIndex.get_tfs()
    idf = self.invertedIndex.get_idf()

    q_tokens = tokenize(query)
    print(q_tokens)
    q_tf = contarTokens(q_tokens)
    print(q_tf)
    q_vec = {t: (q_tf[t]/len(q_tokens)) * idf.get(t, 0) for t in q_tf}
    print(q_vec)
    scores = {}
    for doc in self.invertedIndex.tokens:
        # doc vector
        doc_vec = {t: tfs[doc].get(t, 0) * idf.get(t, 0) for t in q_vec}
        num = sum(q_vec[t] * doc_vec.get(t, 0) for t in q_vec)
        denom = math.sqrt(
            sum(
                v*v for v in q_vec.values())
            ) * math.sqrt(sum(
                v*v for v in doc_vec.values()
            )
        )
        scores[doc] = num / denom if denom else 0.0
    return scores

  def loadJSON(self, file):
    file_path = os.path.join("data", file)
    data = readJSON(file_path)
    self.stdout.write(self.style.SUCCESS(f"{file_path} leido correctamente"))
    return data
