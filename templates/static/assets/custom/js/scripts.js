(function () {
    select_variacao = document.getElementById('select-variacoes');
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');

    if (!select_variacao) {
        return;
    }

    if (!variation_preco) {
        return;
    }

    select_variacao.addEventListener('change', function () {
        preco = this.options[this.selectedIndex].getAttribute('data-preco');
        preco_promocional = this.options[this.selectedIndex].getAttribute('data-preco-promocional');

        variation_preco.innerHTML = preco;

        if (variation_preco_promocional) {
            variation_preco_promocional.innerHTML = preco_promocional;
        }
    })
})();

