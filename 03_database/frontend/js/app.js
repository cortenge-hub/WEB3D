const nomesTabelas = {
  edificios: "Edifícios",
  pavimentos: "Pavimentos",
  setores: "Setores",
  ambientes: "Ambientes",
  quadros: "Quadros",
  circuitos: "Circuitos",
  equipamentos: "Equipamentos",
  documentos: "Documentos",
  fotos360: "Fotos 360",
  modelos3d: "Modelos 3D",
  arquivos_ifc: "Arquivos IFC",
  arquivos_dxf: "Arquivos DXF",
  plantas: "Plantas",
  marcadores: "Marcadores",
  manutencoes: "Manutenções",
  inspecoes: "Inspeções",
  eventos: "Eventos",
  usuarios: "Usuários",
  configuracoes: "Configurações",
  sincronizacao: "Sincronização"
};

function abrirTabela(tabela) {
  const nome = nomesTabelas[tabela] || tabela;

  document.getElementById("abaAtual").innerText = nome;
  document.getElementById("tituloModulo").innerText = `Cadastro de ${nome}`;
  document.getElementById("descricaoModulo").innerText =
    `Tabela selecionada: ${tabela}. Próxima etapa: gerar formulário automático.`;

  document.getElementById("propTabela").innerText = tabela;
}