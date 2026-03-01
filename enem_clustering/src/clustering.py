"""
Módulo de algoritmos de clustering para análise do ENEM.

Contém implementações de K-Means, DBSCAN, Hierarchical Clustering e Gaussian Mixture
com funções para determinação automática do número ótimo de clusters.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from typing import Tuple, List, Dict, Optional
import warnings

warnings.filterwarnings('ignore')


def kmeans_multi_seed(
    X: np.ndarray,
    n_clusters: int,
    n_seeds: int = 10,
    max_iter: int = 300,
    random_state: Optional[int] = None
) -> Tuple[KMeans, np.ndarray, float]:
    """
    Aplica K-Means com múltiplos seeds para encontrar a melhor inicialização.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    n_clusters : int
        Número de clusters.
    n_seeds : int, padrão=10
        Número de seeds diferentes para testar.
    max_iter : int, padrão=300
        Número máximo de iterações.
    random_state : int, opcional
        Seed para reprodutibilidade.
    
    Retorna
    -------
    tuple
        - Melhor modelo KMeans
        - Labels dos clusters
        - Inertia do melhor modelo
    
    Exemplo
    -------
    >>> modelo, labels, inertia = kmeans_multi_seed(X, n_clusters=5, n_seeds=10)
    """
    print(f"K-Means com {n_seeds} seeds (k={n_clusters})")
    
    melhor_modelo = None
    melhor_inertia = np.inf
    
    seeds = np.random.RandomState(random_state).randint(0, 10000, size=n_seeds)
    
    for seed in seeds:
        modelo = KMeans(
            n_clusters=n_clusters,
            max_iter=max_iter,
            n_init=1,
            random_state=seed
        )
        modelo.fit(X)
        
        if modelo.inertia_ < melhor_inertia:
            melhor_inertia = modelo.inertia_
            melhor_modelo = modelo
    
    print(f"- Melhor inertia: {melhor_inertia:.2f}")
    
    return melhor_modelo, melhor_modelo.labels_, melhor_inertia


def aplicar_dbscan(
    X: np.ndarray,
    eps: float = 0.5,
    min_samples: int = 5,
    metric: str = 'euclidean'
) -> Tuple[DBSCAN, np.ndarray, int]:
    """
    Aplica DBSCAN para clustering.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    eps : float, padrão=0.5
        Distância máxima entre vizinhos.
    min_samples : int, padrão=5
        Número mínimo de pontos para formar cluster.
    metric : str, padrão='euclidean'
        Métrica de distância.
    
    Retorna
    -------
    tuple
        - Modelo DBSCAN
        - Labels dos clusters
        - Número de clusters (excluindo ruído)
    
    Exemplo
    -------
    >>> modelo, labels, n_clusters = aplicar_dbscan(X, eps=0.5, min_samples=5)
    """
    print(f"DBSCAN (eps={eps}, min_samples={min_samples})")
    
    modelo = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    labels = modelo.fit_predict(X)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"- Clusters encontrados: {n_clusters}")
    print(f"- Pontos de ruído: {n_noise} ({100*n_noise/len(labels):.1f}%)")
    
    return modelo, labels, n_clusters


def aplicar_hierarchical(
    X: np.ndarray,
    n_clusters: int,
    linkage: str = 'ward',
    metric: str = 'euclidean'
) -> Tuple[AgglomerativeClustering, np.ndarray]:
    """
    Aplica Hierarchical Clustering.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    n_clusters : int
        Número de clusters.
    linkage : str, padrão='ward'
        Método de linkage ('ward', 'complete', 'average', 'single').
    metric : str, padrão='euclidean'
        Métrica de distância.
    
    Retorna
    -------
    tuple
        - Modelo AgglomerativeClustering
        - Labels dos clusters
    
    Exemplo
    -------
    >>> modelo, labels = aplicar_hierarchical(X, n_clusters=5, linkage='ward')
    """
    print(f"Hierarchical Clustering (k={n_clusters}, linkage={linkage})")
    
    modelo = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage,
        metric=metric
    )
    labels = modelo.fit_predict(X)
    
    return modelo, labels


def aplicar_gaussian_mixture(
    X: np.ndarray,
    n_components: int,
    covariance_type: str = 'full',
    max_iter: int = 100,
    random_state: int = 42
) -> Tuple[GaussianMixture, np.ndarray, np.ndarray]:
    """
    Aplica Gaussian Mixture Model para clustering.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    n_components : int
        Número de componentes (clusters).
    covariance_type : str, padrão='full'
        Tipo de covariância.
    max_iter : int, padrão=100
        Número máximo de iterações.
    random_state : int, padrão=42
        Seed para reprodutibilidade.
    
    Retorna
    -------
    tuple
        - Modelo GaussianMixture
        - Labels dos clusters
        - Probabilidades de pertencimento
    
    Exemplo
    -------
    >>> modelo, labels, probs = aplicar_gaussian_mixture(X, n_components=5)
    """
    print(f"Gaussian Mixture (k={n_components}, covariance={covariance_type})")
    
    modelo = GaussianMixture(
        n_components=n_components,
        covariance_type=covariance_type,
        max_iter=max_iter,
        random_state=random_state
    )
    labels = modelo.fit_predict(X)
    probs = modelo.predict_proba(X)
    
    print(f"- Convergência: {modelo.converged_}")
    print(f"- Iterações: {modelo.n_iter_}")
    
    return modelo, labels, probs


def metodo_elbow(
    X: np.ndarray,
    k_range: range = range(2, 11),
    n_seeds: int = 5,
    plot: bool = False
) -> Tuple[List[int], List[float], int]:
    """
    Determina número ótimo de clusters pelo método do cotovelo (elbow).
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    k_range : range, padrão=range(2, 11)
        Range de valores de k a testar.
    n_seeds : int, padrão=5
        Número de seeds por k.
    plot : bool, padrão=False
        Se True, plota o gráfico.
    
    Retorna
    -------
    tuple
        - Lista de k testados
        - Lista de inertias
        - K ótimo sugerido
    
    Exemplo
    -------
    >>> ks, inertias, k_otimo = metodo_elbow(X, k_range=range(2, 11))
    """
    print("\nMétodo do Cotovelo (Elbow):")
    
    ks = list(k_range)
    inertias = []
    
    for k in ks:
        _, _, inertia = kmeans_multi_seed(X, n_clusters=k, n_seeds=n_seeds)
        inertias.append(inertia)
    
    # Calcular k ótimo pela segunda derivada
    diffs = np.diff(inertias)
    diffs2 = np.diff(diffs)
    k_otimo_idx = np.argmin(diffs2) + 1
    k_otimo = ks[k_otimo_idx] if k_otimo_idx < len(ks) else ks[len(ks)//2]
    
    print(f"- K sugerido: {k_otimo}")
    
    if plot:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 5))
        plt.plot(ks, inertias, 'bo-')
        plt.axvline(k_otimo, color='r', linestyle='--', label=f'K sugerido: {k_otimo}')
        plt.xlabel('Número de Clusters (k)')
        plt.ylabel('Inertia')
        plt.title('Método do Cotovelo')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    return ks, inertias, k_otimo


def analise_silhouette(
    X: np.ndarray,
    k_range: range = range(2, 11),
    n_seeds: int = 5
) -> Tuple[List[int], List[float], int]:
    """
    Determina número ótimo de clusters pela análise de Silhouette.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    k_range : range, padrão=range(2, 11)
        Range de valores de k a testar.
    n_seeds : int, padrão=5
        Número de seeds por k.
    
    Retorna
    -------
    tuple
        - Lista de k testados
        - Lista de silhouette scores
        - K ótimo (maior silhouette)
    
    Exemplo
    -------
    >>> ks, scores, k_otimo = analise_silhouette(X, k_range=range(2, 11))
    """
    print("\nAnálise de Silhouette:")
    
    ks = list(k_range)
    scores = []
    
    for k in ks:
        _, labels, _ = kmeans_multi_seed(X, n_clusters=k, n_seeds=n_seeds)
        score = silhouette_score(X, labels)
        scores.append(score)
        print(f"  k={k}: silhouette={score:.4f}")
    
    k_otimo = ks[np.argmax(scores)]
    print(f"- Melhor k: {k_otimo} (silhouette={max(scores):.4f})")
    
    return ks, scores, k_otimo


def comparar_algoritmos(
    X: np.ndarray,
    k: int,
    n_seeds: int = 5
) -> Dict[str, Dict]:
    """
    Compara múltiplos algoritmos de clustering.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    k : int
        Número de clusters.
    n_seeds : int, padrão=5
        Número de seeds para K-Means.
    
    Retorna
    -------
    dict
        Dicionário com resultados de cada algoritmo.
    
    Exemplo
    -------
    >>> resultados = comparar_algoritmos(X, k=5)
    """
    print(f"\nComparando algoritmos (k={k}):")
    print("="*50)
    
    resultados = {}
    
    # K-Means
    print("\n1. K-Means")
    modelo_km, labels_km, _ = kmeans_multi_seed(X, n_clusters=k, n_seeds=n_seeds)
    resultados['K-Means'] = {
        'modelo': modelo_km,
        'labels': labels_km,
        'silhouette': silhouette_score(X, labels_km),
        'davies_bouldin': davies_bouldin_score(X, labels_km),
        'calinski_harabasz': calinski_harabasz_score(X, labels_km)
    }
    
    # Hierarchical
    print("\n2. Hierarchical")
    modelo_hc, labels_hc = aplicar_hierarchical(X, n_clusters=k)
    resultados['Hierarchical'] = {
        'modelo': modelo_hc,
        'labels': labels_hc,
        'silhouette': silhouette_score(X, labels_hc),
        'davies_bouldin': davies_bouldin_score(X, labels_hc),
        'calinski_harabasz': calinski_harabasz_score(X, labels_hc)
    }
    
    # Gaussian Mixture
    print("\n3. Gaussian Mixture")
    modelo_gm, labels_gm, _ = aplicar_gaussian_mixture(X, n_components=k)
    resultados['GaussianMixture'] = {
        'modelo': modelo_gm,
        'labels': labels_gm,
        'silhouette': silhouette_score(X, labels_gm),
        'davies_bouldin': davies_bouldin_score(X, labels_gm),
        'calinski_harabasz': calinski_harabasz_score(X, labels_gm)
    }
    
    # Resumo
    print("\n" + "="*50)
    print("RESUMO DA COMPARAÇÃO")
    print("="*50)
    for nome, res in resultados.items():
        print(f"{nome}:")
        print(f"  Silhouette: {res['silhouette']:.4f}")
        print(f"  Davies-Bouldin: {res['davies_bouldin']:.4f}")
        print(f"  Calinski-Harabasz: {res['calinski_harabasz']:.2f}")
    
    return resultados


def pipeline_clustering(
    X: np.ndarray,
    algoritmo: str = 'kmeans',
    k: Optional[int] = None,
    auto_k: bool = True,
    k_range: range = range(2, 11),
    **kwargs
) -> Dict:
    """
    Pipeline completo de clustering com seleção automática de k.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    algoritmo : str, padrão='kmeans'
        Algoritmo a usar ('kmeans', 'hierarchical', 'dbscan', 'gmm').
    k : int, opcional
        Número de clusters. Se None e auto_k=True, determina automaticamente.
    auto_k : bool, padrão=True
        Se True, determina k automaticamente.
    k_range : range, padrão=range(2, 11)
        Range para busca de k.
    **kwargs
        Parâmetros adicionais para os algoritmos.
    
    Retorna
    -------
    dict
        Dicionário com modelo, labels e métricas.
    
    Exemplo
    -------
    >>> resultado = pipeline_clustering(X, algoritmo='kmeans', auto_k=True)
    """
    print("\n" + "="*60)
    print("PIPELINE DE CLUSTERING")
    print("="*60)
    
    # Determinar k automaticamente
    if k is None and auto_k and algoritmo != 'dbscan':
        _, _, k = analise_silhouette(X, k_range=k_range)
    elif k is None:
        k = 5
    
    print(f"\nAlgoritmo: {algoritmo}")
    print(f"Número de clusters: {k}")
    
    # Aplicar algoritmo
    if algoritmo.lower() == 'kmeans':
        modelo, labels, _ = kmeans_multi_seed(
            X, n_clusters=k,
            n_seeds=kwargs.get('n_seeds', 10)
        )
    elif algoritmo.lower() in ['hierarchical', 'hierarquico']:
        modelo, labels = aplicar_hierarchical(
            X, n_clusters=k,
            linkage=kwargs.get('linkage', 'ward')
        )
    elif algoritmo.lower() == 'dbscan':
        modelo, labels, n_clust = aplicar_dbscan(
            X,
            eps=kwargs.get('eps', 0.5),
            min_samples=kwargs.get('min_samples', 5)
        )
        k = n_clust
    elif algoritmo.lower() in ['gmm', 'gaussian_mixture']:
        modelo, labels, probs = aplicar_gaussian_mixture(
            X, n_components=k,
            covariance_type=kwargs.get('covariance_type', 'full')
        )
    else:
        raise ValueError(f"Algoritmo '{algoritmo}' não reconhecido")
    
    # Calcular métricas
    resultado = {
        'algoritmo': algoritmo,
        'k': k,
        'modelo': modelo,
        'labels': labels,
        'silhouette': silhouette_score(X, labels) if len(set(labels)) > 1 else 0,
        'davies_bouldin': davies_bouldin_score(X, labels) if len(set(labels)) > 1 else 0,
        'calinski_harabasz': calinski_harabasz_score(X, labels) if len(set(labels)) > 1 else 0
    }
    
    print("\n" + "="*60)
    print("CLUSTERING CONCLUÍDO")
    print("="*60)
    print(f"Silhouette Score: {resultado['silhouette']:.4f}")
    print(f"Davies-Bouldin: {resultado['davies_bouldin']:.4f}")
    print(f"Calinski-Harabasz: {resultado['calinski_harabasz']:.2f}")
    
    return resultado
