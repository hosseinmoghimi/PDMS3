from web.apps import APP_NAME
from web.models import Bus, ComServer, ComServerDataBlock, Feeder
from authentication.repo import ProfileRepo
 

        
class BusRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Bus.objects
        self.profile = ProfileRepo(user=self.user).me
        # self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_line_id' in kwargs:
            objects = objects.filter(invoice_line_id=kwargs['invoice_line_id'])
        if 'product_id' in kwargs:
            objects = objects.filter(invoice_line__product_or_service_id=kwargs['product_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def bus(self, *args, **kwargs):
        if 'bus_id' in kwargs:
            return self.objects.filter(pk= kwargs['bus_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class FeederRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Feeder.objects
        self.profile = ProfileRepo(user=self.user).me
        # self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'com_server_id' in kwargs:
            objects = objects.filter(com_server_id=kwargs['com_server_id'])
        if 'bus_id' in kwargs:
            objects = objects.filter(bus_id=kwargs['bus_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def feeder(self, *args, **kwargs):
        if 'feeder_id' in kwargs:
            return self.objects.filter(pk= kwargs['feeder_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class ComServerRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ComServer.objects
        self.profile = ProfileRepo(user=self.user).me
        # self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'bus_id' in kwargs:
            objects = objects.filter(bus_id=kwargs['bus_id'])
        if 'feeder_id' in kwargs:
            objects = Feeder.objects.filter(pk=kwargs['feeder_id']).first().com_server_set()
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def com_server(self, *args, **kwargs):
        if 'com_server_id' in kwargs:
            return self.objects.filter(pk= kwargs['com_server_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class ComServerDataBlockRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ComServerDataBlock.objects
        self.profile = ProfileRepo(user=self.user).me
        # self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_line_id' in kwargs:
            objects = objects.filter(invoice_line_id=kwargs['invoice_line_id'])
        if 'product_id' in kwargs:
            objects = objects.filter(invoice_line__product_or_service_id=kwargs['product_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def com_server_data_block(self, *args, **kwargs):
        if 'com_server_id' in kwargs:
            return self.objects.filter(pk= kwargs['com_server_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()

 