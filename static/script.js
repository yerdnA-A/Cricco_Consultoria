document.addEventListener("DOMContentLoaded", () => {
  const formCotacao = document.getElementById("form-cotacao");
  const valorCartaInput = document.getElementById("valor_carta");
  const valorPagoInput = document.getElementById("valor_pago");
  const successMessage = document.getElementById("success-message");
  const errorMessage = document.getElementById("error-message");

  // Restringe input para números, pontos e vírgulas
  const restrictToNumeric = (e) => {
    e.target.value = e.target.value.replace(/[^0-9.,]/g, "");
  };

  if (valorCartaInput)
    valorCartaInput.addEventListener("input", restrictToNumeric);
  if (valorPagoInput)
    valorPagoInput.addEventListener("input", restrictToNumeric);

  if (formCotacao) {
    formCotacao.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const dados = Object.fromEntries(formData.entries());

      // Checa se os campos obrigatórios estão preenchidos
      if (!dados.nome || !dados.whatsapp || !dados.email) {
        alert("Preencha os campos Nome, WhatsApp e Email.");
        return;
      }

      try {
        const resposta = await fetch("/api/cotacao", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dados),
        });

        const resultado = await resposta.json();
        console.log("Resposta do servidor:", resultado);

        if (resultado.status === "sucesso") {
          if (successMessage) {
            successMessage.classList.remove("hidden");
            successMessage.scrollIntoView({
              behavior: "smooth",
              block: "center",
            });
          }
        } else {
          const msg =
            typeof resultado.mensagem === "object"
              ? JSON.stringify(resultado.mensagem, null, 2)
              : resultado.mensagem;

          if (errorMessage) {
            errorMessage.textContent = "Erro ao enviar formulário: " + msg;
            errorMessage.classList.remove("hidden");
            errorMessage.scrollIntoView({
              behavior: "smooth",
              block: "center",
            });
          } else {
            alert("Erro ao enviar formulário: " + msg);
          }
        }

        // Reseta mensagens e formulário após 5 segundos
        setTimeout(() => {
          e.target.reset();
          if (successMessage) successMessage.classList.add("hidden");
          if (errorMessage) errorMessage.classList.add("hidden");
        }, 5000);
      } catch (erro) {
        console.error("Erro ao enviar dados:", erro);
        alert("Ocorreu um erro ao enviar o formulário. Tente novamente.");
      }
    });
  }
});
