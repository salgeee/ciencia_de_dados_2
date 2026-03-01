"""
Módulos para análise de clustering do ENEM.

Este pacote contém utilitários para:
- Preparação de dados do ENEM
- Aplicação de algoritmos de clustering
- Cálculo de métricas de avaliação
- Visualização de resultados
"""

from .data_prep import (
    carregar_dados_enem,
    limpar_dados_enem,
    agregar_por_escola,
    preparar_features_clustering,
    criar_features_adicionais,
    pipeline_preparacao
)

from .clustering import (
    kmeans_multi_seed,
    aplicar_dbscan,
    aplicar_hierarchical,
    aplicar_gaussian_mixture,
    metodo_elbow,
    analise_silhouette,
    comparar_algoritmos,
    pipeline_clustering
)

from .metrics import (
    calcular_silhouette_score,
    calcular_davies_bouldin,
    calcular_calinski_harabasz,
    calcular_ari_entre_runs,
    comparar_multiplos_algoritmos,
    gerar_relatorio_metricas,
    analise_estabilidade_kmeans
)

from .visualization import (
    plotar_elbow,
    plotar_silhouette_analysis,
    plotar_clusters_2d,
    plotar_heatmap_correlacao,
    plotar_perfil_clusters,
    plotar_dendrograma,
    plotar_tamanho_clusters
)

__version__ = "1.0.0"
__author__ = "Equipe Ciência de Dados II - UFU"

__all__ = [
    # data_prep
    "carregar_dados_enem",
    "limpar_dados_enem",
    "agregar_por_escola",
    "preparar_features_clustering",
    "criar_features_adicionais",
    "pipeline_preparacao",
    # clustering
    "kmeans_multi_seed",
    "aplicar_dbscan",
    "aplicar_hierarchical",
    "aplicar_gaussian_mixture",
    "metodo_elbow",
    "analise_silhouette",
    "comparar_algoritmos",
    "pipeline_clustering",
    # metrics
    "calcular_silhouette_score",
    "calcular_davies_bouldin",
    "calcular_calinski_harabasz",
    "calcular_ari_entre_runs",
    "comparar_multiplos_algoritmos",
    "gerar_relatorio_metricas",
    "analise_estabilidade_kmeans",
    # visualization
    "plotar_elbow",
    "plotar_silhouette_analysis",
    "plotar_clusters_2d",
    "plotar_heatmap_correlacao",
    "plotar_perfil_clusters",
    "plotar_dendrograma",
    "plotar_tamanho_clusters",
]
