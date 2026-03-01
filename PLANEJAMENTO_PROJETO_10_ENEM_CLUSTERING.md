# PLANEJAMENTO: PROJETO 10 - Agrupamento de Escolas por Desempenho no ENEM

**Confidence:** 0.92 (HIGH) | **Sources:** PDF do trabalho, KB: Clustering

---

## 1. OVERVIEW

| Aspecto | Descrição |
|---------|-----------|
| **Tema** | Agrupamento de escolas por desempenho no ENEM |
| **Fonte** | Microdados ENEM 2024 (INEP) |
| **Equipe** | Até 3 alunos |
| **Prazo Entrega** | 27/02/2026 |
| **Apresentação** | 02/03/2026 a 09/03/2026 |
| **Nota** | 30 pontos |

### Perguntas de Pesquisa
1. Existem "tipos" de escolas com padrões semelhantes de nota?
2. As escolas públicas estaduais se agrupam juntas?
3. Quais fatores mais distinguem grupos de alto desempenho?

---

## 2. ARQUITETURA DO PROJETO

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE CLUSTERING                        │
├─────────────────────────────────────────────────────────────────┤
│  1. AQUISIÇÃO        →  2. PREP          →  3. EDA              │
│     • Download          • Limpeza           • Estatísticas        │
│     • Dicionário        • Normalização      • Correlações         │
│     • Seleção           • Encoding          • Visualizações       │
│                                                                  │
│  4. MODELAGEM        →  5. AVALIAÇÃO       →  6. INTERPRETAÇÃO  │
│     • K-Means           • Silhouette        • Perfis de clusters │
│     • DBSCAN            • Davies-Bouldin    • Fatores chave      │
│     • Hierárquico       • Estabilidade      • Responder questões │
│     • GMM               • Comparação        • Conclusões         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. ETAPAS DETALHADAS

### FASE 1: Aquisição e Entendimento dos Dados (Semana 1)

| Tarefa | Descrição | Entregável Parcial |
|--------|-----------|-------------------|
| 1.1 Download | Baixar microdados ENEM 2024 | Pasta `data/raw/` |
| 1.2 Dicionário | Mapear variáveis relevantes | Documento `docs/variaveis.md` |
| 1.3 Seleção | Escolher features por escola | Lista de features selecionadas |

**Variáveis Sugeridas:**
```
Features de Contexto:
- CO_UF_ESCOLA (Estado)
- TP_DEPENDENCIA_ADM_ESCOLA (Federal/Estadual/Municipal/Privada)
- TP_LOCALIZACAO_ESCOLA (Urbana/Rural)

Features de Desempenho:
- Média das notas (CN, CH, LC, MT, REDACAO)
- Taxa de participação
- Percentual de treineiros

Features Socioeconômicas (agregadas por escola):
- Q006 (Renda familiar média dos candidatos)
- Q002 (Escolaridade da mãe)
- Q010 a Q025 (Acesso a recursos)
```

---

### FASE 2: Pré-processamento (Semana 1-2)

| Tarefa | Descrição | Validação |
|--------|-----------|-----------|
| 2.1 Limpeza | Remover escolas com < 10 alunos | Contagem antes/depois |
| 2.2 Missing | Imputar ou remover valores faltantes | % missing por coluna |
| 2.3 Encoding | One-hot para categóricas | Verificar cardinalidade |
| 2.4 Normalização | StandardScaler | Boxplot antes/depois |
| 2.5 Outliers | Analisar (não remover cegamente) | IQR method |

**Checklist:**
- [ ] Padronizar notas (0-1000 → z-score)
- [ ] Tratar categóricas (Uf, Dependência, Localização)
- [ ] Criar feature de média geral da escola
- [ ] Verificar distribuições (skewness)

---

### FASE 3: Análise Exploratória (Semana 2)

| Análise | Ferramenta | Output |
|---------|------------|--------|
| Estatísticas descritivas | `df.describe()` | Tabela resumo |
| Correlações | Pearson/Spearman heatmap | `corr_matrix.png` |
| Distribuições | Histogramas + Boxplots | `distributions/` |
| PCA | Variância explicada | `pca_variance.png` |
| t-SNE/UMAP | Visualização 2D | `tsne_visualization.png` |

**Perguntas a responder na EDA:**
- Qual a distribuição das notas por tipo de escola?
- Existe correlação entre renda média e desempenho?
- Quais estados têm as maiores variações?

---

### FASE 4: Aplicação de Algoritmos (Semana 2-3)

#### 4.1 Determinar Número de Clusters (k)

