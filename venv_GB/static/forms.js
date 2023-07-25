console.log("dentro do arquivo form.js");

document
  .getElementById("formulario")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Coleta os dados do formulário
    var formData = new FormData(this);
    var respostasUsuario = {};

    // Converte os dados do formulário para JSON
    for (var [key, value] of formData.entries()) {
      switch (key) {
        case "top-selecionado":
          respostasUsuario["palavra"] = value;
          break;
        case "pergunta-1":
          respostasUsuario["is_toponimo"] = value;
          break;
        case "pergunta-2":
          respostasUsuario["tipo"] = value;
          break;
        case "pergunta-3":
          respostasUsuario["localizacao"] = value;
          break;
        default:
          respostasUsuario[key] = value;
      }
    }

    console.log(respostasUsuario); // Verifique se as respostas do usuário estão corretas

    // Envia os dados do formulário e os dados existentes como JSON
    fetch("/load-data")
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Falha ao carregar dados existentes.");
        }
      })
      .then(function (existingData) {
        // Adicionar as novas respostas do usuário aos dados existentes
        existingData.push(respostasUsuario);
        console.log("EXISTING DATA: ", existingData);

        // Enviar os dados atualizados para o servidor
        return fetch("/submit-form", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(existingData),
        });
      })
      .then(function (response) {
        if (response.ok) {
          alert("Respostas salvas com sucesso!");
        } else {
          throw new Error("Ocorreu um erro ao salvar as respostas.");
        }
      })
      .catch(function (error) {
        alert(error.message);
        console.log(error);
      });
  });

// document
//   .getElementById("formulario")
//   .addEventListener("submit", function (event) {
//     event.preventDefault(); // Impede o envio padrão do formulário

//     // Coleta os dados do formulário
//     var formData = new FormData(this);
//     var respostasUsuario = [];
//     var jsonData = {};

//     // Converte os dados do formulário para JSON
//     for (var [key, value] of formData.entries()) {
//       jsonData[key] = value;
//     }

//     respostasUsuario.push(jsonData);
//     console.log(respostasUsuario);

//     // Carregar dados existentes do arquivo JSON
//     fetch("/load-data", {
//       method: "GET",
//       headers: {
//         "Content-Type": "application/json",
//       },
//     })
//       .then(function (response) {
//         if (!response.ok) {
//           throw new Error("Falha ao carregar dados existentes.");
//         }
//         return response.json();
//       })
//       .then(function (existingData) {
//         // Adicionar as novas respostas do usuário aos dados existentes
//         existingData.push(...respostasUsuario);
//         console.log("EXISTING DATA: " + existingData);
//         // Salvar o array atualizado no arquivo JSON
//         return fetch("/submit-form", {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify(existingData),
//         });
//       })
//       .then(function (response) {
//         if (response.ok) {
//           alert("Respostas salvas com sucesso!");
//         } else {
//           alert("Ocorreu um erro ao salvar as respostas.");
//         }
//       })
//       .catch(function (error) {
//         alert("Ocorreu um erro ao salvar as respostas.");
//         console.log(error);
//       });
//   });

// VERSAO SAFE!
// document
//   .getElementById("formulario")
//   .addEventListener("submit", function (event) {
//     event.preventDefault(); // Impede o envio padrão do formulário

//     // Coleta os dados do formulário
//     var formData = new FormData(this);
//     var respostasUsuario = [];
//     var jsonData = {};

//     // Converte os dados do formulário para JSON
//     for (var [key, value] of formData.entries()) {
//       jsonData[key] = value;
//     }

//     respostasUsuario.push(jsonData);
//     console.log(respostasUsuario);

//     // Envia os dados do formulário como JSON
//     fetch("/submit-form", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(respostasUsuario),
//     })
//       .then(function (response) {
//         if (response.ok) {
//           alert("Respostas salvas com sucesso!");
//         } else {
//           alert("Ocorreu um erro ao salvar as respostas.");
//         }
//       })
//       .catch(function (error) {
//         alert("Ocorreu um erro ao salvar as respostas.");
//         console.log(error);
//       });
//   });
