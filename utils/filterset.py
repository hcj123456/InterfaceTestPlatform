from django_filters import FilterSet,filters
from projects.models import Projects


class TimeFilterSet(FilterSet):

    max_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')
    min_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')

    class Meta:
        model = Projects
        # fields = ['max_time', 'min_time']
        fields = ('max_time', 'min_time')