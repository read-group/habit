from django.test import TestCase
#from django.core.cache import cache
from django.core.cache import caches
from habitinfo.models import HabitCatalog
from django.http import JsonResponse

import json
from django.core import serializers

# Create your tests here.
class TestWelcomeTests(TestCase):
    def test_v(self):
        """
        query count test
        """
        cache=caches["default"]

        #序列化queryset
        HabitCatalog.objects.create(code="001",name="hello")
        HabitCatalog.objects.create(code="002",name="hello2")
        rtn1=cache.set("hello1",HabitCatalog.objects.all())
        data = serializers.serialize("json", cache.get("hello1"))
        print("queryset===",data)

        #利用JsonResponse返回响应
        rtn={'status':0,'content':data}
        jsres=JsonResponse(rtn)#内部利用了json.dumps函数来序列化字典
        print(jsres.content)
        # objects=json.loads(str(jsres.content))
        # print(objects)



# def test_contact_view_success(self):
#     # same again, but with valid data, then
#     self.client.login(username='username1', password='password1')
#
#     self.assertRedirects(response, '/')
