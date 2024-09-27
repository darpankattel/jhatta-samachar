from rest_framework.generics import ListCreateAPIView, ListAPIView
from core.response import MyResponse


# This file is not used in the project, but is a good example of how to create custom classes for DRF views
# TODO: Fix the bug that not all the records are returned, instead only the first page is returned, hence, is not working as expected
# TODO: But, this is not used in the project, so, it is not a priority


class CustomListAPIView(ListAPIView):
    """
    Similar to ListAPIView, but with custom pagination, that, if request.GET["all"] == "true", will return all objects, else, will return the paginated response if required.
    """

    def get_paginated_response(self, data):
        # if get all is true, then return all
        if self.request.GET.get('all') == 'true':
            return MyResponse.success(data=data, message="Successfully fetched")

        return super().get_paginated_response(data)


class CustomListCreateAPIView(ListCreateAPIView):
    """
    Similar to ListCreateAPIView, but with custom pagination, that, if request.GET["all"] == "true", will return all objects, else, will return the paginated response if required.
    """

    def get_paginated_response(self, data):
        # if get all is true, then return all
        print(self.request.GET.get('all'))
        if self.request.GET.get('all') == 'true':
            return MyResponse.success(data=data, message="Successfully fetched")

        return super().get_paginated_response(data)
