import tkinter as tk
from tkinter import ttk, font as tkfont, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.utils import resample
from textwrap import fill

plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial"],
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})
sns.set_style("whitegrid")

df = pd.read_csv("SIM2024.csv", sep=";", encoding="latin1")

def criar_janela_rolavel(titulo, texto, fig=None, tamanho=(900, 650)):
    win = tk.Toplevel()
    win.title(titulo)
    win.geometry(f"{tamanho[0]}x{tamanho[1]}")
    win.configure(bg="#f8f9fa")

    container = ttk.Frame(win)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#f8f9fa", highlightthickness=0)
    v_scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)
    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content, anchor="nw")

    def on_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content.bind("<Configure>", on_configure)

    if fig:
        canvas_fig = FigureCanvasTkAgg(fig, master=content)
        canvas_fig.draw()
        widget_fig = canvas_fig.get_tk_widget()
        widget_fig.pack(padx=10, pady=(10, 5), fill="both", expand=False)

    wrapped = fill(texto, 95)
    fonte_texto = tkfont.Font(family="Segoe UI", size=11)
    text_widget = tk.Text(content, wrap="word", height=10, padx=12, pady=12,
                          font=fonte_texto, fg="#333", bg="#ffffff", relief="flat")
    text_widget.insert("1.0", wrapped)
    text_widget.configure(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=(5, 20))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    def on_close():
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
        if fig:
            plt.close(fig)
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_close)

def grafico_assistmed():
    texto = (
        "O campo ASSISTMED indica se o falecido recebeu assistência médica durante a doença que ocasionou a morte. "
        "Observa-se que a maior parte dos registros indica que houve assistência médica. Isso sugere que a maioria dos óbitos ocorreu "
        "em contextos com acompanhamento profissional, embora ainda exista um percentual de casos sem atendimento ou sem informação "
        "(9 = ignorado)."
    )
    counts = df["ASSISTMED"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6.7))
    counts.plot(kind="bar", color=["steelblue", "indianred", "gray"], ax=ax)
    ax.set_title("1ª Questão - Distribuição do campo ASSISTMED")
    ax.set_xlabel("1 = Sim | 2 = Não | 9 = Ignorado")
    ax.set_ylabel("Frequência")
    plt.tight_layout(rect=[0, 0.20, 1, 1])
    fig.text(0.5, 0.09, "\n".join(fill(par, 100) for par in texto.split("\n\n")),
             ha="center", va="top", fontsize=10, wrap=True)
    plt.show()
    plt.close(fig)

def grafico_causabas():
    top5 = df["CAUSABAS"].value_counts().head(5)
    texto = (
        "O campo CAUSABAS representa o código da causa básica da morte, segundo a Classificação Internacional de Doenças (CID-10). "
        "Exemplo: C500 = Neoplasia maligna da mama. Os códigos seguem o padrão da CID-10, com uma letra e três dígitos. "
        "Esses códigos representam as doenças mais frequentemente registradas como causa básica de óbito no conjunto de dados analisado.\n\n"
        "Observação: o gráfico exibe apenas as 5 causas mais frequentes no período analisado. Para análises mais detalhadas, filtre por UF, faixa etária ou ano."
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top5.index, y=top5.values, palette="crest", ax=ax)
    ax.set_title("Top 5 causas básicas de óbito (CAUSABAS)", fontweight="bold")
    ax.set_xlabel("Código CID-10")
    ax.set_ylabel("Frequência")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, int(p.get_height())),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    criar_janela_rolavel("Top 5 causas básicas de óbito (CAUSABAS)", texto, fig)

def grafico_balanceamento():
    top5 = df["CAUSABAS"].value_counts().head(5)
    df_top5 = df[df["CAUSABAS"].isin(top5.index)]
    minimo = df_top5["CAUSABAS"].value_counts().max()
    df_balanceado = pd.concat([
        resample(grupo, replace=True, n_samples=minimo, random_state=42)
        for _, grupo in df_top5.groupby("CAUSABAS")
    ])
    texto = (
        "Foi utilizada a técnica de *upsampling*, replicando amostras das classes minoritárias "
        "para equilibrar a quantidade de registros por categoria. "
        "Essa abordagem é simples e eficaz quando o objetivo é evitar viés de classes "
        "em análises exploratórias e garantir uma representação mais equilibrada "
        "das causas básicas de óbito nos gráficos e nas análises estatísticas subsequentes."
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    df_balanceado["CAUSABAS"].value_counts().plot(kind="bar", color="mediumseagreen", ax=ax)
    ax.set_title("3ª Questão - Distribuição das classes após balanceamento", fontweight="bold")
    ax.set_xlabel("Código CID-10")
    ax.set_ylabel("Quantidade de registros (balanceados)")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, int(p.get_height())),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    criar_janela_rolavel("Distribuição das classes após balanceamento", texto, fig)

