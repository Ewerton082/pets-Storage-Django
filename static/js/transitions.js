$(document).ready(function() {
    // Quando o formulário for enviado
    $('#myForm').on('submit', function(event) {
        event.preventDefault();  // Impede o envio normal do formulário

        $.ajax({
            type: 'POST',
            url: '{% url "minha_url_de_redirecionamento" %}',  // URL de destino
            data: $(this).serialize(),  // Envia os dados do formulário
            success: function(response) {
                // Se a resposta for bem-sucedida, redireciona
                window.location.href = response.redirect_url;
            },
            error: function(xhr, errmsg, err) {
                console.log("Erro: " + errmsg);
            }
        });
    });
});