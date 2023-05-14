const toponimos = Array.from(document.querySelectorAll(".toponimo"));
const toponimo_display = document.querySelector("#top-display");
let toponimo_selecionado = document.getElementById("top-s");
const formulario = document.getElementById("formulario");

/**@param {MouseEvent} event */
function selecionarToponimo(event) {
  const toponimo_clicado = event.currentTarget.innerHTML;
  toponimo_display.innerHTML = '"' + toponimo_clicado + '"';
  toponimo_selecionado.value = toponimo_clicado;

  formulario.reset();
}

if (toponimos) {
  toponimos.forEach((toponimo) =>
    toponimo.addEventListener("click", selecionarToponimo)
  );
}

// Seleciona estado da lista de estados
function selecionarEstado() {
  var listaEstados = document.getElementById("listaEstados");
  var estado = document.getElementById("estado");
  estado.value = listaEstados.value;
}

// Seleciona tipo de toponimo da lista de tipos
function selecionarTipo() {
  var tipo = document.getElementById("tipo").value;
  document.getElementById("tipo-selecionado").value = tipo;
}

//____________________________________________________________________
// TESTES / WIP NOVAS FUNCIONALIDADES

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

// Testando ação quando usuário tecla enter.
const teste = document.getElementById("novo-toponimo");

/** @param {KeyboardEvent} event */
function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    toponimo_selecionado.value = teste.value;
    toponimo_display.innerHTML = '"' + teste.value + '"';
    teste.value = ""; //limpa caixa de texto
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
