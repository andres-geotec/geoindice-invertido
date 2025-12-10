import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .utils import readJSON
from .classes.inverted_index import InvertedIndex

# query = 'Accidentes vehiculares en tlaxcala'

class ResourceListView(APIView):
  def get(self, request):
    docs = self.loadJSON('docs.json')
    # print(request.GET.get('query', ''))
    query = request.GET.get('q', '')
    if query.strip() == '':
      return Response(docs)

    self.invertedIndex = InvertedIndex()
    self.invertedIndex.tokens = self.loadJSON('tokens.json')
    self.invertedIndex.index = self.loadJSON('index.json')

    q_score = self.invertedIndex.score_query(query)
    scores = sorted(q_score.items(), key=lambda x: x[1], reverse=True)
    # top_k = 3
    top_k = int(request.GET.get('k', len(docs)))
    
    data = []
    for id, score in scores[:top_k]:
      doc = docs[id]
      doc['score'] = score
      data.append({id: doc})

    return Response(data)
  
  def loadJSON(self, file):
    file_path = os.path.join("data", file)
    if not os.path.exists(file_path):
      return Response(
        {"detail": f"Aún no se ha descargado {file}, ejecuta el comando fetch_resources."},
        status=status.HTTP_404_NOT_FOUND,
      )
    data = readJSON(file_path)
    # self.stdout.write(self.style.SUCCESS(f"{file_path} leido correctamente"))
    return data

