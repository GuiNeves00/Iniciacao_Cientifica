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
  submit.style.backgroundColor = "lightgray";
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

// Faz com que a palavra avaliada mude de cor apos o envio do formulario
formulario.addEventListener("submit", function (event) {
  event.preventDefault();

  if (toponimo_clicado_estilo) {
    toponimo_clicado_estilo.style.backgroundColor = "lightgreen";
    toponimo_clicado_estilo = null;
  }
});
//_________________________________________________________________

// Exibir quantos possíveis toponimos existem na noticia
window.onload = function () {
  var qntdToponimos = toponimos.length;
  alert("Existem " + qntdToponimos + " possíveis topônimos nesta notícia");
  exibirDialogo();
};

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

// Obtendo dados para escrever no BD
// const formularioBD = document.getElementById("formulario");

// function obterRespostas(event, toponimo_selecionado) {
//   var opcoesP1 = document.querySelectorAll('input[name="pergunta1"]');
//   var respostaP1;
//   opcoesP1.forEach(function (opcao) {
//     if (opcao.checked) {
//       respostaP1 = opcao.value;
//     }
//   });
//   console.log("Resposta P1: " + respostaP1);

//   var respostaP2 = document.getElementById("pergunta2-respostas").value;
//   console.log("Resposta P2: " + respostaP2);

//   var respostaP3 = document.getElementById("listaEstados").value;
//   console.log("Resposta P3: " + respostaP3);

//   var respostasUsuario = {
//     pergunta1: respostaP1,
//     pergunta2: respostaP2,
//     pergunta3: respostaP3,
//   };

//   // escreverRespostas(respostasUsuario);

//   // this.submit();
// }

// if (formularioBD) {
//   formularioBD.addEventListener("submit", obterRespostas);
// }

// _________________________________________________________

// Manipulacao e "UX" no Formulario
const submit = document.getElementById("submit");
const pergunta1 = document.getElementById("pergunta-1");
const pergunta2 = document.getElementById("pergunta-2");
const pergunta3 = document.getElementById("pergunta-3");

const respostaP2 = document.getElementById("pergunta2-respostas");
const respostaP3 = document.getElementById("pergunta3-respostas");

// A funcao abaixo mostra ou nao a pergunta 2 e o botao de enviar
// com base na resposta da pergunta 1
function mostrarPergunta2(event) {
  // se a resposta da pergunta 1 for 'sim', 'nao-sei' ou vazia,
  // mostre a pergunta 2 e mantenha o submit desativado
  if (
    pergunta1.querySelector('input[name="pergunta-1"]:checked').value === "sim"
  ) {
    pergunta2.style.display = "block";
    submit.disabled = true;
    submit.style.backgroundColor = "lightgray";
  }
  // se a resposta da pergunta 1 for 'nao',
  // remova a resposta das outras perguntas, matenha-as escondidas e ative o submit
  else {
    pergunta2.style.display = "none";
    respostaP2.value = "";
    pergunta3.style.display = "none";
    respostaP3.value = "";
    submit.disabled = false;
    submit.style.backgroundColor = "lightgreen";
  }
}
pergunta1.addEventListener("change", mostrarPergunta2);
//...

// Mostrar pergunta 3 apos pergunta 2 ter sido respondida
function mostrarPergunta3(event) {
  if (pergunta2.value !== "") {
    pergunta3.style.display = "block";
  } else {
    pergunta3.style.display = "none";
  }
}
pergunta2.addEventListener("change", mostrarPergunta3);
//...

// Disponibiliza o botão de submit apos a pergunta 3 ter sido respondida
function mostrarSubmit(event) {
  if (pergunta3.value !== "") {
    submit.disabled = false;
    submit.style.backgroundColor = "lightgreen";
  } else {
    submit.disabled = true;
  }
}
pergunta3.addEventListener("change", mostrarSubmit);
//_________________________________________________________________

// Testando ação quando usuário clica em próxima notícia
const continuar = document.getElementById("continuar");

/** @param {MouseEvent} event */
function continuarAvaliando(event) {
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