def grafico_sexo():
    mapping = {1: "Masculino", 2: "Feminino"}
    df_c500 = df[df["CAUSABAS"] == "C500"].copy()
    df_c500 = df_c500[df_c500["SEXO"].isin([1, 2])]
    df_c500["SEXO_cat"] = df_c500["SEXO"].map(mapping)
    texto = (
        "Ao filtrar pelo código C500, selecionamos os registros de óbitos cuja causa básica é o câncer de mama. "
        "Como esperado, observa-se uma predominância quase total de indivíduos do sexo feminino. "
        "Isso confirma a coerência dos dados, já que o câncer de mama afeta majoritariamente mulheres.\n\n"
        "Realizar balanceamento de SEXO nesse caso **não seria adequado**, pois "
        "alteraria a representatividade biológica e epidemiológica da doença."
    )
    fig, ax = plt.subplots(figsize=(8.5, 5))
    sns.countplot(x="SEXO_cat", data=df_c500, order=["Masculino", "Feminino"], palette=["#4e79a7", "#e15759"], ax=ax)
    ax.set_title("Distribuição de SEXO em óbitos por C500 (câncer de mama)", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Frequência")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, int(p.get_height())),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    criar_janela_rolavel("Distribuição por SEXO", texto, fig)

def mostrar_questao5():
    texto = (
        "A partir da base SIM 2024, uma investigação relevante seria analisar os fatores associados à mortalidade materna e neonatal no Brasil, "
        "considerando variáveis demográficas, socioeconômicas e de assistência à saúde disponíveis na base. O estudo poderia ter como objetivos "
        "identificar padrões e fatores de risco relacionados à mortalidade infantil e materna, avaliando características como idade da mãe, escolaridade, cor/raça, tipo de parto, peso ao nascer, assistência médica recebida (ASSISTMED) e região geográfica. A análise incluiria "
        "a distribuição espacial e temporal, verificando estados ou municípios com maiores índices de mortalidade e tendências ao longo do período. "
        "Também seriam avaliados perfis de risco cruzando idade da mãe, escolaridade e assistência médica para identificar grupos populacionais mais vulneráveis. "
        "Além disso, seria possível examinar a relação entre tipo de parto e desfechos neonatais ou maternos, bem como analisar como o peso ao nascer influencia "
        "a mortalidade neonatal, considerando prematuridade e assistência médica. Por fim, técnicas de modelagem preditiva poderiam ser aplicadas para estimar "
        "o risco de óbito materno e neonatal com base nas variáveis da base, fornecendo insights para políticas públicas, priorização de recursos e estratégias "
        "de prevenção, contribuindo para a redução da mortalidade materna e infantil no país."
    )
    criar_janela_rolavel("Questão 5 - Proposta de estudo", texto, fig=None, tamanho=(700, 250))

janela = tk.Tk()
janela.title("Análise SIM 2024 - Visualização Interativa")
janela.geometry("400x320")

tk.Label(janela, text="Selecione o gráfico que deseja visualizar:", font=("Arial", 11, "bold")).pack(pady=10)

tk.Button(janela, text="Questão 1 - Distribuição ASSISTMED", command=grafico_assistmed, width=35, bg="#4e79a7", fg="white").pack(pady=5)
tk.Button(janela, text="Questão 2 - Top 5 causas (CAUSABAS)", command=grafico_causabas, width=35, bg="#59a14f", fg="white").pack(pady=5)
tk.Button(janela, text="Questão 3 - Balanceamento de classes CAUSABAS", command=grafico_balanceamento, width=35, bg="#f28e2b", fg="white").pack(pady=5)
tk.Button(janela, text="Questão 4 - Distribuição por SEXO", command=grafico_sexo, width=35, bg="#e15759", fg="white").pack(pady=5)
tk.Button(janela, text="Questão 5 - Proposta de estudo", command=mostrar_questao5, width=35, bg="#76b7b2", fg="white").pack(pady=5)
tk.Button(janela, text="Sair", command=janela.destroy, width=35, bg="#999999", fg="white").pack(pady=20)

janela.mainloop()