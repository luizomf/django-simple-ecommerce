from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar')


class FecharPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FecharPedido')


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')
