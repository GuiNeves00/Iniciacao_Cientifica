document.getElementById("download-btn").addEventListener("click", function () {
  // Fazer uma requisição ao backend para obter o arquivo 'db.json'
  fetch("/downloads")
    .then((response) => response.blob())
    .then((blob) => {
      // Criar um URL temporário para o Blob
      const url = URL.createObjectURL(blob);

      // Criar um link de download e clicar nele para iniciar o download
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = "db.json";
      document.body.appendChild(a);
      a.click();

      // Limpar o URL temporário
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => console.error("Erro ao obter o arquivo JSON:", error));
});
