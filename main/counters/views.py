from django.shortcuts import render
from django.views import View

class MyView(View):
    def post(self, request):
        # <view logic>
        # import pdb; pdb.set_trace()
        print("yo")
        pass
