from rest_framework import viewsets
from rest_framework.response import Response
from .models import Module
from .serializers import ModuleSerializer
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    page_size = 10  # Set number of result to display per page
    max_page_size = 50  # Sets max page size that user may request
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):

        return Response({
            'page_number': self.page.number,
            'size_per_page': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages,
            'total': self.page.paginator.count,
            'results': data
        })


class ModuleViewSet(viewsets.ModelViewSet):

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Module.objects.all()
        query_param = dict(self.request.query_params.items())
        queryset = queryset.filter(**query_param)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
