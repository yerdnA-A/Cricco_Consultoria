document.addEventListener("DOMContentLoaded", (event) => {
  const formCotacao = document.getElementById("form-cotacao");

  // Função para restringir input para números, pontos e vírgulas
  const restrictToNumeric = (e) => {
    e.target.value = e.target.value.replace(/[^0-9.,]/g, "");
  };

  const valorCartaInput = document.getElementById("valor_carta");
  const valorPagoInput = document.getElementById("valor_pago");

  if (valorCartaInput)
    valorCartaInput.addEventListener("input", restrictToNumeric);
  if (valorPagoInput)
    valorPagoInput.addEventListener("input", restrictToNumeric);

  if (formCotacao) {
    formCotacao.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const dados = Object.fromEntries(formData.entries());

      console.log("Dados do formulário prontos para envio:", dados);

      try {
        const resposta = await fetch("http://localhost:5000/api/cotacao", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(dados),
        });

        const resultado = await resposta.json();
        console.log("Resposta do servidor:", resultado);

        const successMessage = document.getElementById("success-message");
        if (successMessage) {
          successMessage.classList.remove("hidden");
          successMessage.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }

        setTimeout(() => {
          e.target.reset();
          if (successMessage) successMessage.classList.add("hidden");
        }, 5000);
      } catch (erro) {
        console.error("Erro ao enviar dados:", erro);
        alert("Ocorreu um erro ao enviar o formulário. Tente novamente.");
      }
    });
  }
});
