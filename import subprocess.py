import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os

# ===== CONFIGURAÇÕES =====
vcf_input = "seus_dados.vcf"       # <- Coloque o nome do seu VCF aqui
prefix = "saida_admixture"
k = 3

# ===== 1. CONVERTE VCF PARA PLINK =====
print("🔄 Convertendo VCF para formato PLINK...")
plink_cmd = f"plink --vcf {vcf_input} --make-bed --out {prefix}"
plink_status = subprocess.run(plink_cmd, shell=True)

if plink_status.returncode != 0:
    print("❌ Erro na conversão com PLINK.")
    exit()

# ===== 2. RODA ADMIXTURE =====
print(f"🧬 Rodando ADMIXTURE com K={k}...")
admixture_cmd = f"admixture {prefix}.bed {k} --cv"
admixture_status = subprocess.run(admixture_cmd, shell=True)

if admixture_status.returncode != 0:
    print("❌ Erro ao rodar ADMIXTURE.")
    exit()

# ===== 3. LÊ O RESULTADO =====
q_file = f"{prefix}.{k}.Q"
if not os.path.exists(q_file):
    print("❌ Arquivo de saída .Q não encontrado.")
    exit()

print(f"✅ Análise concluída. Resultados salvos em: {q_file}")

# ===== 4. MOSTRA GRÁFICO DE ANCESTRALIDADE =====
print("📊 Gerando gráfico de barras com proporções...")

q = pd.read_csv(q_file, delim_whitespace=True, header=None)
q.columns = [f"Pop_{i+1}" for i in range(q.shape[1])]

# Gráfico de barras empilhadas
q.plot(kind='bar', stacked=True, figsize=(10,5), colormap='tab10')
plt.title(f"Proporções de Ancestralidade (K={k})")
plt.ylabel("Proporção")
plt.xlabel("Indivíduos")
plt.xticks([], [])
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

#update 