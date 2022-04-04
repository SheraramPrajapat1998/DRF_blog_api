from rest_framework.response import Response
from rest_framework import views
import psutil, shutil


class APIHealthCheck(views.APIView):
    name = "api_health_check"
    """
    To Check APP Health
    """
    def get(self, request, format=None):
        cpu_dict = self.cpu_usage()
        cpu_dict["health"] = "OK"
        cpu_dict["message"] = "Working Fine."
        return Response(cpu_dict)

    def cpu_usage(self):
        "Check CPU Usage"
        du = shutil.disk_usage('/')
        used = (du.used / du.total) * 100
        cpu_percent_data = psutil.cpu_percent()
        virtual_memory_data = dict(psutil.virtual_memory()._asdict())
        virtual_memory_data['used_disk'] = used
        virtual_memory_data['available_disk'] = (100 - used)
        virtual_memory_data['cpu_percent_data'] = cpu_percent_data

        return virtual_memory_data
