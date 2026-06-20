# Visualizador 3D de Quadros Elétricos - Template Google Drive/CSV

## Estrutura de pastas sugerida no Google Drive

Quadros_Eletricos_3D/
├── 01_CSV_DATABASE/
│   ├── 01_QUADROS.csv
│   ├── 02_CIRCUITOS.csv
│   ├── 03_PAVIMENTOS.csv
│   ├── 04_PLANTAS.csv
│   ├── 05_FOTOS360.csv
│   ├── 06_DOCUMENTOS.csv
│   ├── 07_LOCAIS.csv
│   ├── 08_OBJETOS3D.csv
│   └── 09_EVENTOS.csv
├── 02_ASSETS/
│   ├── 01_PLANTAS_SVG/
│   ├── 02_PLANTAS_PNG/
│   ├── 03_MODELOS_GLB_GLTF/
│   ├── 04_IFC/
│   ├── 05_DXF/
│   ├── 06_FOTOS360/
│   └── 07_DOCUMENTOS_PDF/
└── visualizador_3d_quadros_csv.html

## Como testar localmente

Por segurança, navegadores podem bloquear leitura de CSV local quando o HTML é aberto com duplo clique.
Use um servidor local:

1. Extraia este ZIP.
2. Abra o terminal dentro da pasta extraída.
3. Execute:

python -m http.server 8000

4. Abra no navegador:

http://localhost:8000/visualizador_3d_quadros_csv.html

## Como usar Google Sheets como CSV público

Para cada aba da planilha, publique como CSV ou use o link:

https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/export?format=csv&gid=GID_DA_ABA

Depois substitua as URLs no bloco CSV_URLS dentro do HTML.

## Observação sobre Google Drive e arquivos 3D

Google Drive funciona para teste, mas pode falhar em alguns navegadores por CORS, confirmação de download ou MIME type.
Para GLB/GLTF em produção, prefira hospedagem estática: GitHub Pages, Netlify, Firebase Hosting, Google Cloud Storage ou servidor próprio.

## Formatos

SVG: recomendado para planta baixa.
PNG: recomendado apenas como imagem de fundo simples.
GLB/GLTF: recomendado para objetos 3D na web.
IFC: recomendado para BIM, mas exige loader específico ou conversão para GLB.
DXF: recomendado como intercâmbio CAD; para web, converter para SVG ou GLB.
