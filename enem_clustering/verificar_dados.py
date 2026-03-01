import pandas as pd

# Verificar o que o notebook 04 está carregando
df_clusters = pd.read_csv('data/processed/escolas_com_clusters.csv')
print('Arquivo escolas_com_clusters.csv:')
print(f'  Total: {len(df_clusters)} escolas')
print(f'  Clusters: {df_clusters["cluster"].value_counts().sort_index().to_dict()}')
print()

# Verificar se existe parquet
try:
    df_parquet = pd.read_parquet('data/processed/dados_escolas.parquet')
    print('Arquivo dados_escolas.parquet existe:')
    print(f'  Total: {len(df_parquet)} escolas')
    if 'cluster' in df_parquet.columns:
        print(f'  Clusters: {df_parquet["cluster"].value_counts().sort_index().to_dict()}')
except Exception as e:
    print(f'Arquivo dados_escolas.parquet NAO existe ou erro: {e}')

print()
print('Composicao do arquivo CSV (escolas_com_clusters.csv):')
for c in sorted(df_clusters['cluster'].unique()):
    subset = df_clusters[df_clusters['cluster'] == c]
    comp = subset['TP_DEPENDENCIA_ADM_ESC'].value_counts(normalize=True) * 100
    count = subset['TP_DEPENDENCIA_ADM_ESC'].value_counts()
    print(f'Cluster {c}: {len(subset)} escolas')
    print(f'  Estadual (2): {comp.get(2.0, 0):.1f}% ({count.get(2.0, 0)} escolas)')
    print(f'  Privada (4):  {comp.get(4.0, 0):.1f}% ({count.get(4.0, 0)} escolas)')
    print(f'  Federal (1):  {comp.get(1.0, 0):.1f}% ({count.get(1.0, 0)} escolas)')
    print()

# Verificar media por cluster
print('Medias por cluster:')
for c in sorted(df_clusters['cluster'].unique()):
    subset = df_clusters[df_clusters['cluster'] == c]
    print(f'Cluster {c}: {subset["MEDIA_GERAL"].mean():.2f}')
