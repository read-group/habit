from django.test import TestCase
#from django.core.cache import cache
from django.core.cache import caches
from habitinfo.models import HabitCatalog
from cms.models import WxWelcome
from django.http import JsonResponse

import json
from django.core import serializers

# Create your tests here.
class TestWelcomeTests(TestCase):
    def test_v(self):
        """
        query count test
        """
        a=WxWelcome.objects.all()
        print(type(a))
        # cache=caches["default"]
        #
        # #序列化queryset
        # HabitCatalog.objects.create(code="001",name="hello")
        # HabitCatalog.objects.create(code="002",name="hello2")
        # rtn1=cache.set("hello1",HabitCatalog.objects.all())
        # data = serializers.serialize("json", cache.get("hello1"))
        # print("queryset===",data)
        #
        # #利用JsonResponse返回响应
        # rtn={'status':0,'content':data}
        # jsres=JsonResponse(rtn)#内部利用了json.dumps函数来序列化字典
        # print(jsres.content)



        #构造一个欢迎对象，目的测试单模型对象
        # imgpath='/home/jy/pv1/rice/habit/back_python/back/media/upload/webwxgetmsgimg.jpg'
        # welcome=WxWelcome()
        # welcome.code="001"
        # welcome.name="ok"
        # from media.models import MediaResource,MEDIA_TYPE
        # from django.core.files.uploadedfile import SimpleUploadedFile
        #
        # #构造媒体对象
        # media=MediaResource()
        # media.code='001'
        # media.name='ddd'
        # media.mediaType='img'
        # media.img = SimpleUploadedFile(name='test_image.jpg', content=open(imgpath, 'rb').read(), content_type='image/jpeg')
        # m=media.save()
        # welcome.img=m
        # #print(welcome.toJSON())
        # #dic={"status":1,"data":[welcome]}
        # d=serializers.serialize("json", [welcome])
        # print(d)

        #welcome.save()

# def test_contact_view_success(self):
#     # same again, but with valid data, then
#     self.client.login(username='username1', password='password1')
#
#     self.assertRedirects(response, '/')
