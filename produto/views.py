from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        produto = variacao.produto
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        variacao_id = variacao_id
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        preco_quatitativo = variacao.preco
        preco_quatitativo_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        variacao_estoque = variacao.estoque

        if produto.imagem:
            imagem = produto.imagem.name
        else:
            imagem = ''

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_atual = carrinho[variacao_id]['quantidade']
            quantidade_atual += 1

            if variacao_estoque < 1:
                messages.error(self.request, 'Estoque insuficiente.')
                return redirect(http_referer)

            if variacao_estoque < quantidade_atual:
                messages.error(
                    self.request,
                    f'Estoque insuficiente, adicionamos '
                    f'{variacao_estoque}x no seu carrinho.'
                )
                quantidade_atual = variacao_estoque

            carrinho[variacao_id]['preco_quatitativo'] = preco_quatitativo * \
                quantidade_atual
            carrinho[variacao_id]['preco_quatitativo_promocional'] = \
                preco_quatitativo_promocional * quantidade_atual
            carrinho[variacao_id]['quantidade'] = quantidade_atual
        else:
            if variacao_estoque < 1:
                messages.error(self.request, 'Estoque insuficiente.')
                return redirect(http_referer)

            carrinho[variacao_id] = {
                'produto_nome': produto_nome,
                'produto_id': produto_id,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quatitativo': preco_quatitativo,
                'preco_quatitativo_promocional': preco_quatitativo_promocional,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()
        print(carrinho)

        return HttpResponse(f'{variacao.produto} {variacao.nome}')


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover carrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
