# Adicionando suporte ao WSL (Windows Subsystem for Linux)

**1. No prompt de comando verificar distribuições instaladas e disponíveis:**

```ruby
wsl --list --verbose
wsl --list --online
```

**2. Instalar a distribuição Ubuntu:**

```ruby
wsl --install -d Ubuntu
```

**3. Verificar se o recurso VirtualMachinePlatform está habilitado:**

 ```ruby
DISM /Online /Get-Features /Format:Table | findstr VirtualMachinePlatform
```

Saída esperada: ```VirtualMachinePlatform | Enabled```

**4. Atualizar os pacotes do Ubuntu:**

```ruby
sudo apt update
sudo apt upgrade
```

**5. Navegar até a pasta de trabalho no Windows (exemplo):**

```ruby
cd /mnt/c/Users/Usuario/Downloads/Ancestralidade
```

# Instalando o ADMIXTURE

Iremos utilizar o ADMIXTURE, que é um programa para análise genética de populações, geralmente usado para estimar ancestrias e mistura genética.

**1. Atualizar o sistema:**

 ```ruby
sudo apt update && sudo apt upgrade -y
```

**2. Instalar ferramentas necessárias para compilar (caso não tenha o executável pronto):**

 ```ruby
sudo apt install build-essential
```

**3. Baixar o ADMIXTURE:**

 ```ruby
wget https://dalexander.github.io/admixture/binaries/admixture_linux-1.3.0.tar.gz
tar -xzvf admixture_linux-1.3.0.tar.gz
```

**4. Mova o executável para /usr/local/bin (local padrão para programas):**

 ```ruby
sudo mv dist/admixture_linux-1.3.0/admixture /usr/local/bin/admixture
```

**5. Dê permissão de execução para ele:**

```ruby
sudo chmod +x /usr/local/bin/admixture
```

**6. Teste se está funcionando:**

```ruby
admixture --help
```

O ADMIXTURE está instalado e funcionando corretamente no WSL, estando pronto para rodar análises genéticas.

# Preparando os arquivos para o ADMIXTURE

O ADMIXTURE trabalha com arquivos de entrada no formato **PLINK**, ou seja, ele espera os arquivos:

* **.bed** (binário de genótipos)

* **.bim** (informações dos SNPs)

* **.fam** (informações dos indivíduos)

Ele não lê diretamente arquivos *CSV*, *VCF* ou *IDAT*, então primeiro precisamos converter seus dados brutos para o formato **PLINK**. Para isso iremos utilizar a ferramenta **PLINK** para a conversão:

**1. Instale a ferramenta PLINK:**

```ruby
sudo apt install plink
sudo apt install putty-tools
wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20210606.zip

```

sudo apt install vcftools



