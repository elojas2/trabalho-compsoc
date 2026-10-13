# Grafo de coocorrência de atores - Controvérsia das Bets
# Uso: python grafo_coocorrencia.py   (corpus_bets.csv na mesma pasta)
# Requer: pip install networkx matplotlib numpy

import csv, itertools, collections
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1. Ler o corpus: cada linha é um texto; a coluna "atores" lista os atores separados por ";"
linhas = list(csv.DictReader(open("corpus_bets.csv", encoding="utf-8")))

# 2. Contar em quantos textos cada ator aparece (tamanho do nó)
#    e quantas vezes cada par aparece junto no mesmo texto (peso da ligação)
aparicoes = collections.Counter()
pares = collections.Counter()
for texto in linhas:
    atores = sorted(set(texto["atores"].split(";")))
    aparicoes.update(atores)
    for a, b in itertools.combinations(atores, 2):
        pares[(a, b)] += 1

# 3. Exportar para o Gephi (nós e arestas)
with open("gephi_nos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Id", "Label", "Textos"])
    for ator, n in aparicoes.items(): w.writerow([ator, ator, n])
with open("gephi_arestas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Source", "Target", "Weight", "Type"])
    for (a, b), n in pares.items(): w.writerow([a, b, n, "Undirected"])

# 4. Montar o grafo
G = nx.Graph()
for ator, n in aparicoes.items(): G.add_node(ator, n=n)
for (a, b), n in pares.items(): G.add_edge(a, b, w=n)
pos = nx.kamada_kawai_layout(G)          # posiciona os nós (quem aparece junto fica perto)
centro = np.mean(list(pos.values()), axis=0)

# 5. Cores por grupo de ator
cores = {
    "Operadoras/Associações": "#c0504d", "Clubes/Futebol": "#e08a3c",
    "Governo/Fazenda": "#1f6f8b", "Polícia": "#1f6f8b",
    "Congresso": "#4a7fb5", "STF/Judiciário": "#4a7fb5",
    "Pesquisadores/Saúde": "#2e8b57", "Ministério Público": "#2e8b57",
    "Pequenos negócios/Sebrae": "#2e8b57",
}
cinza = "#7d8b99"

# 6. Desenhar
fig, ax = plt.subplots(figsize=(11, 8), dpi=150)
for a, b, d in G.edges(data=True):
    ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
            color="#9aa5b1", lw=0.6 + d["w"] * 0.9, alpha=0.55, zorder=1)
    if d["w"] >= 4:   # rotula só as ligações fortes
        ax.text((pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2, str(d["w"]),
                fontsize=8, color="#52606d", ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.5))
for ator in G.nodes:
    n = aparicoes[ator]
    ax.scatter(*pos[ator], s=180 + n * 90, color=cores.get(ator, cinza),
               zorder=2, edgecolors="white", lw=1.5)
    v = pos[ator] - centro
    if ator == "Operadoras/Associações":   # nó colado no centro: rótulo vai para baixo
        v = np.array([0.0, -1.0])
    v = v /(np.linalg.norm(v) + 1e-6) * (0.06 + n * 0.004)   # rótulo para fora do centro
    ax.text(pos[ator][0] + v[0], pos[ator][1] + v[1], f"{ator} ({n})", fontsize=9,
            ha="left" if v[0] > 0 else "right", va="bottom" if v[1] > 0 else "top",
            zorder=3, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))

legenda = [("Setor de apostas", "#c0504d"), ("Futebol", "#e08a3c"),
           ("Executivo e polícia", "#1f6f8b"), ("Legislativo e Judiciário", "#4a7fb5"),
           ("Saúde, Min. Público e Sebrae", "#2e8b57"), ("Outros", cinza)]
ax.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=10, label=l) for l, c in legenda],
          loc="lower left", fontsize=8, frameon=False)
ax.set_title(f"Coocorrência de atores em {len(linhas)} notícias e documentos (2018–2026)",
             fontsize=12, loc="left")
ax.text(0.99, 0.01, "Tamanho do nó = nº de textos em que o ator aparece; "
        "espessura da linha = nº de textos em que dois atores aparecem juntos",
        transform=ax.transAxes, ha="right", fontsize=7, color="#52606d")
ax.margins(0.18); ax.axis("off"); plt.tight_layout()
plt.savefig("grafo_atores.png")
print("Gerados: grafo_atores.png, gephi_nos.csv, gephi_arestas.csv")
