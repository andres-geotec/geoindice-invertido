import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ResourceListView(APIView):
  def get(self, request):
    file_path = os.path.join("data", "resources.json")

    if not os.path.exists(file_path):
      return Response(
        {"detail": "Aún no se ha descargado resources.json, ejecuta el comando fetch_resources."},
        status=status.HTTP_404_NOT_FOUND,
      )

    with open(file_path, "r", encoding="utf-8") as f:
      data = json.load(f)

    # Aquí podrías filtrar, paginar, etc. usando 'data'
    return Response(data)

