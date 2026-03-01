"""
Módulo de preparação de dados para clustering do ENEM.

Contém funções para carregar, limpar, agregar e pré-processar dados do ENEM
para análise de clustering de escolas.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple, List, Optional
import warnings

warnings.filterwarnings('ignore')


def carregar_dados_enem(
    caminho_arquivo: str,
    amostra: Optional[float] = None,
    colunas: Optional[List[str]] = None,
    encoding: str = 'latin1',
    sep: str = ';',
    random_state: int = 42
) -> pd.DataFrame:
    """
    Carrega dados do ENEM de um arquivo CSV.
    
    Parâmetros
    ----------
    caminho_arquivo : str
        Caminho para o arquivo CSV dos microdados do ENEM.
    amostra : float, opcional
        Fração dos dados a ser carregada (0.0 a 1.0) para arquivos grandes.
        Se None, carrega todos os dados.
    colunas : list, opcional
        Lista de colunas específicas a carregar. Se None, carrega todas.
    encoding : str, padrão='latin1'
        Encoding do arquivo CSV.
    sep : str, padrão=';'
        Separador do CSV.
    random_state : int, padrão=42
        Seed para reprodutibilidade da amostragem.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame com os dados carregados.
    
    Exemplo
    -------
    >>> df = carregar_dados_enem('microdados_enem_2024.csv', amostra=0.1)
    """
    print(f"Carregando dados de: {caminho_arquivo}")
    
    if amostra is not None and 0 < amostra < 1:
        print(f"Aplicando amostragem de {amostra*100:.1f}%")
        df = pd.read_csv(
            caminho_arquivo,
            usecols=colunas,
            encoding=encoding,
            sep=sep,
            low_memory=False
        )
        df = df.sample(frac=amostra, random_state=random_state).reset_index(drop=True)
    else:
        df = pd.read_csv(
            caminho_arquivo,
            usecols=colunas,
            encoding=encoding,
            sep=sep,
            low_memory=False
        )
    
    print(f"Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df


def limpar_dados_enem(
    df: pd.DataFrame,
    min_alunos_por_escola: int = 10,
    coluna_escola: str = 'CO_ESCOLA',
    colunas_notas: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Limpa dados do ENEM removendo escolas com poucos alunos e tratando missing.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com dados do ENEM.
    min_alunos_por_escola : int, padrão=10
        Número mínimo de alunos por escola para ser incluída.
    coluna_escola : str, padrão='CO_ESCOLA'
        Nome da coluna que identifica a escola.
    colunas_notas : list, opcional
        Lista de colunas de notas. Se None, usa as notas padrão do ENEM.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame limpo.
    
    Exemplo
    -------
    >>> df_limpo = limpar_dados_enem(df, min_alunos_por_escola=10)
    """
    df_limpo = df.copy()
    
    # Colunas de notas padrão do ENEM
    if colunas_notas is None:
        colunas_notas = [
            'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC',
            'NU_NOTA_MT', 'NU_NOTA_REDACAO'
        ]
    
    # Filtrar apenas colunas que existem no DataFrame
    colunas_notas_existentes = [c for c in colunas_notas if c in df_limpo.columns]
    
    print(f"\nLimpeza de dados:")
    print(f"- Linhas originais: {len(df_limpo)}")
    
    # Remover linhas sem identificação de escola
    if coluna_escola in df_limpo.columns:
        df_limpo = df_limpo[df_limpo[coluna_escola].notna()]
        print(f"- Após remover sem escola: {len(df_limpo)}")
    
    # Remover notas ausentes
    for col in colunas_notas_existentes:
        if col in df_limpo.columns:
            df_limpo = df_limpo[df_limpo[col].notna()]
    
    print(f"- Após remover notas ausentes: {len(df_limpo)}")
    
    # Filtrar escolas com mínimo de alunos
    if coluna_escola in df_limpo.columns:
        # Verificar se os dados já estão agregados (têm coluna QTD_ALUNOS)
        if 'QTD_ALUNOS' in df_limpo.columns:
            # Dados já agregados - usar QTD_ALUNOS diretamente
            df_limpo = df_limpo[df_limpo['QTD_ALUNOS'] >= min_alunos_por_escola]
            print(f"- Após filtrar escolas (QTD_ALUNOS >= {min_alunos_por_escola}): {len(df_limpo)}")
        else:
            # Dados não agregados - contar ocorrências
            contagem = df_limpo[coluna_escola].value_counts()
            escolas_validas = contagem[contagem >= min_alunos_por_escola].index
            df_limpo = df_limpo[df_limpo[coluna_escola].isin(escolas_validas)]
            print(f"- Após filtrar escolas (>= {min_alunos_por_escola} alunos): {len(df_limpo)}")
            print(f"- Escolas restantes: {len(escolas_validas)}")
    
    return df_limpo.reset_index(drop=True)


