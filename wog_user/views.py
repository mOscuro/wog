from rest_framework import viewsets, response, permissions
from wog_user.serializers import UserAccountSerializer
from wog_user.models import User
# Create your views here.

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserAccountSerializer(request.user,
                context={'request':request}).data)
        return super(UserAccountViewSet, self).retrieve(request, pk)