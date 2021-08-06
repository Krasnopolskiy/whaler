from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from main.heuristics.certificate import CertificateHeuristic
from main.heuristics.checker import Checker
from main.heuristics.database import DatabaseHeuristic
from main.heuristics.google_safebrowsing import GoogleSafeBrowsingHeuristic
from main.heuristics.yandex_safebrowsing import YandexSafeBrowsingHeuristic

CHECKER = Checker(
    [
        DatabaseHeuristic,
        CertificateHeuristic,
        GoogleSafeBrowsingHeuristic,
        YandexSafeBrowsingHeuristic,
    ]
)


class IndexView(View):
    context = {}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html', self.context)

    def post(self, request: HttpRequest) -> HttpResponse:
        address = request.POST.get('address')
        if address is None:
            return redirect(reverse('index'))
        self.context['result'] = CHECKER.process(address)
        self.context['address'] = address
        return render(request, 'index.html', self.context)

@method_decorator(staff_member_required, name='dispatch')
class ReportsView(View):
    context = {}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'report.html', self.context)
