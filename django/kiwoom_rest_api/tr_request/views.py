import json
from datetime import datetime as dt
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from manager import TrManager


class OrderRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        req_dir = os.path.join(settings.BASE_DIR, "watcher/cache/tr/requests")
        res_dir = os.path.join(settings.BASE_DIR, "watcher/cache/tr/responses")

        manager = TrManager(request, req_dir, res_dir)
        data = manager.run()
        if data is None:
            return HttpResponse("Bad Request", status=400)
        return JsonResponse(data)
