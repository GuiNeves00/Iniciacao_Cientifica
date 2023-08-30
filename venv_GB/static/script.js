// Exibicao e selecao do toponimo
const toponimos = Array.from(document.querySelectorAll(".toponimo"));
const toponimo_display = document.querySelector("#top-display");
let toponimo_selecionado = document.getElementById("top-s");
const formulario = document.getElementById("formulario");
let toponimo_clicado_estilo = null;

/**@param {MouseEvent} event */
function selecionarToponimo(event) {
  const toponimo_clicado = event.currentTarget.innerHTML;
  toponimo_clicado_estilo = event.currentTarget;
  toponimo_display.innerHTML = '"' + toponimo_clicado + '"';
  toponimo_selecionado.value = toponimo_clicado;
  // sempre que escolher um novo toponimo para avaliar
  // matenha a pergunta 1 ativa e remova as demais
  // e desabilite o botao de enviar formulario
  pergunta1.style.display = "block";
  pergunta2.style.display = "none";
  pergunta3.style.display = "none";
  submit.disabled = true;
  submit.style.backgroundColor = "#f8f8f2";
  formulario.reset();

  // se nenhum toponimo estiver selecionado, remova a pergunta1
  if (toponimo_display === "..." || toponimo_display === "") {
    pergunta1.style.display = "none";
  }
}

if (toponimos) {
  toponimos.forEach((toponimo) =>
    toponimo.addEventListener("click", selecionarToponimo)
  );
}

// Faz com que a palavra avaliada mude de cor apos o envio do formulario. Quando a opcao de repetir respsota estiver marcada, todas as palavras correspondentes mudaram de cor.
formulario.addEventListener("submit", function (event) {
  event.preventDefault();

  if (checkbox.checked && indicesRR.length > 1) {
    for (var j = 0; j < indicesRR.length; j++) {
      var toponimo_estilo = toponimos[indicesRR[j]];
      toponimo_estilo.style.backgroundColor = "#50fa7b";
      toponimo_estilo.style.color = "black";
    }
    toponimo_clicado_estilo = null;
  } else if (toponimo_clicado_estilo) {
    toponimo_clicado_estilo.style.backgroundColor = "#50fa7b";
    toponimo_clicado_estilo.style.color = "black";
  }
  toponimo_clicado_estilo = null;
  submit.disabled = true;
  submit.style.backgroundColor = "#f8f8f2";
});

//_________________________________________________________________

// Exibir quantos possíveis toponimos existem na noticia
// Perguntar se o usuario que avaliar a noticia ou nao
// Carregar funcao de mostrar tutorial
window.onload = function () {
  var qntdToponimos = toponimos.length;
  var cniQntdToponimos = document.getElementById("cni-qntd-toponimos");
  cniQntdToponimos.textContent =
    "Possíveis nomes de lugares nesta notícia: " + qntdToponimos;
  exibirDialogo();

  document
    .getElementById("tutorial-btn")
    .addEventListener("click", openTutorial);

  const closeButton = document.getElementById("fechar-tutorial-btn");
  closeButton.style.visibility = "visible";

  document
    .getElementById("tutorial-popup")
    .addEventListener("scroll", function () {
      closeButton.style.visibility = this.scrollTop > 20 ? "visible" : "hidden";
    });

  // Event listener to close the popup when clicking outside of it
  window.addEventListener("click", function (event) {
    const popup = document.getElementById("tutorial-popup");
    if (event.target === popup) {
      closeTutorial();
    }
  });

  // Event listener to close the popup when 'Esc' key is pressed
  window.addEventListener("keydown", function (event) {
    const popup = document.getElementById("tutorial-popup");
    if (event.key === "Escape" && popup.style.display === "block") {
      closeTutorial();
    }
  });
};

// Exibir caixa de dialogo perguntando se ja avaliou a noticia
function exibirDialogo() {
  var dialogo = document.getElementById("confirmar-noticia-inedita");
  dialogo.style.display = "block";
  overlay.style.display = "block";
}

function recarregarPagina() {
  location.reload();
}

//_________________________________________________________________

// PERGUNTA 3 -- Seleciona estado da lista de estados
function selecionarEstado() {
  var listaEstados = document.getElementById("listaEstados");
  var estado = document.getElementById("pergunta3-respostas");
  estado.value = listaEstados.value;
  // estado = resposta da P3
}
//_________________________________________________________________

