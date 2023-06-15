const testeJSON = `{
  "id": 1,
  "metadados": "wip",
  "url": "noticia.com/ex-noticia",
  "pubdate": "Wed, 03 May 2023 13:33:00 -0000",
  "titulo":
    "Crianças autistas participam de sessão de terapia com cães do Bope em Macapá",
  "subtitulo":
    "Ação foi realizada na manhã desta sexta-feira (28). Segundo o Creap, atividade chamada de cinoterapia promove diversos benefícios, como saúde física e mental dos pacientes.",
  "texto":
    "Crianças autistas receberam nesta sexta-feira (28) uma atividade terapêutica com cães do Batalhão de Operações Especiais (Bope) da Polícia Militar (PM) do Amapá. A iniciativa ocorreu no Canil do Bope. O local fica situado no Comando Geral da PM, no bairro do Beirol, na Zona Sul de Macapá. Segundo Mário Coimbra, coordenador de reabilitação do Creap, a atividade chamada de cinoterapia promove diversos benefícios, como a saúde física e mental dos pacientes. 'Os benefícios se dão através do contato e a troca de afeto; o prazer de rir brincar com um animal a sensação de bem-estar e conforto e, principalmente para a criança com autismo, os estímulos sensoriais físicos e emocionais que vão auxiliar na terapêutica que ele já realiza no Creap diariamente', disse o coordenador. Além de atender crianças com autismo, o evento ainda contou com a participação da pequena Daniela, que tem 1 ano de idade e é portadora da Síndrome de Down. A mãe dela, a fonoaudióloga Valquíria Câmara, falou sobre a importância do momento. 'O projeto, ele é muito importante porque ele traz é uma vivência diferente, né? E assim, você entra em contato com animais e isso estimula muito a criança, no desenvolvimento geral dela [...] é um momento que essas crianças dão o melhor de si', disse Daniela. A ação faz parte do projeto Melhor Amigo, que iniciou em 2019, mas teve de ser interrompido no ano seguinte por conta da pandemia de Covid-19. Após o fim das medidas restritivas, a cinoterapia com as crianças autistas retornou em 2023. Segundo Lino Medeiros, capitão do canil do Bope, a ideia é que a prática volte a ocorrer mais vezes este ano, mas a frequência será definida pelos profissionais de saúde. As atividades desta sexta foram realizadas em conjunto entre o Creap e o Bope. Veja o plantão de últimas notícias do g1 Amapá",
  "spacy": [
    "Bope",
    "Macapá",
    "Creap",
    "Bope",
    "Polícia Militar",
    "PM",
    "Amapá",
    "Canil do Bope",
    "Comando Geral da PM",
    "Beirol",
    "Zona Sul",
    "Macapá",
    "Creap",
    "Creap",
    "Covid-19",
    "Bope",
    "Creap",
    "Bope"
  ],
  "contribuicoes": [
    ["Bope", "N", null, null, "Macapá", "S", "Cidade", "Amapá", "Creap", "N", null, null, "Polícia Militar", "N", null, null, "PM", "N", null, null, "Amapá", "S", "Estado", "Amapá", "Comando Geral da PM", "S", "Bairro", "Rio de Janeiro", "Beirol", "S", "Bairro", "Amapá", "Zona Sul", "S", "Zona", null, "Mário Coimbra", "S", "Rua", "São Paulo"],
  ["Bope", "N", null, null, "Macapá", "S", "Cidade", "Amapá", "Creap", "S", "Rua", "Minas Gerais", "Polícia Militar", "N", null, null, "PM", "N", null, null, "Amapá", "S", "Estado", "Amapá", "Comando Geral da PM", "N", null, null, "Beirol", "S", "Bairro", "Amapá", "Zona Sul", "S", "Zona", null],
  ["Bope", "N", null, null, "Macapá", "S", "Cidade", "Amapá", "Creap", "S", "Bairro", "Espirito Santo", "Polícia Militar", "N", null, null, "PM", "N", null, null, "Amapá", "S", "Estado", "Amapá", "Comando Geral da PM", "N", null, null, "Beirol", "S", "Rua", "Bahia", "Zona Sul", "N", null, null]
  ],
  "totalContribuicoes": 3
}
`;

// const teste = JSON.parse(testeJSON);
// console.log(teste.contribuicoes[0]);

