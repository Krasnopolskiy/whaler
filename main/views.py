from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from main.heuristics.certificate import CertificateHeuristic
from main.heuristics.checker import Checker
from main.heuristics.database import DatabaseHeuristic
from main.heuristics.safebrowsing import SafeBrowsingHeuristic


CHECKER = Checker([DatabaseHeuristic, CertificateHeuristic, SafeBrowsingHeuristic])


class IndexView(View):
    context = {}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        address = request.POST.get('address')
        if address is None:
            return redirect(reverse('index'))
        self.context['result'] = CHECKER.process(address)
        self.context['address'] = address
        return render(request, 'index.html', self.context)
