
class AreaRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Area.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
    def area(self,*args, **kwargs):
        pk=0
        if 'area_id' in kwargs:
            pk=kwargs['area_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    
