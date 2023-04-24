const toponimos = Array.from(document.querySelectorAll(".toponimo"));
const toponimo_ajuste = document.querySelector("#top-ajuste");
// for (let i = 0; i < toponimos.length; i++) {
//   console.log(toponimos[i].innerHTML);
// }

/**@param {MouseEvent} event */
function avaliartoponimo(event) {
  const toponimo_clicado = event.currentTarget.innerHTML;
  toponimo_ajuste.innerHTML = '"' + toponimo_clicado + '"';
}

if (toponimos) {
  toponimos.forEach((toponimo) =>
    toponimo.addEventListener("click", avaliartoponimo)
  );
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
const teste = document.querySelector("#top");
function testeEnter() {
  // const teste = document.querySelector("#top");
  if (teste) {
    teste.addEventListener("keydown", checkEnter);
  }
}

function checkEnter(event) {
  if (event.keyCode === 13) {
    console.log("Tecla enter pressionada na caixa");
    console.log(teste.value);
  }
}
//____________________________________________________________________
