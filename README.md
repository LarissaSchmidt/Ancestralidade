# Ancestralidade

Sim, é possível utilizar os dados de `ancestry_string` que o relatório da Illumina (via **Microarray Analysis para PRS 1.1.3**) fornece como base para um **mapa de ancestralidade**, mas com algumas considerações técnicas e estratégicas importantes:

A pipeline utilizada pela Illumina incorpora alguma **análise de ancestralidade genética (ancestry inference)** – provavelmente baseada em dados de **referência de populações do projeto 1000 Genomes, HGDP, ou gnomAD**. As análises de ancestralidade genômica geralmente são feitas com base em **populações de referência**.

* O GSA (Global Screening Array) e outros chips da Illumina costumam incluir SNPs informativos para ancestralidade.

Alguns SNPs (polimorfismos de nucleotídeo único) são mais úteis do que outros para diferenciar populações do mundo. Esses SNPs têm frequências alélicas muito distintas entre grupos (por exemplo, um alelo comum em europeus e raro em asiáticos).
Esses SNPs são chamados de AIMs – Ancestry Informative Markers.
Chips como o Illumina GSA (Global Screening Array) já vêm com esses AIMs selecionados, o que permite rodar ferramentas como ADMIXTURE com boa acurácia na inferência de ancestralidade, mesmo com menos marcadores do que o genoma completo.
  
* Os softwares internos ou pipelines Illumina (ex: **GenomeStudio**, **DRAGEN**, ou cloud Illumina Connected Analysis\*\*) podem fazer essa inferência com ferramentas como:

  * **ADMIXTURE**
  * **PCA-based ancestry projection**
  * **SNPweights**

---

### Coluna `ancestry_string`:

1. **Criar visualizações geográficas e interativas**:

   * Um **mapa de calor ou pizza** de ancestralidade por continente (América, Europa, África, Ásia, etc.).
   * Criar mapas personalizados no estilo do MyHeritage, AncestryDNA, 23andMe, etc.

2. **Adicionar explicações interpretativas** no laudo:

   * "Seu DNA apresenta 70% de similaridade com populações europeias, 24% ameríndias, e 6% africanas, com base em dados genéticos de referência global."
   * Incluir um parágrafo explicativo sobre o significado genético e histórico dessas proporções.

3. **Aprofundar com ferramentas externas** (opcional):

   * Se quiser enriquecer com **mais resolução** (ex: distinguir Sul da Europa vs Norte), pode usar ferramentas como:

     * [ADMIXTURE](http://dalexander.github.io/admixture/)
     * [PCA com PLINK + R](https://www.cog-genomics.org/plink/)
     * [SNPRelate (Bioconductor R package)](https://bioconductor.org/packages/release/bioc/html/SNPRelate.html)
   * Para isso, seria necessário o **arquivo genotípico bruto (PLINK ou VCF)** derivado do IDAT.

---

### **Bloco visual e interpretativo:**

```
Ancestralidade Genética Estimada:

🧬 Europeu: 70%  
🧬 Ameríndio (Admixed American): 24%  
🧬 Africano: 6%

Interpretação:
Sua composição genética apresenta predominância de variantes associadas a populações europeias, com contribuição significativa de ancestrais ameríndios e pequena porcentagem africana. Essa distribuição pode influenciar o cálculo do risco poligênico, que é ajustado de acordo com grupos populacionais de referência.
```

#### **Mapa sugerido:**

* Um **mapa mundi** ou da **América Latina + Europa + África**, com bolhas percentuais.
* Alternativamente, um **gráfico de pizza colorido**, com legenda estilizada.

---

### ⚠️ Cuidados

* **Evite interpretações rígidas ou deterministas**. A ancestralidade genética não equivale à identidade étnica ou cultural.
* A terminologia `Admixed American` da Illumina **inclui população latino-americana com miscigenação** (e não apenas "indígenas").
* Sempre que possível, deixe claro que se trata de **estimativas baseadas em comparação genética com populações de referência**.

---
