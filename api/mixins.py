from rest_framework import generics, status, views
from rest_framework.response import Response


class GetObjectView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        name = self.model.__name__ or 'Object'
        instance = self.get_queryset()
        if instance:
            serializer = self.serializer_class(instance)
            return Response({
                "responseCode": 100,
                "message": f"{name} Detail",
                "data": serializer.data
            })
        else:
            return Response({
                "responseCode": 103,
                "message": f"{name} Not Found."
            }, status=status.HTTP_404_NOT_FOUND)


class UpdateObjectView(generics.UpdateAPIView):

    def post(self, request, *args, **kwargs):
        name = self.model.__name__ or 'Object'
        instance = self.get_queryset()
        if not instance:
            return Response({
                "responseCode": 103,
                "message": f"{name} Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
            instance, data=request.data,
            partial=self.partial_update == True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "responseCode": 100,
                "message": f"{name} Updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "responseCode": 103,
                "message": f"Error Updating {name}",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