```python
# Métodos a aplicar:
1. Elbow Method (Inertia)
2. Silhouette Analysis
3. Gap Statistic (opcional)
4. Dendrograma (Hierarchical)
```

**Experimento K:**
- Testar k = 2 a 10
- Registrar métricas para cada k

#### 4.2 Algoritmos a Testar

| Algoritmo | Configuração | Por Quê? |
|-----------|--------------|----------|
| **K-Means** | n_init=10, random_state=42 | Baseline, interpretável |
| **MiniBatchKMeans** | batch_size=1000 | Se dados > 10k escolas |
| **DBSCAN** | eps via k-distance | Detectar outliers naturais |
| **Hierarchical** | linkage='ward' | Dendrograma, hierarquia |
| **GMM** | covariance_type='full' | Clusters sobrepostos |

#### 4.3 Validação de Estabilidade

```python
# Testar estabilidade (exigido no PDF)
seeds = [0, 1, 2, 42, 100]
labels_per_seed = []

for seed in seeds:
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(X)
    labels_per_seed.append(labels)

# Calcular ARI entre execuções
from sklearn.metrics import adjusted_rand_score
ari_scores = []
for i in range(len(seeds)):
    for j in range(i+1, len(seeds)):
        ari = adjusted_rand_score(labels_per_seed[i], labels_per_seed[j])
        ari_scores.append(ari)

# ARI > 0.8 indica estabilidade
```

#### 4.4 Métricas de Avaliação

| Métrica | Target | Uso |
|---------|--------|-----|
| Silhouette Score | ≥ 0.25 | Qualidade geral |
| Davies-Bouldin | ↓ mínimo | Separabilidade |
| Calinski-Harabasz | ↑ máximo | Densidade |
| ARI (estabilidade) | > 0.8 | Consistência |

---

### FASE 5: Interpretação e Resposta às Questões (Semana 3)

#### Questão 1: Existem "tipos" de escolas?

**Análise:**
```python
# Perfil de cada cluster
for cluster in range(n_clusters):
    subset = df[df['cluster'] == cluster]
    print(f"\n=== CLUSTER {cluster} ({len(subset)} escolas) ===")
    print(f"Nota média MT: {subset['NU_NOTA_MT'].mean():.1f}")
    print(f"Nota média CN: {subset['NU_NOTA_CN'].mean():.1f}")
    print(f"% Escolas Públicas: {(subset['TP_DEPENDENCIA'] != 4).mean()*100:.1f}")
    print(f"Renda média: {subset['Q006'].mean():.2f}")
```

#### Questão 2: Escolas públicas estaduais se agrupam?

**Análise:**
```python
# Verificar homogeneidade das públicas estaduais
mask_estadual = df['TP_DEPENDENCIA_ADM_ESCOLA'] == 2
estaduais = df[mask_estadual]

# Distribuição dos clusters entre estaduais
print(estaduais['cluster'].value_counts(normalize=True))

# Comparar com distribuição geral
print(df['cluster'].value_counts(normalize=True))
```

#### Questão 3: Fatores que distinguem alto desempenho

**Análise:**
```python
# Identificar cluster de alto desempenho
cluster_means = df.groupby('cluster')[['NU_NOTA_MT', 'NU_NOTA_CN', 
                                        'NU_NOTA_LC', 'NU_NOTA_CH']].mean()
high_perf_cluster = cluster_means.mean(axis=1).idxmax()

# Comparar com outros clusters
high_perf = df[df['cluster'] == high_perf_cluster]
others = df[df['cluster'] != high_perf_cluster]

# Quais features mais diferem?
from scipy import stats
for col in features:
    t_stat, p_value = stats.ttest_ind(high_perf[col], others[col])
    if p_value < 0.001:
        print(f"{col}: diferença significativa (p={p_value:.4f})")
```

---

## 4. CRONOGRAMA

```
FEVEREIRO 2026
├─ Semana 1 (03-07/02)
│  ├─ [ ] Download ENEM 2024
│  ├─ [ ] Limpeza inicial
│  └─ [ ] EDA inicial
│
├─ Semana 2 (10-14/02)
│  ├─ [ ] Pré-processamento completo
│  ├─ [ ] PCA / t-SNE
│  └─ [ ] Determinar k ótimo
│
├─ Semana 3 (17-21/02)
│  ├─ [ ] Aplicar algoritmos
│  ├─ [ ] Avaliar métricas
│  └─ [ ] Interpretar clusters
│
└─ Semana 4 (24-27/02) ← ENTREGA 27/02
   ├─ [ ] Finalizar notebook
   ├─ [ ] Escrever relatório (6 páginas)
   ├─ [ ] Criar slides
   ├─ [ ] Gravar vídeo (3-5 min)
   └─ [ ] Publicar no GitHub

MARÇO 2026
└─ Apresentação (02-09/03) - 20 min
```

