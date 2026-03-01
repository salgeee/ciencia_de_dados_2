"""
Gerador de PDF do Relatório Técnico usando ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from pathlib import Path

print("="*60)
print("GERANDO PDF DO RELATÓRIO TÉCNICO")
print("="*60)

# Carregar dados
df = pd.read_csv('enem_clustering/data/processed/escolas_com_clusters.csv')
df_30 = pd.read_csv('enem_clustering/data/processed/escolas_com_clusters_30pct.csv')

# Criar documento
doc = SimpleDocTemplate(
    "enem_clustering/relatorio/Relatorio_Tecnico_ENEM_Clustering.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Estilos
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=20,
    alignment=TA_CENTER,
    borderColor=colors.HexColor('#3498db'),
    borderWidth=2,
    borderPadding=10
)

style_heading1 = ParagraphStyle(
    'CustomH1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=12,
    borderColor=colors.HexColor('#3498db'),
    borderWidth=1,
    borderPadding=5
)

style_heading2 = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#34495e'),
    spaceAfter=10
)

style_heading3 = ParagraphStyle(
    'CustomH3',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=colors.HexColor('#7f8c8d'),
    spaceAfter=8
)

style_normal = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

style_bullet = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=10,
    leftIndent=20,
    spaceAfter=6
)

# Conteúdo
story = []

# TÍTULO
story.append(Paragraph("Relatório Técnico", style_title))
story.append(Paragraph("Análise de Clustering do Desempenho Escolar no ENEM 2024", styles['Heading2']))
story.append(Spacer(1, 0.5*cm))

# Metadados
meta_text = f"""
<b>Autores:</b> Leonardo Ferreira Salge 12311BSI307<br/>
<b></b> Vinícius Ferreira Salge 12311BSI308<br/>
<b></b> Daniel Solis Salge 12311BSI305<br/>
<b></b> Guilherme Gomes Alves 12311BSI306 <br/>
<b>Data:</b> Março/2026<br/>
<b>Base de Dados:</b> Microdados ENEM 2024 (INEP)<br/>
<b>Volume Analisado:</b> {len(df):,} escolas (100% dos dados válidos)
"""
story.append(Paragraph(meta_text, styles['Normal']))
story.append(Spacer(1, 1*cm))

# 1. INTRODUÇÃO
story.append(Paragraph("1. Introdução", style_heading1))

story.append(Paragraph("1.1 Contexto", style_heading2))
story.append(Paragraph(
    "O Exame Nacional do Ensino Médio (ENEM) é o principal instrumento de avaliação "
    "da educação brasileira, utilizado para acesso ao ensino superior e indicador "
    "de qualidade educacional. Este estudo aplica técnicas de <b>clustering não-supervisionado</b> "
    "para identificar padrões naturais de desempenho entre escolas brasileiras.",
    style_normal
))

story.append(Paragraph("1.2 Objetivos", style_heading2))
story.append(Paragraph("<b>Objetivo Geral:</b> Identificar grupos de escolas com perfis de desempenho similares no ENEM 2024", style_normal))
story.append(Paragraph("<b>Objetivos Específicos:</b>", style_normal))
story.append(Paragraph("1. Verificar se existem 'tipos' distintos de escolas baseados no desempenho", style_bullet))
story.append(Paragraph("2. Analisar o agrupamento de escolas públicas estaduais", style_bullet))
story.append(Paragraph("3. Identificar fatores associados ao alto desempenho escolar", style_bullet))

story.append(Paragraph("1.3 Perguntas de Pesquisa", style_heading2))
story.append(Paragraph("1. Existem tipos distintos de escolas no Brasil baseados no desempenho no ENEM?", style_bullet))
story.append(Paragraph("2. As escolas públicas estaduais se agrupam em um cluster específico?", style_bullet))
story.append(Paragraph("3. Quais os principais fatores associados ao alto desempenho escolar?", style_bullet))

story.append(PageBreak())

# 2. DESCRIÇÃO DOS DADOS
story.append(Paragraph("2. Descrição dos Dados", style_heading1))

story.append(Paragraph("2.1 Fonte e Volume", style_heading2))

# Tabela de fonte
data_fonte = [
    ['Característica', 'Valor'],
    ['Fonte', 'Microdados ENEM 2024 (INEP)'],
    ['Total de inscritos', '4.332.944'],
    ['Escolas analisadas', f'{len(df):,}'],
    ['Critério de inclusão', 'Escolas com ≥10 alunos e notas válidas']
]

tabela_fonte = Table(data_fonte, colWidths=[6*cm, 10*cm])
tabela_fonte.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_fonte)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("2.2 Variáveis Utilizadas", style_heading2))
data_vars = [
    ['Variável', 'Descrição', 'Tipo'],
    ['NU_NOTA_CN', 'Nota Ciências da Natureza', 'Numérica'],
    ['NU_NOTA_CH', 'Nota Ciências Humanas', 'Numérica'],
    ['NU_NOTA_LC', 'Nota Linguagens e Códigos', 'Numérica'],
    ['NU_NOTA_MT', 'Nota Matemática', 'Numérica'],
    ['NU_NOTA_REDACAO', 'Nota Redação', 'Numérica'],
    ['TP_DEPENDENCIA_ADM_ESC', 'Tipo de escola (1-4)', 'Categórica'],
    ['QTD_ALUNOS', 'Quantidade de alunos por escola', 'Numérica']
]

tabela_vars = Table(data_vars, colWidths=[4*cm, 8*cm, 4*cm])
tabela_vars.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_vars)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("2.3 Estatísticas por Cluster", style_heading2))

# Calcular estatísticas
stats_data = [['Cluster', 'Total Escolas', 'Média Geral', 'Mediana', 'Desvio Padrão']]
for c in sorted(df['cluster'].unique()):
    subset = df[df['cluster'] == c]
    stats_data.append([
        f'Cluster {c}',
        f'{len(subset):,}',
        f'{subset["MEDIA_GERAL"].mean():.2f}',
        f'{subset["MEDIA_GERAL"].median():.2f}',
        f'{subset["MEDIA_GERAL"].std():.2f}'
    ])

tabela_stats = Table(stats_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 4*cm])
tabela_stats.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_stats)

story.append(PageBreak())

# 3. METODOLOGIA
story.append(Paragraph("3. Metodologia", style_heading1))

story.append(Paragraph("3.1 Pipeline de Processamento", style_heading2))
pipeline_text = """
Dados Brutos (4.3M alunos) → Limpeza → Agregação por Escola → 
Engenharia de Features → Normalização → Clustering → Validação → Interpretação
"""
story.append(Paragraph(pipeline_text, style_normal))

story.append(Paragraph("3.2 Algoritmos Testados", style_heading2))
data_alg = [
    ['Algoritmo', 'Silhouette', 'Davies-Bouldin', 'Observação'],
    ['K-Means (k=2)', '0.568', '0.652', 'Melhor resultado'],
    ['DBSCAN', '-', '-', 'Não convergiu'],
    ['Hierárquico', '0.542', '0.701', 'Segunda opção'],
    ['GMM', '0.531', '0.728', 'Inferior']
]
tabela_alg = Table(data_alg, colWidths=[4*cm, 3*cm, 3*cm, 6*cm])
tabela_alg.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#90EE90')),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_alg)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("3.3 Configuração do Modelo Selecionado", style_heading2))
story.append(Paragraph("• <b>Algoritmo:</b> K-Means", style_normal))
story.append(Paragraph("• <b>Número de clusters (k):</b> 2", style_normal))
story.append(Paragraph("• <b>Inicializações:</b> Múltiplas seeds (n=10)", style_normal))
story.append(Paragraph("• <b>Features:</b> Notas das 5 áreas + Média Geral + Qtd Alunos + Tipo Escola", style_normal))

story.append(PageBreak())

# 4. RESULTADOS
story.append(Paragraph("4. Resultados", style_heading1))

story.append(Paragraph("4.1 Composição dos Clusters", style_heading2))

# Tabela de composição
comp_data = [['Cluster', 'Tipo', 'Quantidade', 'Percentual']]
mapa_tipos = {1.0: 'Federal', 2.0: 'Estadual', 3.0: 'Municipal', 4.0: 'Privada'}

for c in sorted(df['cluster'].unique()):
    subset = df[df['cluster'] == c]
    total = len(subset)
    comp = subset['TP_DEPENDENCIA_ADM_ESC'].value_counts()
    
    for cod, nome in mapa_tipos.items():
        count = comp.get(cod, 0)
        pct = count / total * 100
        comp_data.append([f'Cluster {c}', nome, f'{count:,}', f'{pct:.1f}%'])

tabela_comp = Table(comp_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm])
tabela_comp.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_comp)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("4.2 Análise por Área do Conhecimento", style_heading2))
areas_data = [['Área', 'Cluster 0 (Baixo)', 'Cluster 1 (Alto)', 'Diferença']]
areas = [('Ciências Natureza', 'NU_NOTA_CN'), ('Ciências Humanas', 'NU_NOTA_CH'), 
         ('Linguagens', 'NU_NOTA_LC'), ('Matemática', 'NU_NOTA_MT'), ('Redação', 'NU_NOTA_REDACAO')]

for nome, col in areas:
    m0 = df[df['cluster']==0][col].mean()
    m1 = df[df['cluster']==1][col].mean()
    areas_data.append([nome, f'{m0:.1f}', f'{m1:.1f}', f'+{m1-m0:.1f}'])

tabela_areas = Table(areas_data, colWidths=[4*cm, 3.5*cm, 3.5*cm, 3*cm])
tabela_areas.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_areas)
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("4.3 Comparação: Amostra 30% vs 100%", style_heading2))
m30_c0 = df_30[df_30['cluster']==0]['MEDIA_GERAL'].mean()
m30_c1 = df_30[df_30['cluster']==1]['MEDIA_GERAL'].mean()
m100_c0 = df[df['cluster']==0]['MEDIA_GERAL'].mean()
m100_c1 = df[df['cluster']==1]['MEDIA_GERAL'].mean()

comp_30_data = [
    ['Métrica', 'Amostra 30%', 'Amostra 100%', 'Diferença'],
    ['Total escolas', f'{len(df_30):,}', f'{len(df):,}', f'+{len(df)-len(df_30):,}'],
    ['Média Cluster 0', f'{m30_c0:.2f}', f'{m100_c0:.2f}', f'{m100_c0-m30_c0:+.2f}'],
    ['Média Cluster 1', f'{m30_c1:.2f}', f'{m100_c1:.2f}', f'{m100_c1-m30_c1:+.2f}'],
    ['Estaduais no Alto (%)', '11.4%', '15.5%', '+4.1%'],
    ['Privadas no Alto (%)', '79.3%', '77.6%', '-1.7%']
]
tabela_comp30 = Table(comp_30_data, colWidths=[4*cm, 3.5*cm, 3.5*cm, 3*cm])
tabela_comp30.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(tabela_comp30)

# Adicionar figuras
story.append(Spacer(1, 1*cm))
story.append(Paragraph("4.4 Visualizações", style_heading2))

if Path('enem_clustering/relatorio/figuras/figura1_analise_geral.png').exists():
    story.append(Paragraph("Figura 1: Análise Geral dos Clusters", style_heading3))
    img = Image('enem_clustering/relatorio/figuras/figura1_analise_geral.png', width=16*cm, height=11*cm)
    story.append(img)

story.append(PageBreak())

if Path('enem_clustering/relatorio/figuras/figura2_composicao_clusters.png').exists():
    story.append(Paragraph("Figura 2: Composição dos Clusters", style_heading3))
    img2 = Image('enem_clustering/relatorio/figuras/figura2_composicao_clusters.png', width=16*cm, height=7*cm)
    story.append(img2)

story.append(PageBreak())

# 5. DISCUSSÃO
story.append(Paragraph("5. Discussão", style_heading1))

story.append(Paragraph("5.1 Respostas às Perguntas de Pesquisa", style_heading2))

story.append(Paragraph("<b>Pergunta 1: Existem tipos de escolas?</b>", style_heading3))
story.append(Paragraph(
    "SIM. O clustering identificou dois grupos distintos: <b>Cluster 0 (Baixo)</b> com 67.4% das escolas, "
    "média 497.5, predominantemente estadual (94.5%); e <b>Cluster 1 (Alto)</b> com 32.6% das escolas, "
    "média 604.3, predominantemente privada (77.6%).",
    style_normal
))

story.append(Paragraph("<b>Pergunta 2: As escolas estaduais se agrupam?</b>", style_heading3))
story.append(Paragraph(
    "SIM, fortemente no cluster de baixo desempenho: 92.6% das escolas estaduais (14.679) estão no Cluster 0, "
    "enquanto apenas 7.4% (1.165 escolas) alcançaram o Cluster 1 de alto desempenho.",
    style_normal
))

story.append(Paragraph("<b>Pergunta 3: Fatores de alto desempenho:</b>", style_heading3))
story.append(Paragraph("1. <b>Tipo de escola (Privada):</b> 77.6% das escolas de alto desempenho", style_bullet))
story.append(Paragraph("2. <b>Redação:</b> Maior gap (197 pontos)", style_bullet))
story.append(Paragraph("3. <b>Matemática:</b> Segundo maior gap (119 pontos)", style_bullet))
story.append(Paragraph("4. <b>Dependência Federal:</b> 9x mais representada no alto desempenho", style_bullet))

story.append(Paragraph("5.2 Análise Crítica", style_heading2))
story.append(Paragraph(
    "<b>Limitações:</b> Correlação não implica causalidade. A associação entre escola privada e alto desempenho "
    "não prova que a privatização causa sucesso. Variáveis socioeconômicas (renda, educação dos pais) não foram incluídas.",
    style_normal
))
story.append(Paragraph(
    "<b>Pontos Positivos:</b> 1.165 escolas estaduais demonstram que é possível excelência no setor público. "
    "A amostra de 30% foi representativa (diferenças menores que 5%).",
    style_normal
))

story.append(PageBreak())

# 6. CONCLUSÕES
story.append(Paragraph("6. Conclusões", style_heading1))

story.append(Paragraph("6.1 Principais Achados", style_heading2))
story.append(Paragraph(
    "1. <b>Dipolarização do sistema educacional:</b> Existe uma clara divisão entre escolas de baixo e alto "
    "desempenho, com forte correlação com a dependência administrativa.",
    style_normal
))
story.append(Paragraph(
    "2. <b>Desigualdade estrutural:</b> 92.6% das escolas estaduais encontram-se no cluster de baixo desempenho, "
    "indicando desafios sistêmicos no ensino público.",
    style_normal
))
story.append(Paragraph(
    "3. <b>Possibilidade de excelência pública:</b> A existência de 1.165 escolas estaduais no cluster de alto "
    "desempenho demonstra que fatores de gestão e recursos podem superar limitações estruturais.",
    style_normal
))

story.append(Paragraph("6.2 Recomendações", style_heading2))
story.append(Paragraph(
    "1. <b>Investigação aprofundada:</b> Estudar as 1.165 escolas estaduais de alto desempenho para identificar "
    "práticas replicáveis em outras escolas públicas.",
    style_normal
))
story.append(Paragraph(
    "2. <b>Políticas públicas:</b> Focar recursos em Matemática e Redação (maiores gaps identificados).",
    style_normal
))
story.append(Paragraph(
    "3. <b>Atenção às privadas de baixo desempenho:</b> 22.4% das escolas privadas também estão no cluster inferior.",
    style_normal
))

story.append(Paragraph("6.3 Contribuições do Estudo", style_heading2))
story.append(Paragraph(
    "• Demonstração da aplicabilidade de clustering em dados educacionais<br/>"
    "• Validação da representatividade de amostras (30% vs 100%)<br/>"
    "• Base empírica para formulação de políticas públicas",
    style_normal
))

story.append(Spacer(1, 2*cm))

# Referências
story.append(Paragraph("Referências", style_heading1))
story.append(Paragraph(
    "1. INEP. Microdados ENEM 2024. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira, 2024.<br/><br/>"
    "2. Hastie, T., Tibshirani, R., & Friedman, J. The Elements of Statistical Learning. Springer, 2009.<br/><br/>"
    "3. Rousseeuw, P. J. Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. "
    "Journal of Computational and Applied Mathematics, 1987.",
    style_normal
))

# Gerar PDF
doc.build(story)

print("="*60)
print("PDF GERADO COM SUCESSO!")
print("="*60)
print(f"\nArquivo: enem_clustering/relatorio/Relatorio_Tecnico_ENEM_Clustering.pdf")
print(f"Total de páginas: Aproximadamente 6 páginas")
print(f"\nConteúdo:")
print("  - Introdução")
print("  - Descrição dos Dados")
print("  - Metodologia")
print("  - Resultados (tabelas e figuras)")
print("  - Discussão")
print("  - Conclusões")
print("  - Referências")
