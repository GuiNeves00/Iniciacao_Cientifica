let testejson = {
  id: 0,
  texto: "João Monlevade fica em Minas Gerais, perto de Nova Era.",
  toponimosGP: ["João Monlevade", "Minas Gerais", "em"],
  toponimosUsuario: {
    nomeToponimo: ["João Monlevade", "em", "Minas Gerais", "Nova Era"],
    isToponimo: [true, false, true, true],
    tipoToponimo: ["Cidade", "null", "Estado", "Cidade"],
    estadoToponimo: ["MG", "null", "MG", "MG"],
  },
};

console.log(testejson);
console.log("________________________________________________");
console.log(
  testejson.toponimosUsuario.nomeToponimo[0],
  testejson.toponimosUsuario.isToponimo[0],
  testejson.toponimosUsuario.tipoToponimo[0],
  testejson.toponimosUsuario.estadoToponimo[0]
);
