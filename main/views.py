from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @action(detail=False, methods=["get"])
    def last(self, request):
        """
        Retrieve the last Car object.
        """
        last_car = self.queryset.order_by('-id').first()  # Replace '-id' with '-<field>' if needed
        if last_car:
            serializer = self.get_serializer(last_car)
            return Response(serializer.data)
        return Response({"detail": "No cars found."}, status=404)
