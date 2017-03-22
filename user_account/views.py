from rest_framework import viewsets, response, permissions
from user_account.serializers import UserAccountSerializer
from user_account.models import User
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