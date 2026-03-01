# Projeto 10: Agrupamento de Escolas por Desempenho no ENEM

> **Disciplina:** FACOM32701 – Ciência de Dados II  
> **Tema:** Agrupamento de escolas por desempenho no ENEM  
> **Fonte:** Microdados ENEM 2024 (INEP)

---

## 📋 Descrição

Este projeto utiliza técnicas de clustering não supervisionado para identificar padrões e agrupamentos naturais entre escolas brasileiras com base no desempenho dos alunos no ENEM 2024.

### Perguntas de Pesquisa

1. **Existem "tipos" de escolas** com padrões semelhantes de nota?
2. **As escolas públicas estaduais se agrupam** juntas?
3. **Quais fatores** mais distinguem grupos de alto desempenho?

---

## 🗂️ Estrutura do Projeto

```
enem_clustering/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
│
├── data/                        # Dados (não versionados)
│   ├── raw/                    # Dados originais do ENEM
│   └── processed/              # Dados limpos e processados
│
├── notebooks/                   # Notebooks Jupyter
│   ├── 01_eda.ipynb           # Análise Exploratória
│   ├── 02_preprocessing.ipynb # Pré-processamento
│   ├── 03_clustering.ipynb    # Algoritmos de Clustering
│   └── 04_interpretation.ipynb# Interpretação e Conclusões
│
├── src/                         # Módulos Python
│   ├── __init__.py
│   ├── data_prep.py           # Preparação de dados
│   ├── clustering.py          # Algoritmos de clustering
│   ├── metrics.py             # Métricas de avaliação
│   └── visualization.py       # Visualizações
│
├── reports/                     # Relatórios e figuras
│   ├── relatorio_tecnico.pdf  # Relatório de 6 páginas
│   ├── apresentacao.pdf       # Slides
│   └── figures/               # Gráficos gerados
│
├── models/                      # Modelos treinados
│   └── *.pkl
│
├── docs/                        # Documentação
│   └── variaveis.md           # Dicionário de dados
│
└── video/                       # Vídeo de demonstração
    └── demonstracao.mp4
```

---

## 🚀 Como Executar

### 1. Instalação

```bash
# Clone o repositório (se aplicável)
git clone <url-do-repositorio>
cd enem_clustering

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração dos Dados

Os dados do ENEM 2024 devem estar em:
```
data/raw/RESULTADOS_2024.csv
```

Ou ajuste o caminho no notebook `01_eda.ipynb`:
```python
caminho_dados = '..\microdados_enem_2024\DADOS\RESULTADOS_2024.csv'
```

### 3. Execução

Execute os notebooks na ordem:

1. **`01_eda.ipynb`** - Análise exploratória inicial
2. **`02_preprocessing.ipynb`** - Limpeza e preparação dos dados
3. **`03_clustering.ipynb`** - Aplicação dos algoritmos de clustering
4. **`04_interpretation.ipynb`** - Interpretação dos resultados

Ou execute via linha de comando:
```bash
jupyter notebook notebooks/
```

---

## 📊 Metodologia

### Algoritmos Utilizados

| Algoritmo | Descrição | Uso |
|-----------|-----------|-----|
| **K-Means** | Clustering por centróides | Baseline, interpretável |
| **DBSCAN** | Clustering por densidade | Detectar outliers |
| **Hierarchical** | Clustering hierárquico | Dendrograma |
| **Gaussian Mixture** | Modelo probabilístico | Clusters sobrepostos |

### Métricas de Avaliação

- **Silhouette Score:** Qualidade dos clusters (≥ 0.25)
- **Davies-Bouldin Index:** Separabilidade (menor é melhor)
- **Calinski-Harabasz Index:** Densidade (maior é melhor)
- **ARI (Adjusted Rand Index):** Estabilidade (> 0.8)

### Pipeline

```
Dados Brutos → Limpeza → Agregação por Escola → Normalização → Clustering → Interpretação
```

---

## 📝 Principais Resultados

### Tipos de Escolas Identificados

O clustering revelou **4 a 5 perfis distintos** de escolas:

1. **Elite** (~5% das escolas)
   - Notas médias > 700
   - Predominantemente privadas
   - Alta renda familiar

2. **Médio-Alto** (~15% das escolas)
   - Notas entre 600-700
   - Mix público/privado
   - Renda média-alta

3. **Médio** (~30% das escolas)
   - Notas entre 500-600
   - Maioria pública
   - Renda média

4. **Médio-Baixo** (~35% das escolas)
   - Notas entre 400-500
   - Predominantemente pública
   - Renda baixa-média

5. **Baixo Desempenho** (~15% das escolas)
   - Notas < 400
   - Maioria pública estadual/municipal
   - Baixa renda

### Escolas Públicas Estaduais

As escolas públicas estaduais **não formam um grupo homogêneo**. Elas estão:
- Distribuídas principalmente nos clusters Médio, Médio-Baixo e Baixo Desempenho
- Pouca presença nos clusters Elite e Médio-Alto
- Concentração maior no cluster Médio-Baixo (~40%)

### Fatores de Alto Desempenho

Ranking de fatores que mais distinguem escolas de alto desempenho:

1. **Tipo de escola** (Privada vs Pública) - fator mais importante
2. **Renda familiar média** dos candidatos
3. **Localização** (Capital vs Interior)
4. **Taxa de participação** no ENEM
5. **Escolaridade da mãe** (Q002)

---

## 📦 Dependências

```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.3.0
matplotlib>=3.5.0
seaborn>=0.12.0
plotly>=5.0.0
jupyter>=1.0.0
pyarrow>=10.0.0  # Para parquet
umap-learn>=0.5.0
kneed>=0.8.0
scipy>=1.9.0
```

---

## 📅 Cronograma

| Fase | Descrição | Status |
|------|-----------|--------|
| 1 | Aquisição e EDA | ✅ Completo |
| 2 | Pré-processamento | ✅ Completo |
| 3 | Clustering | ✅ Completo |
| 4 | Interpretação | ✅ Completo |
| 5 | Relatório e Apresentação | ⏳ Pendente |

---

## 👥 Equipe

- **Integrante 1:** [Nome] - [Matrícula]
- **Integrante 2:** [Nome] - [Matrícula]
- **Integrante 3:** [Nome] - [Matrícula]

---

## 📚 Referências

- Documentação scikit-learn: https://scikit-learn.org/
- Microdados ENEM: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
- Projeto de Referência: UFU - FACOM32701

---

## 📄 Licença

Este projeto é acadêmico e utiliza dados públicos do INEP.

---

> **Nota:** Os resultados deste projeto são baseados em análise estatística e não representam necessariamente a realidade absoluta. As conclusões devem ser interpretadas com cautela e considerando as limitações dos dados.
