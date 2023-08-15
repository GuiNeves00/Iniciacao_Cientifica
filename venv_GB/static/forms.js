console.log("dentro do arquivo form.js");

var indice = -1;
var existingData = [];

/**@param {MouseEvent} event */
function obterIndice(event) {
  var valor = event.currentTarget;
  indice = toponimos.indexOf(valor);
  console.log("INDICE: ", indice);
}

const toponimos_forms = Array.from(document.querySelectorAll(".toponimo"));
if (toponimos_forms) {
  toponimos_forms.forEach((toponimo) =>
    toponimo.addEventListener("click", obterIndice)
  );
}

var tamLista = toponimos_forms.length;
// var respostasUsuario = new Array(tamLista).fill({});
var respostasUsuario = [];
for (var i = 0; i < tamLista; i++) {
  respostasUsuario.push({});
}

document
  .getElementById("formulario")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Coleta os dados do formulário
    var formData = new FormData(this);
    var novoObjeto = {};

    // Converte os dados do formulário para JSON
    for (var [key, value] of formData.entries()) {
      if (indice === undefined) {
        // Se o índice for indefinido, crie um novo objeto e adicione os valores correspondentes
        switch (key) {
          case "top-selecionado":
            novoObjeto["palavra"] = value;
            break;
          case "pergunta-1":
            novoObjeto["is_toponimo"] = value;
            break;
          case "pergunta-2":
            novoObjeto["tipo"] = value;
            break;
          case "pergunta-3":
            novoObjeto["localizacao"] = value;
            break;
          default:
            novoObjeto[key] = value;
        }
      } else {
        // Caso contrário, atualize os valores no objeto existente no índice especificado
        switch (key) {
          case "top-selecionado":
            respostasUsuario[indice]["palavra"] = value;
            break;
          case "pergunta-1":
            respostasUsuario[indice]["is_toponimo"] = value;
            break;
          case "pergunta-2":
            respostasUsuario[indice]["tipo"] = value;
            break;
          case "pergunta-3":
            respostasUsuario[indice]["localizacao"] = value;
            break;
          default:
            respostasUsuario[indice][key] = value;
        }
      }
    }
    // Se o indice for indefinido, significa que anteriormente, no loop acima foi adicionado dados ao novoObjeto, portanto o adicionamos em respostasUsuario
    if (indice === undefined) {
      respostasUsuario.push(novoObjeto);
    }
    indice = undefined; // Smp q usuario selecionar toponimo o valor sera alterado. Portanto garantimos que seja indefinido por padrao
    console.log("respostaUsuario DOIS : ", respostasUsuario); // Verifique se as respostas do usuário estão corretas

    // Envia os dados do formulário e os dados existentes como JSON
    // fetch("/load-data")
    //   .then(function (response) {
    //     if (response.ok) {
    //       return response.json();
    //     } else {
    //       throw new Error("Falha ao carregar dados existentes.");
    //     }
    //   })
    //   .then(function (data) {
    //     // Adicionar as novas respostas do usuário aos dados existentes
    //     existingData = data;
    //     console.log("EXISTING DATA: ", existingData);

    //     // Enviar os dados atualizados para o servidor
    //     return fetch("/submit-form", {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(existingData),
    //     });
    //   })
    //   .then(function (response) {
    //     if (response.ok) {
    //       // Push the individual responses to the existingData array
    //       existingData.push(...respostasUsuario);
    //       console.log("EXISTING DATA: ", existingData);

    //       // Send the updated data to the server
    //       return fetch("/submit-form", {
    //         method: "POST",
    //         headers: {
    //           "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify(existingData),
    //       });
    //     } else {
    //       throw new Error("Ocorreu um erro ao salvar as respostas.");
    //     }
    //   })
    //   .catch(function (error) {
    //     alert(error.message);
    //     console.log(error);
    //   });

    // NOVA TENTATIVA DO EDIT
    fetch("/salvar_json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(respostasUsuario),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message); // Deve imprimir "JSON gravado com sucesso!"
      })
      .catch((error) => {
        console.error("Erro ao enviar os dados:", error);
      });
  });
