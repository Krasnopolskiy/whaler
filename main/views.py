from django.contrib.admin.views.decorators import staff_member_required
from django.db import connections
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from main.heuristics.certificate import CertificateHeuristic
from main.heuristics.checker import Checker
from main.heuristics.database import DatabaseHeuristic
from main.heuristics.google_safebrowsing import GoogleSafeBrowsingHeuristic
from main.heuristics.neuro_network import NeuroNetworkHeuristic
from main.heuristics.yandex_safebrowsing import YandexSafeBrowsingHeuristic

CHECKER = Checker(
    [
        NeuroNetworkHeuristic,
        GoogleSafeBrowsingHeuristic,
        YandexSafeBrowsingHeuristic,
        DatabaseHeuristic,
        CertificateHeuristic,
    ]
)


def validate_addres(address: str) -> bool:
    if address is None:
        return False
    if '.' not in address:
        return False
    if len(address) < 4:
        return False
    return True


class IndexView(View):
    context = {}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html', self.context)

    def post(self, request: HttpRequest) -> HttpResponse:
        address = request.POST.get('address')
        if not validate_addres(address):
            return redirect(reverse('index'))
        self.context['result'] = CHECKER.process(address)
        self.context['address'] = address
        return render(request, 'index.html', self.context)


class ReportView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        address = request.POST.get('address')
        if not validate_addres(address):
            return redirect(reverse('index'))
        with connections['reports'].cursor() as cursor:
            cursor.execute(
                'INSERT INTO reports (address) VALUES (%s)', [str(address)],
            )
        return redirect(reverse('index'))


@method_decorator(staff_member_required, name='dispatch')
class ReportListView(View):
    context = {}

    def get(self, request: HttpRequest) -> HttpResponse:
        with connections['reports'].cursor() as cursor:
            cursor.execute('SELECT id, address FROM reports')
            self.context['reports'] = cursor.fetchall()
        return render(request, 'report.html', self.context)


@method_decorator(staff_member_required, name='dispatch')
class ReportAcceptView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        with connections['reports'].cursor() as cursor:
            cursor.execute(
                'SELECT address FROM reports WHERE id=%s', [str(pk)],
            )
            address = cursor.fetchone()[0]
            cursor.execute(
                'DELETE FROM reports WHERE id=%s', [str(pk)],
            )
            with connections['phishing'].cursor() as cursor:
                cursor.execute(
                    'INSERT INTO links (link) VALUES (%s)', [str(address)],
                )
                cursor.execute(
                    'INSERT INTO domains (domain) VALUES (%s)', [str(address)],
                )
        return redirect(reverse('index'))


@method_decorator(staff_member_required, name='dispatch')
class ReportDeclineView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        with connections['reports'].cursor() as cursor:
            cursor.execute(
                'DELETE FROM reports WHERE id=%s', [str(pk)],
            )
        return redirect(reverse('index'))