// Versao "tuplas"
// const testeTuplas = `{
//   "id": 1,
//   "metadados": "wip",
//   "url": "noticia.com/ex-noticia",
//   "pubdate": "Wed, 03 May 2023 13:33:00 -0000",
//   "titulo":
//   "Crianças autistas participam de sessão de terapia com cães do Bope em Macapá",
//   "subtitulo":
//   "Ação foi realizada na manhã desta sexta-feira (28). Segundo o Creap, atividade chamada de cinoterapia promove diversos benefícios, como saúde física e mental dos pacientes.",
//   "texto":
//   "Crianças autistas receberam nesta sexta-feira (28) uma atividade terapêutica com cães do Batalhão de Operações Especiais (Bope) da Polícia Militar (PM) do Amapá. A iniciativa ocorreu no Canil do Bope. O local fica situado no Comando Geral da PM, no bairro do Beirol, na Zona Sul de Macapá. Segundo Mário Coimbra, coordenador de reabilitação do Creap, a atividade chamada de cinoterapia promove diversos benefícios, como a saúde física e mental dos pacientes. 'Os benefícios se dão através do contato e a troca de afeto; o prazer de rir brincar com um animal a sensação de bem-estar e conforto e, principalmente para a criança com autismo, os estímulos sensoriais físicos e emocionais que vão auxiliar na terapêutica que ele já realiza no Creap diariamente', disse o coordenador. Além de atender crianças com autismo, o evento ainda contou com a participação da pequena Daniela, que tem 1 ano de idade e é portadora da Síndrome de Down. A mãe dela, a fonoaudióloga Valquíria Câmara, falou sobre a importância do momento. 'O projeto, ele é muito importante porque ele traz é uma vivência diferente, né? E assim, você entra em contato com animais e isso estimula muito a criança, no desenvolvimento geral dela [...] é um momento que essas crianças dão o melhor de si', disse Daniela. A ação faz parte do projeto Melhor Amigo, que iniciou em 2019, mas teve de ser interrompido no ano seguinte por conta da pandemia de Covid-19. Após o fim das medidas restritivas, a cinoterapia com as crianças autistas retornou em 2023. Segundo Lino Medeiros, capitão do canil do Bope, a ideia é que a prática volte a ocorrer mais vezes este ano, mas a frequência será definida pelos profissionais de saúde. As atividades desta sexta foram realizadas em conjunto entre o Creap e o Bope. Veja o plantão de últimas notícias do g1 Amapá",
//   "spacy": [
//     "Bope",
//     "Macapá",
//     "Creap",
//     "Bope",
//     "Polícia Militar",
//     "PM",
//     "Amapá",
//     "Canil do Bope",
//     "Comando Geral da PM",
//     "Beirol",
//     "Zona Sul",
//     "Macapá",
//     "Creap",
//     "Creap",
//     "Covid-19",
//     "Bope",
//     "Creap",
//     "Bope",
//     "Amapá"
//   ],
//   "contribuicoes": [
//     [
//       ("Bope", "N", null, null),
//       ("Macapá", "S", "Cidade", "Amapá"),
//       ("Creap", "N", null, null),
//       ("Polícia Militar", "N", null, null),
//       ("PM", "N", null, null),
//       ("Amapá", "S", "Estado", "Amapá"),
//       ("Comando Geral da PM", "S", "Bairro", "Rio de Janeiro"),
//       ("Beirol", "S", "Bairro", "Amapá"),
//       ("Zona Sul", "S", "Zona", null),
//       ("Mário Coimbra", "S", "Rua", "São Paulo")
//     ],
//     [
//       ("Bope", "N", null, null),
//       ("Macapá", "S", "Cidade", "Amapá"),
//       ("Creap", "S", "Rua", "Minas Gerais"),
//       ("Polícia Militar", "N", null, null),
//       ("PM", "N", null, null),
//       ("Amapá", "S", "Estado", "Amapá"),
//       ("Comando Geral da PM", "N", null, null),
//       ("Beirol", "S", "Bairro", "Amapá"),
//       ("Zona Sul", "S", "Zona", null)
//     ],
//     [
//       ("Bope", "N", null, null),
//       ("Macapá", "S", "Cidade", "Amapá"),
//       ("Creap", "S", "Bairro", "Espirito Santo"),
//       ("Polícia Militar", "N", null, null),
//       ("PM", "N", null, null),
//       ("Amapá", "S", "Estado", "Amapá"),
//       ("Comando Geral da PM", "N", null, null),
//       ("Beirol", "S", "Rua", "Bahia"),
//       ("Zona Sul", "N", null, null)
//     ]
//   ],
//   "totalContribuicoes": 3
// }`;

// const teste = JSON.parse(testeTuplas);
// console.log(teste.contribuicoes);

const info = {
  id: 1,
  metadados: "wip",
  url: "noticia.com/ex-noticia",
  pubdate: "Wed, 03 May 2023 13:33:00 -0000",
  titulo: "Evento acadêmico no ICEA",
  subtitulo: "O evento será gratuito a todos",
  texto:
    "Acontecerá um evento acadêmico na UFOP da cidade de João Monlevade, com presenças de professores da unidade de Mariana. Participe.",
  spacy: ["UFOP", "João Monlevade", "Mariana"],
  contribuicoes: [
    [
      //usuario 1
      {
        //palavra 1
        Palavra: "UFOP",
        Toponimo: false,
        Tipo: null,
        Localizacao: null,
      },
      {
        //palavra 2
        Palavra: "João Monlevade",
        Toponimo: true,
        Tipo: "Cidade",
        Localizacao: "MG",
      },
      {
        //palavra 3
        Palavra: "Mariana",
        Toponimo: true,
        Tipo: "Cidade",
        Localizacao: "MG",
      },
    ],
    [
      //usuario 2
      {
        //palavra 1
        Palavra: "UFOP",
        Toponimo: true,
        Tipo: "Rua",
        Localizacao: "MG",
      },
      {
        //palavra 2
        Palavra: "João Monlevade",
        Toponimo: true,
        Tipo: "Cidade",
        Localizacao: "MG",
      },
      {
        //palavra 3
        Palavra: "Mariana",
        Toponimo: false,
        Tipo: null,
        Localizacao: null,
      },
    ],
    [
      //usuario 3
      {
        //palavra 1
        Palavra: "UFOP",
        Toponimo: false,
        Tipo: null,
        Localizacao: null,
      },
      {
        //palavra 2
        Palavra: "João Monlevade",
        Toponimo: false,
        Tipo: null,
        Localizacao: "MG",
      },
      {
        //palavra 3
        Palavra: "Mariana",
        Toponimo: true,
        Tipo: "Cidade",
        Localizacao: null,
      },
    ],
  ],
  totalContribuicoes: 3,
};

console.log(info.contribuicoes[0]);
