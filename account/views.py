from rest_framework import viewsets, response, permissions
from account.serializers import AccountSerializer
from account.models import User
# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(AccountSerializer(request.user,
                context={'request':request}).data)
        return super(AccountViewSet, self).retrieve(request, pk)