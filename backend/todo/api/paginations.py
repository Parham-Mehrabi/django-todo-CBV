from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TasksPagination(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        return Response(
            # note:1
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "tasks_for_each_page": self.page_size,
                "total_tasks": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data
                # note:2
            }
        )


"""
    #1:
        we could just keep it simple as below:
            class MyPagination(PageNumberPagination):
                page_size = 2
                max_page_size = 10
                page_query_param = 'page'

    #2:
        this key should always called results other wise pagination will break other filters and they wont work
        so we cant just say some thin like: "'data': data"
"""
