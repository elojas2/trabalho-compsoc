# Grafo de coocorrência de atores

Script para analisar a coocorrência de atores em notícias e documentos sobre a controvérsia das bets. Cada linha do corpus representa um texto; atores que aparecem juntos formam uma ligação no grafo.

## Requisitos

- Python 3
- `networkx`, `matplotlib`, `numpy` e `scipy`

## Instalação

No macOS, crie um ambiente virtual na pasta do projeto e instale as dependências nele:

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install networkx matplotlib numpy scipy
```

Ative `.venv` novamente sempre que abrir um novo terminal para trabalhar no projeto. Isso evita instalar pacotes no Python gerenciado pelo Homebrew.

## Dados de entrada

Coloque `corpus_bets.csv` na mesma pasta de `grafo_coocorrencia.py`. O CSV deve estar codificado em UTF-8, ter uma coluna chamada `atores` e usar ponto e vírgula (`;`) para separar os atores em cada linha.

Exemplo:

```csv
atores
Operadoras/Associações;Congresso
Clubes/Futebol;Governo/Fazenda
```

## Execução

Com o ambiente virtual ativado, execute:

```zsh
python grafo_coocorrencia.py
```

O script gera, na mesma pasta:

- `grafo_atores.png`: visualização do grafo; o tamanho dos nós representa o número de textos com cada ator, e a espessura das ligações representa a quantidade de coocorrências.
- `gephi_nos.csv`: nós e número de textos por ator, para importação no Gephi.
- `gephi_arestas.csv`: ligações e pesos de coocorrência, para importação no Gephi.
