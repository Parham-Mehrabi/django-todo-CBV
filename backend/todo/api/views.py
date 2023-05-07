from rest_framework.viewsets import ModelViewSet
from ..models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrSuperUser, IsVerified
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import TasksPagination


class TaskFilter(FilterSet):
    context = CharFilter(field_name="context", lookup_expr="exact")

    class Meta:
        model = Task
        fields = ["context"]


class TaskViewSet(ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrSuperUser, IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ["id"]
    filterset_fields = {
        "context": ["in", "exact"],
        "author__email": ["exact", "in"],
        "created": ["lt", "gt"],
    }
    # filterset_class = TaskFilter
    # note:1&2
    search_fields = ["title", "context", "author__email"]
    ordering_fields = ["is_complete", "created"]
    pagination_class = TasksPagination

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(author=user)


"""
    #1:
        we should just mention the fields but here with a dictionary we declare how exactly we gonna filter
        for example for created we can specify a limited period of time between lt (lower than) and gt(greater than)
        
        
    #2:
        we could use a class and use the class in filterset_class rather the filterset_fields for example:
            class MyFilter(filters.FilterSet):
                min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
                max_price = filters.NumberFilter(field_name="price", lookup_expr='lte') 
                class Meta:
                    model = Product
                    fields = ['category', 'in_stock']
                    
                
            class ProductList(generics.ListAPIView):
                queryset = Product.objects.all()
                serializer_class = ProductSerializer
                filter_backends = (filters.DjangoFilterBackend,)
                filterset_class = MyFilter
"""
