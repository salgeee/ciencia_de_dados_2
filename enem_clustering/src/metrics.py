"""
Módulo de métricas para avaliação de clustering do ENEM.

Contém funções para calcular diversas métricas de qualidade de clustering,
incluindo índices de validação interna e medidas de estabilidade.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    silhouette_score, silhouette_samples,
    davies_bouldin_score, calinski_harabasz_score,
    adjusted_rand_score
)
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


def calcular_silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calcula o Silhouette Score médio.
    
    O Silhouette Score mede quão similar um objeto é ao seu próprio cluster
    comparado aos outros clusters. Varia de -1 a 1, onde valores próximos a 1
    indicam clusters bem definidos.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    float
        Silhouette Score médio.
    
    Exemplo
    -------
    >>> score = calcular_silhouette_score(X, labels)
    >>> print(f"Silhouette: {score:.4f}")
    """
    if len(set(labels)) < 2:
        return 0.0
    return silhouette_score(X, labels)


def calcular_silhouette_por_cluster(
    X: np.ndarray,
    labels: np.ndarray
) -> Dict[int, float]:
    """
    Calcula Silhouette Score para cada cluster individualmente.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    dict
        Dicionário com silhouette score por cluster.
    
    Exemplo
    -------
    >>> scores = calcular_silhouette_por_cluster(X, labels)
    >>> for c, s in scores.items():
    ...     print(f"Cluster {c}: {s:.4f}")
    """
    scores = silhouette_samples(X, labels)
    resultado = {}
    
    for cluster_id in np.unique(labels):
        mascara = labels == cluster_id
        resultado[int(cluster_id)] = float(np.mean(scores[mascara]))
    
    return resultado


