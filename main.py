"""
LISTA DE EXERCÍCIOS 2 - Análise Exploratória e Desbalanceamento de Dados
Base: Sistema de Informação de Mortalidade (SIM) - 2024
Autor: Arlen Ferreira da Silva Filho
Curso: Sistemas de Informação - UFPE
Data: 19/10/2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import resample

# -------------------------------------------------------------------
# 1️⃣ Leitura e informações iniciais
# -------------------------------------------------------------------

print("Análise - Lista 2 (SIM 2024)")
print("Fonte: Ministério da Saúde / DATASUS")
print("-------------------------------------------------------------")

# Leitura do CSV
df = pd.read_csv("SIM2024.csv", sep=";", encoding="latin1")

# -------------------------------------------------------------------
# 2️⃣ Questão 1 - Campo ASSISTMED
# -------------------------------------------------------------------
print("\n1ª Questão - Campo ASSISTMED")

# (i) Significado (segundo Dicionário SIM 2025)
descricao_assistmed = """
O campo ASSISTMED indica se o falecido recebeu assistência médica
durante a doença que ocasionou a morte.
Valores possíveis:
1 – Sim
2 – Não
9 – Ignorado
"""

print(descricao_assistmed)

# (ii) Gráfico de distribuição
plt.figure(figsize=(6,4))
df["ASSISTMED"].value_counts(dropna=False).sort_index().plot(
    kind="bar", color=["steelblue", "indianred", "gray"]
)
plt.title("Distribuição dos valores do campo ASSISTMED")
plt.xlabel("Código (1=Sim, 2=Não, 9=Ignorado)")
plt.ylabel("Frequência")
plt.show()

# (iii) Observação
print("""
Observa-se que a maior parte dos registros indica que houve assistência médica.
Isso sugere que a maioria dos óbitos ocorreu em contextos com acompanhamento
profissional, embora ainda exista um percentual de casos sem atendimento
ou sem informação (9 = ignorado).
""")

# -------------------------------------------------------------------
# 3️⃣ Questão 2 - Campo CAUSABAS
# -------------------------------------------------------------------
print("\n2ª Questão - Campo CAUSABAS")

# (i) Significado
descricao_causabas = """
O campo CAUSABAS representa o código da causa básica da morte,
segundo a Classificação Internacional de Doenças (CID-10).
Exemplo: C500 = Neoplasia maligna da mama.
"""
print(descricao_causabas)

# (ii) Organização e top 5
print("Organização: os códigos seguem o padrão da CID-10, com uma letra e três dígitos.")

top5 = df["CAUSABAS"].value_counts().head(5)
print("\nTop 5 causas básicas mais frequentes:")
print(top5)

plt.figure(figsize=(7,4))
sns.barplot(x=top5.index, y=top5.values, palette="crest")
plt.title("5 causas básicas mais frequentes (CAUSABAS)")
plt.xlabel("Código CID-10")
plt.ylabel("Frequência")
plt.show()

print("""
Esses códigos representam as doenças mais frequentemente registradas
como causa básica de óbito no conjunto de dados analisado.
""")

# -------------------------------------------------------------------
# 4️⃣ Questão 3 - Balanceamento dos dados (CAUSABAS)
# -------------------------------------------------------------------
print("\n3ª Questão - Balanceamento dos 5 códigos mais frequentes")

# Filtragem dos top 5 códigos
df_top5 = df[df["CAUSABAS"].isin(top5.index)]

# Contagem antes
print("\nDistribuição original das classes:")
print(df_top5["CAUSABAS"].value_counts())

# Abordagem de balanceamento: amostragem aleatória (upsampling)
minimo = df_top5["CAUSABAS"].value_counts().max()
df_balanceado = pd.concat([
    resample(grupo, replace=True, n_samples=minimo, random_state=42)
    for _, grupo in df_top5.groupby("CAUSABAS")
])

# Contagem após balanceamento
print("\nDistribuição após balanceamento:")
print(df_balanceado["CAUSABAS"].value_counts())

plt.figure(figsize=(7,4))
df_balanceado["CAUSABAS"].value_counts().plot(kind="bar", color="mediumseagreen")
plt.title("Distribuição das classes após balanceamento")
plt.xlabel("Código CID-10")
plt.ylabel("Quantidade de registros (balanceados)")
plt.show()

print("""
Foi utilizada a técnica de *upsampling*, replicando amostras das classes minoritárias
para equilibrar a quantidade de registros por categoria.
Essa abordagem é simples e eficaz quando o objetivo é evitar viés de classes
em análises exploratórias.
""")

# -------------------------------------------------------------------
# 5️⃣ Questão 4 - Filtragem pelo código C500 e análise de SEXO
# -------------------------------------------------------------------
print("\n4ª Questão - Análise do código C500 (Neoplasia maligna da mama)")

# Filtrar registros
df_c500 = df[df["CAUSABAS"] == "C500"]

# (i) Distribuição de SEXO
print("\nDistribuição do campo SEXO (1=Masculino, 2=Feminino, 9=Ignorado):")
print(df_c500["SEXO"].value_counts())

plt.figure(figsize=(5,4))
sns.countplot(x="SEXO", data=df_c500, palette="coolwarm")
plt.title("Distribuição de SEXO para óbitos por C500 (Câncer de mama)")
plt.xlabel("SEXO (1=Masculino, 2=Feminino, 9=Ignorado)")
plt.ylabel("Frequência")
plt.show()

# (ii) Interpretação
print("""
Ao filtrar pelo código C500, selecionamos os registros de óbitos cuja causa
básica é o câncer de mama. Como esperado, observa-se uma predominância
quase total de indivíduos do sexo feminino.
Isso confirma a coerência dos dados, já que o câncer de mama afeta majoritariamente mulheres.

Realizar balanceamento de SEXO nesse caso **não seria adequado**, pois
alteraria a representatividade biológica e epidemiológica da doença.
""")

# -------------------------------------------------------------------
# 6️⃣ Questão 5 - Proposta de estudo
# -------------------------------------------------------------------
print("\n5ª Questão - Proposta de estudo")

print("""
Com base na base SIM 2024, uma possível linha de investigação seria:
"Analisar a mortalidade materna e neonatal no Brasil, relacionando variáveis como
idade da mãe, escolaridade, assistência médica (ASSISTMED), tipo de parto (PARTO)
e peso ao nascer (PESO)."

Esse estudo permitiria identificar fatores de risco associados à mortalidade
infantil e orientar políticas públicas de saúde reprodutiva.
""")
