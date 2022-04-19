from rest_framework import mixins, viewsets

class MixedPermission:
    '''
        Mixed permissions
    '''
    def get_permissions(self):
        '''
            get permissions for the action
        '''
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CreateRetrieveUpdateDestroyViewset(mixins.CreateModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin,
                                         MixedPermission,
                                         viewsets.GenericViewSet):
    '''
        viewset for craete/detail/update/delete
    '''
    pass
