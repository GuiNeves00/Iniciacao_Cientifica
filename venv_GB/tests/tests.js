let testejson = {
  metadados: "teste",
  id: 0,
  titulo: "Uma notícia sobre o interior de Minas Gerais",
  subtitulo: "Saiba mais sobre João Monlevade",
  texto: "João Monlevade fica em Minas Gerais, perto de Nova Era.",
  toponimosGP: ["João Monlevade", "Minas Gerais", "em"],
  contribuicoes: [
    ["João Monlevade", "Toponimo", "Cidade", "MG", 10],
    ["em", "Palavra", null, null, 5],
    ["Minas Gerais", "Toponimo", "Estado", "MG", 20],
    ["Nova Era", "Toponimo", "Cidade", "MG", 10],
  ],
  totalContribuicoes: 45,
};

console.log(testejson);
console.log("________________________________________________");
console.log(testejson.contribuicoes[0]);