---

## 5. ESTRUTURA DO REPOSITÓRIO

```
enem-clustering/
├── README.md                    # Instruções de reprodução
├── requirements.txt             # Dependências
├── .gitignore
│
├── data/
│   ├── raw/                    # Dados originais (ou script de download)
│   └── processed/              # Dados limpos
│
├── notebooks/
│   ├── 01_eda.ipynb           # Análise exploratória
│   ├── 02_preprocessing.ipynb # Pré-processamento
│   ├── 03_clustering.ipynb    # Algoritmos e avaliação
│   └── 04_interpretation.ipynb # Interpretação e conclusões
│
├── src/
│   ├── __init__.py
│   ├── data_prep.py           # Funções de limpeza
│   ├── clustering.py          # Funções de clustering
│   ├── metrics.py             # Funções de avaliação
│   └── visualization.py       # Funções de plot
│
├── reports/
│   ├── relatorio_tecnico.pdf  # 6 páginas
│   └── apresentacao.pdf       # Slides
│
├── docs/
│   └── variaveis.md           # Dicionário de dados
│
└── video/
    └── demonstracao.mp4       # 3-5 minutos
```

---

## 6. ALTERNATIVAS CONSIDERADAS

| Decisão | Opção A (Escolhida) | Opção B | Racional |
|---------|---------------------|---------|----------|
| Algoritmo principal | K-Means | Só DBSCAN | K-Means mais interpretável para perfis |
| Número de features | 15-20 features | Todas as 100+ | Evitar curse of dimensionality |
| Agragação | Por escola | Por aluno | Escola é unidade de análise pedida |
| Ano dos dados | 2024 | Média 2022-2024 | Foco no ano mais recente disponível |

---

## 7. RISCOS E MITIGAÇÃO

| Risco | Impacto | Prob. | Mitigação |
|-------|---------|-------|-----------|
| Arquivo ENEM muito grande (>1GB) | Alto | Média | Usar amostragem estratificada |
| Muitos missing em variáveis socioeconômicas | Médio | Alta | Imputar mediana por tipo de escola |
| Não encontrar clusters claros | Alto | Média | Testar mais algoritmos, PCA |
| Silhouette < 0.25 | Médio | Média | Documentar e explicar limitações |
| Escolas com poucos alunos | Baixo | Alta | Filtrar escolas com n < 10 |

---

## 8. CHECKLIST DE ENTREGA (Critérios de Avaliação)

| Critério | Peso | Checklist |
|----------|------|-----------|
| **Coleta e preparação** | 20% | [ ] Dados baixados<br>[ ] Limpeza documentada<br>[ ] Normalização aplicada |
| **Algoritmos** | 25% | [ ] ≥ 2 algoritmos testados<br>[ ] Estabilidade verificada (seeds)<br>[ ] Métricas calculadas |
| **Interpretação** | 20% | [ ] 3 perguntas respondidas<br>[ ] Perfis de clusters descritos<br>[ ] Conclusões claras |
| **Visualização/Relatório** | 25% | [ ] Notebook completo<br>[ ] PDF 6 páginas<br>[ ] Slides + Vídeo<br>[ ] GitHub organizado |
| **Originalidade** | 10% | [ ] Análise comparativa inesperada<br>[ ] Insights relevantes |

---

## 9. PRÓXIMOS PASSOS IMEDIATOS

### Hoje
1. [ ] Criar repositório no GitHub
2. [ ] Definir equipe (até 3 alunos)
3. [ ] Baixar microdados ENEM 2024

### Esta Semana
4. [ ] Criar estrutura de pastas
5. [ ] Iniciar notebook de EDA
6. [ ] Mapear variáveis do dicionário

---

## RECURSOS

### KB Local
- `.claude/kb/ml/clustering/` - Documentação de clustering
- `.claude/agents/ai-ml/clustering-specialist.md` - Agente especialista

### Bibliotecas Python
```txt
pandas
numpy
scikit-learn
matplotlib
seaborn
plotly
umap-learn
kneed
```

### Documentação
- [Microdados ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
- Dicionário de variáveis (vem com o download)

---

> **DICA:** Comece pequeno - teste com uma amostra de 1000 escolas antes de rodar em todos os dados. Isso acelera a iteração e validação da metodologia.