def calcular_davies_bouldin(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calcula o Davies-Bouldin Index.
    
    O Davies-Bouldin Index mede a similaridade entre clusters. Valores mais
    baixos indicam melhor clustering (clusters mais compactos e separados).
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    float
        Davies-Bouldin Index.
    
    Exemplo
    -------
    >>> db = calcular_davies_bouldin(X, labels)
    >>> print(f"Davies-Bouldin: {db:.4f}")
    """
    if len(set(labels)) < 2:
        return np.inf
    return davies_bouldin_score(X, labels)


def calcular_calinski_harabasz(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calcula o Calinski-Harabasz Index (Variance Ratio Criterion).
    
    O Calinski-Harabasz Index é a razão entre a dispersão entre clusters e
    a dispersão dentro dos clusters. Valores mais altos indicam clusters
    mais densos e bem separados.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    float
        Calinski-Harabasz Index.
    
    Exemplo
    -------
    >>> ch = calcular_calinski_harabasz(X, labels)
    >>> print(f"Calinski-Harabasz: {ch:.2f}")
    """
    if len(set(labels)) < 2:
        return 0.0
    return calinski_harabasz_score(X, labels)


def calcular_ari_entre_runs(
    X: np.ndarray,
    algoritmo_func,
    n_runs: int = 10,
    **algoritmo_kwargs
) -> Dict[str, float]:
    """
    Calcula o Adjusted Rand Index (ARI) entre múltiplas execuções.
    
    Mede a estabilidade do clustering ao rodar o algoritmo múltiplas vezes
    com diferentes seeds. ARI próximo a 1 indica alta estabilidade.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    algoritmo_func : callable
        Função do algoritmo de clustering.
    n_runs : int, padrão=10
        Número de execuções.
    **algoritmo_kwargs
        Parâmetros para o algoritmo.
    
    Retorna
    -------
    dict
        Estatísticas do ARI (média, std, min, max).
    
    Exemplo
    -------
    >>> from sklearn.cluster import KMeans
    >>> ari_stats = calcular_ari_entre_runs(X, KMeans, n_clusters=5)
    """
    print(f"Calculando ARI entre {n_runs} execuções...")
    
    labels_list = []
    for i in range(n_runs):
        kwargs = algoritmo_kwargs.copy()
        kwargs['random_state'] = i * 100
        modelo = algoritmo_func(**kwargs)
        labels = modelo.fit_predict(X)
        labels_list.append(labels)
    
    # Calcular ARI entre todos os pares
    ari_values = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            ari = adjusted_rand_score(labels_list[i], labels_list[j])
            ari_values.append(ari)
    
    resultado = {
        'media': np.mean(ari_values),
        'std': np.std(ari_values),
        'min': np.min(ari_values),
        'max': np.max(ari_values),
        'ari_values': ari_values
    }
    
    print(f"- ARI médio: {resultado['media']:.4f} (±{resultado['std']:.4f})")
    
    return resultado


def calcular_wcss(X: np.ndarray, labels: np.ndarray, centroids: Optional[np.ndarray] = None) -> float:
    """
    Calcula a Soma dos Quadrados Dentro dos Clusters (WCSS).
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    centroids : np.ndarray, opcional
        Centroides dos clusters. Se None, calcula automaticamente.
    
    Retorna
    -------
    float
        Valor do WCSS.
    
    Exemplo
    -------
    >>> wcss = calcular_wcss(X, labels)
    """
    wcss = 0.0
    for cluster_id in np.unique(labels):
        pontos_cluster = X[labels == cluster_id]
        if centroids is not None:
            centroide = centroids[cluster_id]
        else:
            centroide = np.mean(pontos_cluster, axis=0)
        wcss += np.sum((pontos_cluster - centroide) ** 2)
    
    return wcss


def calcular_bcss(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calcula a Soma dos Quadrados Entre Clusters (BCSS).
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    float
        Valor do BCSS.
    
    Exemplo
    -------
    >>> bcss = calcular_bcss(X, labels)
    """
    centroide_geral = np.mean(X, axis=0)
    bcss = 0.0
    
    for cluster_id in np.unique(labels):
        pontos_cluster = X[labels == cluster_id]
        centroide_cluster = np.mean(pontos_cluster, axis=0)
        n_pontos = len(pontos_cluster)
        bcss += n_pontos * np.sum((centroide_cluster - centroide_geral) ** 2)
    
    return bcss


def calcular_inercia_total(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Calcula a inércia total (WCSS + BCSS).
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    
    Retorna
    -------
    float
        Inércia total.
    """
    return calcular_wcss(X, labels) + calcular_bcss(X, labels)


def comparar_multiplos_algoritmos(
    X: np.ndarray,
    resultados: Dict[str, Dict]
) -> pd.DataFrame:
    """
    Compara múltiplos algoritmos de clustering em um DataFrame.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    resultados : dict
        Dicionário com resultados de cada algoritmo.
        Formato: {'nome': {'labels': [...], ...}, ...}
    
    Retorna
    -------
    pd.DataFrame
        DataFrame comparativo das métricas.
    
    Exemplo
    -------
    >>> resultados = {'K-Means': {'labels': labels_km}, 'DBSCAN': {'labels': labels_db}}
    >>> df_comp = comparar_multiplos_algoritmos(X, resultados)
    """
    comparacoes = []
    
    for nome, res in resultados.items():
        labels = res['labels']
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        metricas = {
            'Algoritmo': nome,
            'Clusters': n_clusters,
            'Silhouette': calcular_silhouette_score(X, labels),
            'Davies-Bouldin': calcular_davies_bouldin(X, labels),
            'Calinski-Harabasz': calcular_calinski_harabasz(X, labels)
        }
        
        # Adicionar tamanho dos clusters
        unique, counts = np.unique(labels, return_counts=True)
        metricas['Menor_Cluster'] = min(counts)
        metricas['Maior_Cluster'] = max(counts)
        
        comparacoes.append(metricas)
    
    return pd.DataFrame(comparacoes)


def gerar_relatorio_metricas(
    X: np.ndarray,
    labels: np.ndarray,
    nome_algoritmo: str = "Clustering"
) -> Dict:
    """
    Gera um relatório completo de métricas para um clustering.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    nome_algoritmo : str, padrão="Clustering"
        Nome do algoritmo usado.
    
    Retorna
    -------
    dict
        Relatório completo com todas as métricas.
    
    Exemplo
    -------
    >>> relatorio = gerar_relatorio_metricas(X, labels, "K-Means")
    >>> print(relatorio['resumo'])
    """
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_amostras = len(labels)
    n_ruido = list(labels).count(-1) if -1 in labels else 0
    
    # Silhouette
    sil_media = calcular_silhouette_score(X, labels)
    sil_por_cluster = calcular_silhouette_por_cluster(X, labels)
    
    # Outras métricas
    db = calcular_davies_bouldin(X, labels)
    ch = calcular_calinski_harabasz(X, labels)
    wcss = calcular_wcss(X, labels)
    
    # Tamanho dos clusters
    unique, counts = np.unique(labels, return_counts=True)
    tamanhos = dict(zip(unique.tolist(), counts.tolist()))
    
    relatorio = {
        'algoritmo': nome_algoritmo,
        'n_clusters': n_clusters,
        'n_amostras': n_amostras,
        'n_ruido': n_ruido,
        'metricas': {
            'silhouette_media': sil_media,
            'silhouette_por_cluster': sil_por_cluster,
            'davies_bouldin': db,
            'calinski_harabasz': ch,
            'wcss': wcss
        },
        'tamanho_clusters': tamanhos,
        'resumo': f"""
{'='*60}
RELATÓRIO DE MÉTRICAS - {nome_algoritmo}
{'='*60}
Número de clusters: {n_clusters}
Total de amostras: {n_amostras}
Pontos de ruído: {n_ruido}

MÉTRICAS DE QUALIDADE:
- Silhouette Score: {sil_media:.4f}
- Davies-Bouldin Index: {db:.4f}
- Calinski-Harabasz Index: {ch:.2f}
- WCSS: {wcss:.2f}

TAMANHO DOS CLUSTERS:
{tamanhos}

SILHOUETTE POR CLUSTER:
{chr(10).join([f'  Cluster {c}: {s:.4f}' for c, s in sil_por_cluster.items()])}
{'='*60}
        """.strip()
    }
    
    print(relatorio['resumo'])
    
    return relatorio


def analise_estabilidade_kmeans(
    X: np.ndarray,
    k_range: range = range(2, 11),
    n_runs: int = 10
) -> pd.DataFrame:
    """
    Analisa a estabilidade do K-Means para diferentes valores de k.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    k_range : range, padrão=range(2, 11)
        Range de valores de k a testar.
    n_runs : int, padrão=10
        Número de execuções por k.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame com estatísticas de estabilidade por k.
    
    Exemplo
    -------
    >>> df_est = analise_estabilidade_kmeans(X, range(2, 8), n_runs=10)
    """
    from sklearn.cluster import KMeans
    
    resultados = []
    
    for k in k_range:
        ari_stats = calcular_ari_entre_runs(
            X, KMeans, n_runs=n_runs, n_clusters=k
        )
        
        resultados.append({
            'k': k,
            'ari_media': ari_stats['media'],
            'ari_std': ari_stats['std'],
            'ari_min': ari_stats['min'],
            'ari_max': ari_stats['max']
        })
    
    return pd.DataFrame(resultados)


def salvar_relatorio_csv(
    relatorio: Dict,
    caminho_saida: str
) -> None:
    """
    Salva as métricas do relatório em arquivo CSV.
    
    Parâmetros
    ----------
    relatorio : dict
        Relatório gerado por gerar_relatorio_metricas.
    caminho_saida : str
        Caminho do arquivo CSV de saída.
    
    Exemplo
    -------
    >>> rel = gerar_relatorio_metricas(X, labels, "K-Means")
    >>> salvar_relatorio_csv(rel, 'metricas.csv')
    """
    # Criar DataFrame com métricas
    df_metricas = pd.DataFrame([{
        'Algoritmo': relatorio['algoritmo'],
        'N_Clusters': relatorio['n_clusters'],
        'N_Amostras': relatorio['n_amostras'],
        'N_Ruido': relatorio['n_ruido'],
        'Silhouette': relatorio['metricas']['silhouette_media'],
        'Davies_Bouldin': relatorio['metricas']['davies_bouldin'],
        'Calinski_Harabasz': relatorio['metricas']['calinski_harabasz'],
        'WCSS': relatorio['metricas']['wcss']
    }])
    
    df_metricas.to_csv(caminho_saida, index=False)
    print(f"Relatório salvo em: {caminho_saida}")
