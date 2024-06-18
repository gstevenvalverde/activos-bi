from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View

from activos.management.commands.load_activos import load_activos

class LoadActivosView(View):
    def get(self, request):
        try:
            load_activos()
            return JsonResponse({"message": "Activos cargados exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
