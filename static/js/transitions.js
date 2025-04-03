document.addEventListener("DOMContentLoaded", () => {
    const formBuy = document.getElementById("form-buy");
    const formSell = document.getElementById("form-sell");

    if (formBuy) {
        formBuy.addEventListener("submit", (event) => {
            const quantityInput = formBuy.querySelector("input[name='quantidade']");
            const quantidade = parseInt(quantityInput.value, 10);
            const botao = document.getElementById("sub-btn");

            if (isNaN(quantidade) || quantidade <= 0) {
                event.preventDefault();
                alert("Por favor, insira uma quantidade válida maior que 0.");
                return;
            }

            if (!botao.disabled) {
                botao.disabled = true;
                botao.innerText = "Processando...";
            } else {
                event.preventDefault();
            }
        });
    }

    if (formSell) {
        formSell.addEventListener("submit", (event) => {
            const quantityInput = formSell.querySelector("input[name='quantidade']");
            const quantidade = parseInt(quantityInput.value, 10);
            const stockQuantity = parseInt(formSell.dataset.stockQuantity, 10);

            if (isNaN(quantidade) || quantidade <= 0) {
                event.preventDefault();
                alert("Por favor, insira uma quantidade válida maior que 0.");
                return;
            }

            if (quantidade > stockQuantity) {
                event.preventDefault();
                alert(`Você está tentando vender mais do que o estoque disponível (${stockQuantity}).`);
                return;
            }

            const botao = formSell.querySelector("button[type='submit']");
            if (botao) {
                botao.disabled = true;
                botao.innerText = "Processando...";
            }
        });
    }
});
