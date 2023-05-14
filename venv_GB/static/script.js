const toponimos = Array.from(document.querySelectorAll(".toponimo"));
const toponimo_display = document.querySelector("#top-display");
let toponimo_selecionado = document.getElementById("top-s");
const formulario = document.getElementById("formulario");

/**@param {MouseEvent} event */
function selecionarToponimo(event) {
  const toponimo_clicado = event.currentTarget.innerHTML;
  toponimo_display.innerHTML = '"' + toponimo_clicado + '"';
  toponimo_selecionado.value = toponimo_clicado;
  // sempre que escolher um novo toponimo para avaliar
  // matenha a pergunta 1 ativa e remova as demais
  pergunta1.style.display = "block";
  pergunta2.style.display = "none";
  pergunta3.style.display = "none";

  formulario.reset();

  // se nenhum toponimo estiver selecionado, remova a pergunta1
  if (toponimo_display === "Testando" || toponimo_display === "") {
    pergunta1.style.display = "none";
  }
}

if (toponimos) {
  toponimos.forEach((toponimo) =>
    toponimo.addEventListener("click", selecionarToponimo)
  );
}

// Seleciona estado da lista de estados
function selecionarEstado() {
  var listaEstados = document.getElementById("listaEstados");
  var estado = document.getElementById("pergunta3-respostas");
  estado.value = listaEstados.value;
  // estado = resposta da P3
}

// Seleciona tipo de toponimo da lista de tipos
function selecionarTipo() {
  var tipo = document.getElementById("pergunta2-respostas").value;
  document.getElementById("tipo-selecionado").value = tipo;
}

//____________________________________________________________________
// TESTES / WIP NOVAS FUNCIONALIDADES
const submit = document.getElementById("submit");
const pergunta1 = document.getElementById("pergunta-1");
const pergunta2 = document.getElementById("pergunta-2");
const pergunta3 = document.getElementById("pergunta-3");

const respostasP2 = document.getElementById("pergunta2-respostas");
const respostasP3 = document.getElementById("pergunta3-respostas");

// A funcao abaixo mostra ou nao a pergunta 2 e o botao de enviar
// com base na resposta da pergunta 1
function mostrarPergunta2(event) {
  // se a resposta da pergunta 1 for 'sim', 'nao-sei' ou vazia,
  // mostre a pergunta 2 e mantenha o submit desativado
  if (
    pergunta1.querySelector('input[name="pergunta-1"]:checked').value ===
      "sim" ||
    pergunta1.querySelector('input[name="pergunta-1"]:checked').value ===
      "nao-sei" ||
    pergunta1.querySelector('input[name="pergunta-1"]:checked').value === ""
  ) {
    pergunta2.style.display = "block";
    submit.disabled = true;
    submit.style.backgroundColor = "lightgray";
  }
  // se a resposta da pergunta 1 for 'nao',
  // remova a resposta das outras perguntas, matenha-as escondidas e ative o submit
  else {
    pergunta2.style.display = "none";
    respostasP2.value = "";
    pergunta3.style.display = "none";
    respostasP3.value = "";
    submit.disabled = false;
    submit.style.backgroundColor = "lightgreen";
  }
}
pergunta1.addEventListener("change", mostrarPergunta2);
//

// ADD COMENTARIO
function mostrarPergunta3(event) {
  if (pergunta2.value !== "") {
    pergunta3.style.display = "block";
  } else {
    pergunta3.style.display = "none";
  }
}
pergunta2.addEventListener("change", mostrarPergunta3);
//

function mostrarSubmit(event) {
  if (pergunta3.value !== "") {
    submit.disabled = false;
    submit.style.backgroundColor = "lightgreen";
  } else {
    submit.disabled = true;
  }
}
pergunta3.addEventListener("change", mostrarSubmit);

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

//

// function testeEnter() {
//   // const teste = document.querySelector("#top");
//   if (teste) {
//     teste.addEventListener("keydown", checkEnter);
//   }
// }

// function checkEnter(event) {
//   if (event.keyCode === 13) {
//     console.log("Tecla enter pressionada na caixa");
//     console.log(teste.value);
//     event.preventDefault();
//   }
// }
//____________________________________________________________________
