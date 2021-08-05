from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponsePermanentRedirect:
        address = request.POST.get('address')
        if address is None:
            return redirect(reverse('index'))
        print(f'[*] New address uploaded: {address}')
        return redirect(reverse('index'))