def agregar_por_escola(
    df: pd.DataFrame,
    coluna_escola: str = 'CO_ESCOLA',
    colunas_notas: Optional[List[str]] = None,
    colunas_categoricas: Optional[List[str]] = None,
    colunas_numericas: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Agrega dados do ENEM por escola calculando médias e modas.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame limpo com dados do ENEM.
    coluna_escola : str, padrão='CO_ESCOLA'
        Nome da coluna que identifica a escola.
    colunas_notas : list, opcional
        Lista de colunas de notas para calcular média.
    colunas_categoricas : list, opcional
        Lista de colunas categóricas para calcular moda.
    colunas_numericas : list, opcional
        Lista de colunas numéricas adicionais para calcular média.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame agregado por escola.
    
    Exemplo
    -------
    >>> df_escolas = agregar_por_escola(df_limpo)
    """
    # Colunas padrão
    if colunas_notas is None:
        colunas_notas = [
            'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC',
            'NU_NOTA_MT', 'NU_NOTA_REDACAO'
        ]
    
    if colunas_categoricas is None:
        colunas_categoricas = ['TP_DEPENDENCIA_ADM_ESC', 'CO_UF_ESC', 'TP_LOCALIZACAO_ESC']
    
    # Filtrar apenas colunas existentes
    colunas_notas = [c for c in colunas_notas if c in df.columns]
    colunas_categoricas = [c for c in colunas_categoricas if c in df.columns]
    
    if colunas_numericas:
        colunas_numericas = [c for c in colunas_numericas if c in df.columns]
    else:
        colunas_numericas = []
    
    print(f"\nAgregando por escola:")
    print(f"- Coluna escola: {coluna_escola}")
    print(f"- Colunas de notas: {colunas_notas}")
    print(f"- Colunas categóricas: {colunas_categoricas}")
    print(f"- Colunas numéricas adicionais: {colunas_numericas}")
    
    agregacoes = {}
    
    # Agregar notas (média)
    for col in colunas_notas:
        agregacoes[col] = 'mean'
    
    # Agregar numéricas adicionais (média)
    for col in colunas_numericas:
        agregacoes[col] = 'mean'
    
    # Agregar categóricas (moda - valor mais frequente)
    for col in colunas_categoricas:
        agregacoes[col] = lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0]
    
    # Agrupar primeiro
    df_agregado = df.groupby(coluna_escola).agg(agregacoes).reset_index()
    
    # Calcular quantidade de alunos (count de qualquer coluna)
    df_agregado['QTD_ALUNOS'] = df.groupby(coluna_escola).size().values
    
    # Renomear colunas - verificar se é MultiIndex (quando usa lambda)
    print(f"- Colunas apos agg (antes de renomear): {df_agregado.columns.tolist()}")
    
    if isinstance(df_agregado.columns, pd.MultiIndex):
        # Flatten multi-index columns
        df_agregado.columns = [col[0] if col[1] == '' or col[1] == '<lambda>' else f"{col[0]}_{col[1]}" 
                               for col in df_agregado.columns.values]
    # Se houver colunas categóricas, renomear as que têm '<lambda>' no nome
    for col in colunas_categoricas:
        if f"{col}_<lambda>" in df_agregado.columns:
            df_agregado.rename(columns={f"{col}_<lambda>": col}, inplace=True)
    
    print(f"- Colunas finais: {df_agregado.columns.tolist()}")
    print(f"- Escolas agregadas: {len(df_agregado)}")
    
    return df_agregado


def preparar_features_clustering(
    df: pd.DataFrame,
    colunas_features: List[str],
    colunas_categoricas: Optional[List[str]] = None,
    normalizar: bool = True,
    scaler: Optional[StandardScaler] = None
) -> Tuple[np.ndarray, StandardScaler, pd.DataFrame]:
    """
    Prepara features para clustering com encoding e normalização.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com dados agregados por escola.
    colunas_features : list
        Lista de colunas a serem usadas como features.
    colunas_categoricas : list, opcional
        Lista de colunas categóricas para label encoding.
    normalizar : bool, padrão=True
        Se True, aplica StandardScaler nas features.
    scaler : StandardScaler, opcional
        Scaler pré-treinado para reutilização.
    
    Retorna
    -------
    tuple
        - X (np.ndarray): Features preparadas
        - scaler (StandardScaler): Scaler treinado
        - df_features (pd.DataFrame): DataFrame com features processadas
    
    Exemplo
    -------
    >>> X, scaler, df_feat = preparar_features_clustering(df, colunas_features)
    """
    df_features = df.copy()
    
    # Filtrar apenas colunas existentes
    colunas_features = [c for c in colunas_features if c in df_features.columns]
    
    print(f"\nPreparando features:")
    print(f"- Features selecionadas: {colunas_features}")
    
    # Label encoding para categóricas
    if colunas_categoricas:
        colunas_categoricas = [c for c in colunas_categoricas if c in df_features.columns]
        print(f"- Colunas categóricas: {colunas_categoricas}")
        
        for col in colunas_categoricas:
            le = LabelEncoder()
            df_features[f'{col}_ENCODED'] = le.fit_transform(df_features[col].astype(str))
            # Substituir na lista de features
            if col in colunas_features:
                idx = colunas_features.index(col)
                colunas_features[idx] = f'{col}_ENCODED'
    
    # Selecionar features
    X = df_features[colunas_features].values
    
    # Tratar NaN
    if np.isnan(X).any():
        print(f"- Tratando {np.isnan(X).sum()} valores NaN")
        X = np.nan_to_num(X, nan=np.nanmean(X, axis=0))
    
    # Normalização
    if normalizar:
        if scaler is None:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            print("- Normalização aplicada (fit_transform)")
        else:
            X_scaled = scaler.transform(X)
            print("- Normalização aplicada (transform)")
        X = X_scaled
    else:
        scaler = None
    
    print(f"- Shape final: {X.shape}")
    
    return X, scaler, df_features


def criar_features_adicionais(
    df: pd.DataFrame,
    colunas_notas: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Cria features adicionais derivadas das notas do ENEM.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com dados agregados.
    colunas_notas : list, opcional
        Lista de colunas de notas.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame com features adicionais.
    
    Exemplo
    -------
    >>> df_enriquecido = criar_features_adicionais(df_escolas)
    """
    df_novo = df.copy()
    
    print(f"\nCriando features adicionais:")
    print(f"- Colunas de entrada: {df_novo.columns.tolist()}")
    
    if colunas_notas is None:
        colunas_notas = [
            'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC',
            'NU_NOTA_MT', 'NU_NOTA_REDACAO'
        ]
    
    # Filtrar colunas existentes
    colunas_notas = [c for c in colunas_notas if c in df_novo.columns]
    
    print(f"- Colunas de notas encontradas: {colunas_notas}")
    
    # Média geral das notas
    if len(colunas_notas) > 0:
        df_novo['MEDIA_GERAL'] = df_novo[colunas_notas].mean(axis=1)
        print("- MEDIA_GERAL criada")
    
    # Desvio padrão das notas (variabilidade)
    if len(colunas_notas) > 1:
        df_novo['STD_NOTAS'] = df_novo[colunas_notas].std(axis=1)
        print("- STD_NOTAS criada")
    
    # Nota máxima e mínima
    if len(colunas_notas) > 0:
        df_novo['NOTA_MAX'] = df_novo[colunas_notas].max(axis=1)
        df_novo['NOTA_MIN'] = df_novo[colunas_notas].min(axis=1)
        print("- NOTA_MAX e NOTA_MIN criadas")
    
    # Diferença entre notas de exatas e humanas
    if 'NU_NOTA_MT' in df_novo.columns and 'NU_NOTA_LC' in df_novo.columns:
        df_novo['DIF_MT_LC'] = df_novo['NU_NOTA_MT'] - df_novo['NU_NOTA_LC']
        print("- DIF_MT_LC criada")
    
    if 'NU_NOTA_CN' in df_novo.columns and 'NU_NOTA_CH' in df_novo.columns:
        df_novo['DIF_CN_CH'] = df_novo['NU_NOTA_CN'] - df_novo['NU_NOTA_CH']
        print("- DIF_CN_CH criada")
    
    # Performance por área (percentil)
    for col in colunas_notas:
        df_novo[f'PCT_{col}'] = df_novo[col].rank(pct=True)
        print(f"- PCT_{col} criada")
    
    print(f"- Colunas de saída: {df_novo.columns.tolist()}")
    
    return df_novo


def pipeline_preparacao(
    caminho_arquivo: str,
    amostra: Optional[float] = None,
    min_alunos: int = 10,
    criar_features: bool = True,
    normalizar: bool = True
) -> Tuple[np.ndarray, pd.DataFrame, StandardScaler]:
    """
    Pipeline completo de preparação de dados do ENEM.
    
    Parâmetros
    ----------
    caminho_arquivo : str
        Caminho para o arquivo CSV.
    amostra : float, opcional
        Fração dos dados para amostragem.
    min_alunos : int, padrão=10
        Mínimo de alunos por escola.
    criar_features : bool, padrão=True
        Se True, cria features adicionais.
    normalizar : bool, padrão=True
        Se True, normaliza as features.
    
    Retorna
    -------
    tuple
        - X (np.ndarray): Features preparadas para clustering
        - df (pd.DataFrame): DataFrame processado
        - scaler (StandardScaler): Scaler treinado
    
    Exemplo
    -------
    >>> X, df, scaler = pipeline_preparacao('dados_enem.csv', amostra=0.1)
    """
    print("="*60)
    print("PIPELINE DE PREPARAÇÃO DE DADOS ENEM")
    print("="*60)
    
    # 1. Carregar dados
    df = carregar_dados_enem(caminho_arquivo, amostra=amostra)
    
    # 2. Limpar dados
    df = limpar_dados_enem(df, min_alunos_por_escola=min_alunos)
    
    # 3. Agregar por escola
    df = agregar_por_escola(df)
    
    # 4. Criar features adicionais
    if criar_features:
        df = criar_features_adicionais(df)
    
    # 5. Preparar features para clustering
    colunas_features = [
        'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC',
        'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_GERAL'
    ]
    colunas_categoricas = ['TP_DEPENDENCIA_ADM_ESCOLA']
    
    # Adicionar features extras se existirem
    for col in ['STD_NOTAS', 'DIF_MT_LC', 'DIF_CN_CH']:
        if col in df.columns:
            colunas_features.append(col)
    
    X, scaler, df = preparar_features_clustering(
        df, colunas_features, colunas_categoricas, normalizar
    )
    
    print("\n" + "="*60)
    print("PIPELINE CONCLUÍDO")
    print("="*60)
    
    return X, df, scaler