// PERGUNTA 2 -- Seleciona tipo de toponimo da lista de tipos
function selecionarTipo() {
  var tipo = document.getElementById("pergunta2-respostas").value;
  // document.getElementById("tipo-selecionado").value = tipo;
}
//_________________________________________________________________

// TESTES / WIP NOVAS FUNCIONALIDADES

// Manipulacao e "UX" no Formulario
const submit = document.getElementById("submit");
const pergunta1 = document.getElementById("pergunta-1");
const pergunta2 = document.getElementById("pergunta-2");
const pergunta3 = document.getElementById("pergunta-3");

const respostaP2 = document.getElementById("pergunta2-respostas");
const respostaP3 = document.getElementById("pergunta3-respostas");

// A funcao abaixo mostra ou nao a pergunta 2 e o botao de enviar com base na resposta da pergunta 1
function mostrarPergunta2() {
  // se a resposta da pergunta 1 for 'sim' mostre a pergunta 2 e mantenha o submit desativado
  if (
    pergunta1.querySelector('input[name="pergunta-1"]:checked').value === "sim"
  ) {
    pergunta2.style.display = "block";
    submit.disabled = true;
    submit.style.backgroundColor = "#f8f8f2";
  }
  // se a resposta da pergunta 1 for 'nao' ou 'nao-sei',
  // remova a resposta das outras perguntas, matenha-as escondidas e ative o submit
  else {
    pergunta2.style.display = "none";
    respostaP2.value = "";
    pergunta3.style.display = "none";
    respostaP3.value = "";
    submit.disabled = false;
    submit.style.backgroundColor = "#50fa7b";
  }
}
pergunta1.addEventListener("change", mostrarPergunta2);
//...

// Mostrar pergunta 3 apos pergunta 2 ter sido respondida
function mostrarPergunta3() {
  if (pergunta2.value !== "") {
    pergunta3.style.display = "block";
  } else {
    pergunta3.style.display = "none";
  }
}
pergunta2.addEventListener("change", mostrarPergunta3);
//...

// Disponibiliza o botão de submit apos a pergunta 3 ter sido respondida
function mostrarSubmit() {
  if (pergunta3.value !== "") {
    submit.disabled = false;
    submit.style.backgroundColor = "#50fa7b";
  } else {
    submit.disabled = true;
  }
}
pergunta3.addEventListener("change", mostrarSubmit);
//_________________________________________________________________

// Testando ação quando usuário clica em próxima notícia
const continuar = document.getElementById("continuar");

/** @param {MouseEvent} event */
function continuarAvaliando() {
  console.log("Clicou em Próxima Notícia");
  location.reload();
}

if (continuar) {
  continuar.addEventListener("click", continuarAvaliando);
}
//_________________________________________________________________

// Testando ação quando usuário tecla enter (adicionar toponimo nao identificado)
const teste = document.getElementById("novo-toponimo");

/** @param {KeyboardEvent} event */
function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    toponimo_selecionado.value = teste.value;
    toponimo_display.innerHTML = '"' + teste.value + '"';
    teste.value = ""; //limpa caixa de texto

    pergunta2.style.display = "none";
    pergunta3.style.display = "none";

    formulario.reset();
  }
}

if (teste) {
  teste.addEventListener("keydown", handleEnter);
}
//_________________________________________________________________

// SIDERBAR FIXADA
window.addEventListener("load", () => {
  const sidebar = document.querySelector(".sidebar");
  const alturaJanela = window.innerHeight;
  sidebar.style.height = `${alturaJanela}px`;

  window.addEventListener("resize", () => {
    const novaAlturaJanela = window.innerHeight;
    sidebar.style.height = `${novaAlturaJanela}px`;
  });
});

// TUTORIAL POPUP

// Função para abrir o popup
function openTutorial() {
  var popup = document.getElementById("tutorial-popup");
  popup.style.display = "block";
}

function openSobre() {
  var popup = document.getElementById("sobre-popup");
  popup.style.display = "block";
}

// Função para fechar o popup
function closeTutorial() {
  var popup = document.getElementById("tutorial-popup");
  popup.style.display = "none";
}

function closeSobre() {
  var popup = document.getElementById("sobre-popup");
  popup.style.display = "none";
}

document.getElementById("sobre-btn").addEventListener("click", openSobre);

document.getElementById("sobre-popup").addEventListener("scroll", function () {
  closeButton.style.visibility = this.scrollTop > 20 ? "visible" : "hidden";
});
