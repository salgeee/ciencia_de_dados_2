import json

with open('enem_clustering/notebooks/04_interpretation.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Atualizar célula 3 para carregar labels automaticamente
notebook['cells'][2]['source'] = [
    "# Carregar dados processados e labels\n",
    "DATA_PROCESSED = project_root / 'data' / 'processed'\n",
    "\n",
    "# Carregar dados das escolas\n",
    "df_escolas = pd.read_parquet(DATA_PROCESSED / 'dados_escolas.parquet')\n",
    "df_clustering = pd.read_parquet(DATA_PROCESSED / 'dados_clustering.parquet')\n",
    "\n",
    "# Tentar carregar labels salvos do notebook 03\n",
    "import os\n",
    "labels_path = DATA_PROCESSED / 'labels_kmeans.npy'\n",
    "\n",
    "if labels_path.exists():\n",
    "    labels = np.load(labels_path)\n",
    "    print('✓ Labels carregados de:', labels_path)\n",
    "else:\n",
    "    # Se nao existir, usar K-Means para gerar labels\n",
    "    from sklearn.cluster import KMeans\n",
    "    print('Labels nao encontrados. Gerando com K-Means...')\n",
    "    \n",
    "    # Determinar melhor k (usar 4 como padrao)\n",
    "    k = 4\n",
    "    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
    "    labels = kmeans.fit_predict(df_clustering)\n",
    "    \n",
    "    # Salvar labels para uso futuro\n",
    "    np.save(labels_path, labels)\n",
    "    print(f'✓ Labels gerados com K-Means (k={k})')\n",
    "\n",
    "# Adicionar labels ao dataframe\n",
    "df_escolas['cluster'] = labels\n",
    "df_clustering['cluster'] = labels\n",
    "\n",
    "print(f'\\nShape df_escolas: {df_escolas.shape}')\n",
    "print(f'Shape df_clustering: {df_clustering.shape}')\n",
    "print(f'Clusters unicos: {sorted(df_escolas["cluster"].unique())}')\n",
    "print(f'\\nDistribuicao dos clusters:')\n",
    "print(df_escolas['cluster'].value_counts().sort_index())"
]

# Atualizar funcao de tipos de escola para usar df_escolas automaticamente
for i, cell in enumerate(notebook['cells']):
    if 'def analisar_tipos_escola' in str(cell['source']):
        notebook['cells'][i]['source'] = [
            "# Analise dos tipos de escolas por cluster\n",
            "def analisar_tipos_escola(df, labels=None):\n",
            "    if labels is not None:\n",
            "        df_analysis = df.copy()\n",
            "        df_analysis['cluster'] = labels\n",
            "    else:\n",
            "        df_analysis = df.copy()\n",
            "    \n",
            "    coluna_tipo = 'TP_DEPENDENCIA_ADM_ESC' if 'TP_DEPENDENCIA_ADM_ESC' in df_analysis.columns else None\n",
            "    \n",
            "    if coluna_tipo:\n",
            "        # Mapear codigos para nomes\n",
            "        tipo_map = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}\n",
            "        df_analysis['tipo_escola'] = df_analysis[coluna_tipo].map(tipo_map).fillna('Outro')\n",
            "        \n",
            "        # Tabela cruzada\n",
            "        crosstab = pd.crosstab(df_analysis['cluster'], \n",
            "                               df_analysis['tipo_escola'], \n",
            "                               normalize='index') * 100\n",
            "        print('Distribuicao percentual por tipo de escola:')\n",
            "        print(crosstab.round(1))\n",
            "        \n",
            "        # Plot\n",
            "        crosstab.plot(kind='bar', stacked=True, figsize=(10, 6))\n",
            "        plt.title('Distribuicao de Tipos de Escola por Cluster')\n",
            "        plt.xlabel('Cluster')\n",
            "        plt.ylabel('Percentual')\n",
            "        plt.legend(title='Tipo de Escola', bbox_to_anchor=(1.05, 1))\n",
            "        plt.tight_layout()\n",
            "        plt.show()\n",
            "    else:\n",
            "        print('Coluna TP_DEPENDENCIA_ADM_ESC nao encontrada')\n",
            "        print('Colunas disponiveis:', df_analysis.columns.tolist())\n",
            "\n",
            "# Executar analise\n",
            "analisar_tipos_escola(df_escolas)"
        ]
        print('Célula de tipos de escola atualizada')
        break

# Atualizar funcao de estaduais
for i, cell in enumerate(notebook['cells']):
    if 'def analisar_estaduais' in str(cell['source']):
        notebook['cells'][i]['source'] = [
            "# Analise especifica das escolas publicas estaduais\n",
            "def analisar_estaduais(df, labels=None):\n",
            "    if labels is not None:\n",
            "        df_analysis = df.copy()\n",
            "        df_analysis['cluster'] = labels\n",
            "    else:\n",
            "        df_analysis = df.copy()\n",
            "    \n",
            "    coluna_tipo = 'TP_DEPENDENCIA_ADM_ESC' if 'TP_DEPENDENCIA_ADM_ESC' in df_analysis.columns else None\n",
            "    \n",
            "    if coluna_tipo:\n",
            "        # Filtrar apenas estaduais (codigo 2)\n",
            "        estaduais = df_analysis[df_analysis[coluna_tipo] == 2]\n",
            "        print(f'Total de escolas estaduais: {len(estaduais)} ({len(estaduais)/len(df_analysis)*100:.1f}%)')\n",
            "        \n",
            "        if len(estaduais) > 0:\n",
            "            print('\\nDistribuicao dos clusters entre estaduais:')\n",
            "            distr = estaduais['cluster'].value_counts(normalize=True).sort_index() * 100\n",
            "            print(distr.round(1))\n",
            "            \n",
            "            # Comparar com distribuicao geral\n",
            "            print('\\nComparacao com distribuicao geral:')\n",
            "            geral = df_analysis['cluster'].value_counts(normalize=True).sort_index() * 100\n",
            "            comparacao = pd.DataFrame({'Estaduais': distr, 'Geral': geral}).fillna(0)\n",
            "            comparacao['Diferenca'] = comparacao['Estaduais'] - comparacao['Geral']\n",
            "            print(comparacao.round(1))\n",
            "            \n",
            "            # Plot\n",
            "            comparacao[['Estaduais', 'Geral']].plot(kind='bar', figsize=(10, 6))\n",
            "            plt.title('Escolas Estaduais vs Distribuicao Geral por Cluster')\n",
            "            plt.xlabel('Cluster')\n",
            "            plt.ylabel('Percentual')\n",
            "            plt.legend()\n",
            "            plt.tight_layout()\n",
            "            plt.show()\n",
            "    else:\n",
            "        print('Coluna TP_DEPENDENCIA_ADM_ESC nao encontrada')\n",
            "\n",
            "# Executar analise\n",
            "analisar_estaduais(df_escolas)"
        ]
        print('Célula de estaduais atualizada')
        break

# Atualizar funcao de fatores de desempenho
for i, cell in enumerate(notebook['cells']):
    if 'def analisar_fatores_desempenho' in str(cell['source']):
        notebook['cells'][i]['source'] = [
            "# Identificar fatores que distinguem alto desempenho\n",
            "def analisar_fatores_desempenho(df, labels=None):\n",
            "    colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']\n",
            "    colunas_notas = [c for c in colunas_notas if c in df.columns]\n",
            "    \n",
            "    if labels is not None:\n",
            "        df_analysis = df.copy()\n",
            "        df_analysis['cluster'] = labels\n",
            "    else:\n",
            "        df_analysis = df.copy()\n",
            "    \n",
            "    # Calcular media geral\n",
            "    df_analysis['MEDIA_GERAL'] = df_analysis[colunas_notas].mean(axis=1)\n",
            "    \n",
            "    # Identificar cluster de maior desempenho\n",
            "    media_por_cluster = df_analysis.groupby('cluster')['MEDIA_GERAL'].mean().sort_values(ascending=False)\n",
            "    melhor_cluster = media_por_cluster.index[0]\n",
            "    pior_cluster = media_por_cluster.index[-1]\n",
            "    \n",
            "    print('Media geral por cluster:')\n",
            "    for cluster, media in media_por_cluster.items():\n",
            "        marker = '⭐' if cluster == melhor_cluster else ''\n",
            "        print(f'  Cluster {cluster}: {media:.2f} {marker}')\n",
            "    \n",
            "    print(f'\\nCluster de MAIOR desempenho: {melhor_cluster} (media: {media_por_cluster[melhor_cluster]:.2f})')\n",
            "    print(f'Cluster de MENOR desempenho: {pior_cluster} (media: {media_por_cluster[pior_cluster]:.2f})')\n",
            "    \n",
            "    # Comparar melhor vs pior\n",
            "    melhor = df_analysis[df_analysis['cluster'] == melhor_cluster]\n",
            "    pior = df_analysis[df_analysis['cluster'] == pior_cluster]\n",
            "    \n",
            "    print(f'\\nComparacao entre Cluster {melhor_cluster} (melhor) e Cluster {pior_cluster} (pior):')\n",
            "    for col in colunas_notas:\n",
            "        media_melhor = melhor[col].mean()\n",
            "        media_pior = pior[col].mean()\n",
            "        diferenca = media_melhor - media_pior\n",
            "        print(f'  {col}: {media_melhor:.1f} vs {media_pior:.1f} (dif: +{diferenca:.1f})')\n",
            "    \n",
            "    # Analise de tipo de escola no melhor cluster\n",
            "    coluna_tipo = 'TP_DEPENDENCIA_ADM_ESC' if 'TP_DEPENDENCIA_ADM_ESC' in df_analysis.columns else None\n",
            "    if coluna_tipo:\n",
            "        print(f'\\nComposicao do Cluster {melhor_cluster} (melhor):')\n",
            "        tipo_map = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}\n",
            "        composicao = melhor[coluna_tipo].map(tipo_map).value_counts(normalize=True) * 100\n",
            "        for tipo, pct in composicao.items():\n",
            "            print(f'  {tipo}: {pct:.1f}%')\n",
            "    \n",
            "    return melhor_cluster\n",
            "\n",
            "# Executar analise\n",
            "melhor = analisar_fatores_desempenho(df_escolas)"
        ]
        print('Célula de fatores de desempenho atualizada')
        break

with open('enem_clustering/notebooks/04_interpretation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print('\n✓ Notebook 04 atualizado com funcoes completas!')
print('Agora o notebook:')
print('  1. Carrega labels automaticamente (ou gera com K-Means)')
print('  2. Executa as analises diretamente')
print('  3. Gera graficos automaticamente')