Aperte a barra de espaço para marcar a opção [x]. Depois, pressione Enter para confirmar (<Ok>).
![image](https://github.com/user-attachments/assets/c5dfb7ef-dcbc-4a89-a321-0a69aac70230)


vcftools --vcf ZML274-001_InfiniumGSA_v3_GRCh37.vcf --plink --out arquivo

plink --file arquivo --make-bed --out arquivo_binario

```ruby
larissaschmidt@DESKTOP-UAKI6G4:/mnt/c/Users/Usuario/Downloads/Ancestralidade$ plink --file arquivo --make-bed --out arquivo_binario
PLINK v1.90b6.24 64-bit (6 Jun 2021)           www.cog-genomics.org/plink/1.9/
(C) 2005-2021 Shaun Purcell, Christopher Chang   GNU General Public License v3
Logging to arquivo_binario.log.
Options in effect:
  --file arquivo
  --make-bed
  --out arquivo_binario

3794 MB RAM detected; reserving 1897 MB for main workspace.
Possibly irregular .ped line.  Restarting scan, assuming multichar alleles.
.ped scan complete (for binary autoconversion).
Performing single-pass .bed write (653947 variants, 1 person).
--file: arquivo_binario-temporary.bed + arquivo_binario-temporary.bim +
arquivo_binario-temporary.fam written.
653947 variants loaded from .bim file.
1 person (0 males, 0 females, 1 ambiguous) loaded from .fam.
Ambiguous sex ID written to arquivo_binario.nosex .
Using 1 thread (no multithreaded calculations invoked).
Before main variant filters, 1 founder and 0 nonfounders present.
Calculating allele frequencies... done.
Warning: Nonmissing nonmale Y chromosome genotype(s) present; many commands
treat these as missing.
Total genotyping rate is 0.993506.
653947 variants and 1 person pass filters and QC.
Note: No phenotypes present.
--make-bed to arquivo_binario.bed + arquivo_binario.bim + arquivo_binario.fam
... done.
```

# Aplicando filtro de controle de qualidade e limpeza dos dados no PLINK

**1. Remover SNPs com muitos dados faltantes (--geno) (remove SNPs com >5% de dados faltantes):**

```ruby
plink --bfile arquivo_binario --geno 0.05 --make-bed --out arquivo_qc1
```

**2. Remover indivíduos com muitos dados faltantes (--mind) (remove indivíduos com >10% de dados faltantes):**

```ruby
plink --bfile arquivo_qc1 --mind 0.1 --make-bed --out arquivo_qc2
```

**3. Remover SNPs com baixa frequência alélica (--maf) (remove SNPs com frequência alélica menor que 1%):**

```ruby
plink --bfile arquivo_qc2 --maf 0.01 --make-bed --out arquivo_qc3
```

**4. Remover SNPs em desequilíbrio de Hardy-Weinberg (--hwe) (remove variantes fora do equilíbrio de Hardy-Weinberg):**

```ruby
plink --bfile arquivo_qc3 --hwe 1e-6 --make-bed --out arquivo_qc4
```

Arquivo final **arquivo_qc4** pronto para o ADMIXTURE.

Passo a passo básico para rodar ADMIXTURE:
Abra seu terminal na pasta onde estão os arquivos (arquivo_binario.bed, etc).

Rodar ADMIXTURE para um valor K (número de populações ancestrais) específico, por exemplo, K=3:

* **K** é o número de populações ancestrais hipotéticas que você quer modelar no seu conjunto de dados.

* O ADMIXTURE tenta explicar a composição genética de cada indivíduo como uma mistura de K grupos genéticos "puros" (populações ancestrais).

* Cada indivíduo recebe proporções que somam 100% distribuídas nesses K grupos.

# Como escolher o K ideal:

**1. Rode ADMIXTURE com a opção --cv para vários Ks:**

```ruby
admixture --cv arquivo_binario.bed 2
admixture --cv arquivo_binario.bed 3
admixture --cv arquivo_binario.bed 4
... e assim por diante.
```

ou

```ruby
for K in 2 3 4 5 6; do
  admixture --cv arquivo_qc4.bed $K | tee log${K}.out
done
```

Assim você terá os erros de cross-validation para decidir o melhor K.

O intervalo de valores de K testados no ADMIXTURE deve ser definido conforme o objetivo da análise e a complexidade das populações amostradas. Comumente, utiliza-se um range entre 2 e 6, pois esses valores costumam capturar as estruturas populacionais principais. Ao ampliar esse intervalo, é possível identificar substruturas populacionais mais detalhadas, porém isso pode dificultar a interpretação dos resultados e gerar artefatos, como grupos muito pequenos ou pouco representativos.

**2. Veja o resultado de CV que aparece no terminal, algo como:**

```ruby
CV error (K=2): 0.45
CV error (K=3): 0.38
CV error (K=4): 0.40
```

**3. O K que apresentar o menor erro CV é o que melhor explica a ancestralidade.**

# Por que é necessário um banco público com diversas amostras para realizar a análise

A análise de ancestralidade por meio do software **ADMIXTURE** baseia-se na comparação entre os genótipos da amostra de interesse e os genótipos de populações de referência. O principal objetivo do programa é estimar proporções de ancestralidade ao inferir componentes genéticos compartilhados com grupos populacionais previamente caracterizados.

Quando a análise é realizada apenas com as amostras individuais, sem a inclusão de um banco de referência diversificado, o modelo não dispõe de variabilidade genética suficiente para identificar padrões estruturais entre diferentes ancestrais. Isso compromete a capacidade do ADMIXTURE de estimar corretamente as proporções populacionais, já que ele depende da presença de agrupamentos genéticos bem definidos para gerar inferências robustas.

Por esse motivo, é essencial utilizar bancos de dados públicos contendo diversas amostras, representando diferentes populações humanas com ancestralidades bem caracterizadas. Esses bancos, além de amplamente utilizados na literatura científica, conferem validade estatística ao modelo e fornecem respaldo metodológico confiável, especialmente quando os resultados serão utilizados para fins laboratoriais ou para emissão de laudos técnicos com base científica.

O **IGSR (International Genome Sample Resource)** é um portal unificado que disponibiliza várias coleções de genomas humanos de referência, organizadas por projeto e versão. Entre essas coleções de dados ("Data Collections"), destacam-se importantes recursos para análises genômicas e de ancestralidade.

> https://www.internationalgenome.org/

Neste contexto, optou-se por integrar dois dos principais bancos de dados genômicos disponíveis: o **1000 Genomes Project** e o **Human Genome Diversity Project (HGDP)**, com o objetivo de criar um **painel de referência mais abrangente e representativo** para análises de ancestralidade com o ADMIXTURE. Para garantir a compatibilidade entre os conjuntos, ambos os bancos devem estar baseados na mesma versão do genoma de referência, o **GRCh37**, assegurando a equivalência posicional dos SNPs.

A unificação dos bancos exige ainda uma série de etapas de padronização, incluindo:

1. a identificação e retenção apenas dos **SNPs compartilhados** entre os dois conjuntos;

```ruby
plink --bfile 1000g_plink --extract common_snps.txt --make-bed --out 1000g_filtered
plink --bfile hgdp_plink --extract common_snps.txt --make-bed --out hgdp_filtered
```

Você pode gerar common_snps.txt com base no cruzamento entre os .bim dos dois arquivos.

2. a **remoção de SNPs monomórficos**, que não contribuem para a diferenciação populacional;

3. o **alinhamento dos alelos** por verificação de strand (**strand alignment**) para evitar erros de polaridade;

Utilize ferramentas como --flip no PLINK para alinhar strands, ou scripts específicos como genotype harmonizer se necessário

4. a **padronização dos identificadores (IDs)**, cromossomos e posições genômicas.

5. realizar o **merge**

```ruby
plink --bfile 1000g_filtered --bmerge hgdp_filtered --make-bed --out painel_ancestralidade
``` 

Esses cuidados metodológicos são fundamentais porque o ADMIXTURE requer conjuntos de dados consistentes e comparáveis entre si, com variações genéticas informativas entre os indivíduos, para que os componentes ancestrais sejam corretamente modelados. A ausência dessas etapas pode introduzir viés ou gerar erros nas estimativas de ancestralidade, comprometendo a validade dos resultados — especialmente em contextos clínicos, laboratoriais ou periciais, nos quais se exige evidência científica sólida.

# 1000 Genomes Project

O arquivo selecionado do **1000 Genomes Project** para compor o painel de referência foi o: ```ALL.chr1-22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz```

Este arquivo é um merge completo dos cromossomos 1 ao 22 e contém variantes genotipadas em **2.504 indivíduos** pertencentes a **26 populações distintas**, representando uma ampla diversidade genética global.

As variantes foram geradas com base na **referência genômica GRCh37/hg19**, assegurando compatibilidade com outros conjuntos que utilizam a mesma build. O processo de geração incluiu as seguintes etapas metodológicas:

* **Alinhamento das leituras** ao genoma de referência utilizando o **BWA (Burrows-Wheeler Aligner)**;

* **Faseamento dos haplótipos** com o software **ShapeIt2**;

* **Chamada de variantes conjunta (multi-sample calling)** utilizando o método **mvncall**, o que permite identificar variantes compartilhadas entre indivíduos;

* **Integração e filtragem** dos dados genotípicos, resultando em um conjunto de **SNPs e indels prontos para análises populacionais**, como aquelas realizadas com o software ADMIXTURE.

Além disso, a documentação oficial do projeto detalha que o arquivo contém importantes informações no formato VCF, como:

* **Profundidade total de leitura (read depth)** para cada variante, calculada a partir dos arquivos BAM por amostra, disponível no campo INFO do VCF, garantindo qualidade e suporte técnico para as chamadas das variantes;

* **Frequências alélicas globais e por superpopulação continental**, sendo os 2.504 indivíduos agrupados em cinco superpopulações (Africana – AFR, Europeia – EUR, Leste Asiática – EAS, Sul Asiática – SAS e Americana – AMR). Essas frequências são disponibilizadas no VCF por meio de campos específicos, permitindo análises refinadas da estrutura genética;

* **Informação do alelo ancestral (Ancestral Allele – AA)** inferido por métodos filogenéticos probabilísticos (Ortheus), que pode ser útil para estudos evolutivos e filogenéticos.

Esse arquivo é amplamente citado na literatura científica e foi desenvolvido especificamente para análises de estrutura populacional, ancestralidade e variação genética em larga escala. Sua utilização garante robustez estatística, reprodutibilidade e qualidade do conjunto de dados, especialmente em análises que requerem representatividade global e comparabilidade com estudos já consolidados. Dessa forma, as variantes presentes são confiáveis, amplamente anotadas e adequadas para a modelagem dos componentes genéticos com o software ADMIXTURE.

> Download: https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/

```ruby
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel
```

Script para baixar o banco completo 1000 Genomes

```ruby
#!/bin/bash
```

```ruby
mkdir -p 1000G_data
```

```ruby
cd 1000G_data
```

```ruby
for chr in {1..22}
do
    echo "Baixando cromossomo $chr..."
    wget -c ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
    wget -c ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi
done

echo "Download completo!"
```

# Human Genome Diversity Project (HGDP)

O arquivo selecionado do **Human Genome Diversity Project (HGDP)** 

> Download feito no link: https://www.internationalgenome.org/data-portal/data-collection/hgdp

# Convergência entre o 1000 Genomes Project e o HGDP para montar um painel conjunto







