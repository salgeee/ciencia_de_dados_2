"""
Módulo de visualização para análise de clustering do ENEM.

Contém funções para plotar gráficos de avaliação de clustering,
visualização de clusters e perfis de grupos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_samples
from scipy.cluster.hierarchy import dendrogram, linkage
from typing import Optional, List, Tuple
import warnings

warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def plotar_elbow(
    ks: List[int],
    inertias: List[float],
    k_otimo: Optional[int] = None,
    figsize: Tuple[int, int] = (10, 6),
    titulo: str = "Método do Cotovelo",
    salvar: Optional[str] = None
) -> None:
    """
    Plota o gráfico do método do cotovelo para determinação de k.
    
    Parâmetros
    ----------
    ks : list
        Lista de valores de k testados.
    inertias : list
        Lista de inertias correspondentes.
    k_otimo : int, opcional
        Valor de k sugerido (destacado no gráfico).
    figsize : tuple, padrão=(10, 6)
        Tamanho da figura.
    titulo : str, padrão="Método do Cotovelo"
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar a imagem.
    
    Exemplo
    -------
    >>> plotar_elbow(ks, inertias, k_otimo=5)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(ks, inertias, 'bo-', linewidth=2, markersize=8)
    
    if k_otimo:
        idx = ks.index(k_otimo) if k_otimo in ks else None
        if idx is not None:
            ax.axvline(k_otimo, color='r', linestyle='--', 
                      label=f'K sugerido: {k_otimo}')
            ax.plot(k_otimo, inertias[idx], 'ro', markersize=12)
    
    ax.set_xlabel('Número de Clusters (k)', fontsize=12)
    ax.set_ylabel('Inertia (WCSS)', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_silhouette_analysis(
    X: np.ndarray,
    labels: np.ndarray,
    figsize: Tuple[int, int] = (12, 8),
    titulo: str = "Análise de Silhouette",
    salvar: Optional[str] = None
) -> None:
    """
    Plota a análise detalhada de silhouette por cluster.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    figsize : tuple, padrão=(12, 8)
        Tamanho da figura.
    titulo : str, padrão="Análise de Silhouette"
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar a imagem.
    
    Exemplo
    -------
    >>> plotar_silhouette_analysis(X, labels)
    """
    from sklearn.metrics import silhouette_score
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    silhouette_avg = silhouette_score(X, labels)
    sample_silhouette_values = silhouette_samples(X, labels)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Silhouette plot
    y_lower = 10
    colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))
    
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[labels == i]
        ith_cluster_silhouette_values.sort()
        
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
        
        color = colors[i]
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i),
                fontsize=10, ha='right')
        
        y_lower = y_upper + 10
    
    ax1.set_xlabel('Coeficiente de Silhouette', fontsize=11)
    ax1.set_ylabel('Cluster', fontsize=11)
    ax1.set_title('Silhouette por Cluster', fontsize=12, fontweight='bold')
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--",
               label=f'Média: {silhouette_avg:.3f}')
    ax1.legend(loc='lower right')
    
    # Scatter plot com PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    scatter = ax2.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, 
                         cmap='tab10', alpha=0.6, edgecolors='w', s=50)
    ax2.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', fontsize=11)
    ax2.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', fontsize=11)
    ax2.set_title('Clusters em 2D (PCA)', fontsize=12, fontweight='bold')
    plt.colorbar(scatter, ax=ax2, label='Cluster')
    
    fig.suptitle(titulo, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_clusters_2d(
    X: np.ndarray,
    labels: np.ndarray,
    metodo: str = 'pca',
    figsize: Tuple[int, int] = (10, 8),
    titulo: str = "Visualização dos Clusters",
    salvar: Optional[str] = None,
    **kwargs
) -> None:
    """
    Plota clusters em 2D usando PCA ou t-SNE.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels : np.ndarray
        Labels dos clusters.
    metodo : str, padrão='pca'
        Método de redução ('pca' ou 'tsne').
    figsize : tuple, padrão=(10, 8)
        Tamanho da figura.
    titulo : str, padrão="Visualização dos Clusters"
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar a imagem.
    **kwargs
        Parâmetros adicionais para t-SNE.
    
    Exemplo
    -------
    >>> plotar_clusters_2d(X, labels, metodo='pca')
    >>> plotar_clusters_2d(X, labels, metodo='tsne', perplexity=30)
    """
    if metodo.lower() == 'pca':
        reducer = PCA(n_components=2)
        X_2d = reducer.fit_transform(X)
        xlabel = f'PC1 ({reducer.explained_variance_ratio_[0]:.1%})'
        ylabel = f'PC2 ({reducer.explained_variance_ratio_[1]:.1%})'
    elif metodo.lower() == 'tsne':
        print("Aplicando t-SNE (pode levar alguns segundos)...")
        reducer = TSNE(
            n_components=2,
            perplexity=kwargs.get('perplexity', 30),
            learning_rate=kwargs.get('learning_rate', 'auto'),
            random_state=kwargs.get('random_state', 42),
            n_iter=1000
        )
        X_2d = reducer.fit_transform(X)
        xlabel = 't-SNE 1'
        ylabel = 't-SNE 2'
    else:
        raise ValueError("Método deve ser 'pca' ou 'tsne'")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1], c=labels,
                        cmap='tab10', alpha=0.7, edgecolors='w', s=60)
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f'{titulo} ({metodo.upper()})', fontsize=14, fontweight='bold')
    
    # Legenda
    legend = ax.legend(*scatter.legend_elements(),
                      title="Clusters", loc='best')
    ax.add_artist(legend)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_heatmap_correlacao(
    df: pd.DataFrame,
    colunas: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (12, 10),
    titulo: str = "Mapa de Correlação",
    salvar: Optional[str] = None
) -> None:
    """
    Plota heatmap de correlação entre variáveis.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com os dados.
    colunas : list, opcional
        Lista de colunas para incluir. Se None, usa todas numéricas.
    figsize : tuple, padrão=(12, 10)
        Tamanho da figura.
    titulo : str, padrão="Mapa de Correlação"
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar a imagem.
    
    Exemplo
    -------
    >>> plotar_heatmap_correlacao(df, colunas=['NU_NOTA_MT', 'NU_NOTA_CN'])
    """
    if colunas:
        df_corr = df[colunas].select_dtypes(include=[np.number])
    else:
        df_corr = df.select_dtypes(include=[np.number])
    
    corr = df_corr.corr()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                annot=True, fmt='.2f', annot_kws={'size': 9}, ax=ax)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_perfil_clusters(
    df: pd.DataFrame,
    labels: np.ndarray,
    colunas: List[str],
    figsize: Tuple[int, int] = (15, 10),
    titulo: str = "Perfil dos Clusters",
    salvar: Optional[str] = None,
    kind: str = 'box'
) -> None:
    """
    Plota boxplots ou violin plots do perfil dos clusters.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com os dados.
    labels : np.ndarray
        Labels dos clusters.
    colunas : list
        Lista de colunas para visualizar.
    figsize : tuple, padrão=(15, 10)
        Tamanho da figura.
    titulo : str, padrão="Perfil dos Clusters"
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar a imagem.
    kind : str, padrão='box'
        Tipo de plot ('box' ou 'violin').
    
    Exemplo
    -------
    >>> plotar_perfil_clusters(df, labels, ['NU_NOTA_MT', 'NU_NOTA_CN'])
    """
    df_plot = df.copy()
    df_plot['Cluster'] = labels
    
    n_cols = 3
    n_rows = (len(colunas) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    for i, col in enumerate(colunas):
        if col in df_plot.columns:
            if kind == 'box':
                sns.boxplot(data=df_plot, x='Cluster', y=col, ax=axes[i])
            elif kind == 'violin':
                sns.violinplot(data=df_plot, x='Cluster', y=col, ax=axes[i])
            axes[i].set_title(col, fontsize=11)
            axes[i].set_xlabel('Cluster')
        else:
            axes[i].text(0.5, 0.5, f'Coluna {col} não encontrada',
                        ha='center', va='center')
            axes[i].set_xticks([])
            axes[i].set_yticks([])
    
    # Remover subplots vazios
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    fig.suptitle(titulo, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_dendrograma(
    X: np.ndarray,
    labels_amostra: Optional[List[str]] = None,
    metodo: str = 'ward',
    metric: str = 'euclidean',
    figsize: Tuple[int, int] = (15, 8),
    titulo: str = "Dendrograma - Clustering Hierárquico",
    max_d: Optional[float] = None,
    truncate_mode: str = 'level',
    p: int = 10,
    salvar: Optional[str] = None
) -> None:
    """
    Plota o dendrograma do clustering hierárquico.
    
    Parâmetros
    ----------
    X : np.ndarray
        Dados de entrada.
    labels_amostra : list, opcional
        Labels para as amostras.
    metodo : str, padrão='ward'
        Método de linkage.
    metric : str, padrão='euclidean'
        Métrica de distância.
    figsize : tuple, padrão=(15, 8)
        Tamanho da figura.
    titulo : str, padrão="Dendrograma"
        Título do gráfico.
    max_d : float, opcional
        Altura máxima para corte (linha horizontal).
    truncate_mode : str, padrão='level'
        Modo de truncamento ('level', 'lastp', ou None).
    p : int, padrão=10
        Número de níveis ou clusters para mostrar.
    salvar : str, opcional
        Caminho para salvar a imagem.
    
    Exemplo
    -------
    >>> plotar_dendrograma(X, max_d=50)
    """
    print("Calculando linkage (pode levar alguns segundos)...")
    Z = linkage(X, method=metodo, metric=metric)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    dendrogram(Z,
               labels=labels_amostra,
               truncate_mode=truncate_mode,
               p=p,
               leaf_rotation=90,
               leaf_font_size=10,
               show_contracted=True,
               ax=ax)
    
    ax.set_xlabel('Amostras' if labels_amostra else 'Índice', fontsize=12)
    ax.set_ylabel('Distância', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    if max_d:
        ax.axhline(y=max_d, c='r', linestyle='--', 
                  label=f'Corte: {max_d}')
        ax.legend()
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_comparacao_silhouette(
    ks: List[int],
    scores: List[float],
    k_otimo: Optional[int] = None,
    figsize: Tuple[int, int] = (10, 6),
    titulo: str = "Silhouette Score por Número de Clusters",
    salvar: Optional[str] = None
) -> None:
    """
    Plota a comparação de Silhouette Score para diferentes k.
    
    Parâmetros
    ----------
    ks : list
        Lista de valores de k.
    scores : list
        Lista de silhouette scores.
    k_otimo : int, opcional
        Valor de k ótimo.
    figsize : tuple, padrão=(10, 6)
        Tamanho da figura.
    titulo : str
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar.
    
    Exemplo
    -------
    >>> plotar_comparacao_silhouette(ks, scores, k_otimo=5)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(ks, scores, 'go-', linewidth=2, markersize=8)
    
    if k_otimo and k_otimo in ks:
        idx = ks.index(k_otimo)
        ax.axvline(k_otimo, color='r', linestyle='--',
                  label=f'Melhor k: {k_otimo}')
        ax.plot(k_otimo, scores[idx], 'ro', markersize=12)
    
    ax.set_xlabel('Número de Clusters (k)', fontsize=12)
    ax.set_ylabel('Silhouette Score', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xticks(ks)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_tamanho_clusters(
    labels: np.ndarray,
    figsize: Tuple[int, int] = (10, 6),
    titulo: str = "Distribuição dos Clusters",
    salvar: Optional[str] = None
) -> None:
    """
    Plota gráfico de barras com o tamanho de cada cluster.
    
    Parâmetros
    ----------
    labels : np.ndarray
        Labels dos clusters.
    figsize : tuple, padrão=(10, 6)
        Tamanho da figura.
    titulo : str
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar.
    
    Exemplo
    -------
    >>> plotar_tamanho_clusters(labels)
    """
    unique, counts = np.unique(labels, return_counts=True)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['gray' if c == -1 else plt.cm.tab10(i) 
              for i, c in enumerate(unique)]
    
    bars = ax.bar(range(len(unique)), counts, color=colors, edgecolor='black')
    
    # Adicionar valores nas barras
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{count}\n({100*count/len(labels):.1f}%)',
               ha='center', va='bottom', fontsize=10)
    
    ax.set_xticks(range(len(unique)))
    ax.set_xticklabels([f'Ruído' if c == -1 else f'Cluster {c}' 
                       for c in unique])
    ax.set_ylabel('Número de Amostras', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()


def plotar_radar_clusters(
    df: pd.DataFrame,
    labels: np.ndarray,
    colunas: List[str],
    figsize: Tuple[int, int] = (12, 12),
    titulo: str = "Perfil Radar dos Clusters",
    salvar: Optional[str] = None
) -> None:
    """
    Plota gráfico radar comparando médias dos clusters.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com os dados.
    labels : np.ndarray
        Labels dos clusters.
    colunas : list
        Lista de colunas para o radar.
    figsize : tuple, padrão=(12, 12)
        Tamanho da figura.
    titulo : str
        Título do gráfico.
    salvar : str, opcional
        Caminho para salvar.
    
    Exemplo
    -------
    >>> plotar_radar_clusters(df, labels, ['NU_NOTA_MT', 'NU_NOTA_CN'])
    """
    df_plot = df.copy()
    df_plot['Cluster'] = labels
    
    # Calcular médias por cluster
    medias = df_plot.groupby('Cluster')[colunas].mean()
    
    # Normalizar para escala 0-1
    medias_norm = (medias - medias.min()) / (medias.max() - medias.min())
    
    # Configurar radar
    angles = np.linspace(0, 2 * np.pi, len(colunas), endpoint=False).tolist()
    angles += angles[:1]  # Fechar o círculo
    
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(medias_norm)))
    
    for i, (cluster, row) in enumerate(medias_norm.iterrows()):
        values = row.tolist()
        values += values[:1]  # Fechar o círculo
        
        ax.plot(angles, values, 'o-', linewidth=2, 
               label=f'Cluster {cluster}', color=colors[i])
        ax.fill(angles, values, alpha=0.15, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(colunas, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    plt.show()
