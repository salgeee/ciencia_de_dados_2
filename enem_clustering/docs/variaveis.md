# Dicionário de Variáveis - ENEM 2024

## Variáveis de Identificação

| Código | Descrição | Tipo |
|--------|-----------|------|
| NU_INSCRICAO | Número de inscrição do participante | String |
| NU_ANO | Ano do ENEM | Inteiro |
| CO_MUNICIPIO_ESC | Código do município da escola | Inteiro |
| CO_UF_ESC | Código da UF da escola | Inteiro |
| SG_UF_ESC | Sigla da UF da escola | String |
| TP_DEPENDENCIA_ADM_ESC | Dependência administrativa da escola | Inteiro |
| TP_LOCALIZACAO_ESC | Localização da escola | Inteiro |

## Variáveis de Desempenho

| Código | Descrição | Tipo | Range |
|--------|-----------|------|-------|
| NU_NOTA_CN | Nota da prova de Ciências da Natureza | Float | 0-1000 |
| NU_NOTA_CH | Nota da prova de Ciências Humanas | Float | 0-1000 |
| NU_NOTA_LC | Nota da prova de Linguagens e Códigos | Float | 0-1000 |
| NU_NOTA_MT | Nota da prova de Matemática | Float | 0-1000 |
| NU_NOTA_REDACAO | Nota da redação | Float | 0-1000 |

## Variáveis Socioeconômicas (Questionário)

| Código | Descrição | Tipo |
|--------|-----------|------|
| Q002 | Até que série seu pai, ou o homem responsável por você, estudou? | String (A-H) |
| Q006 | Qual é a renda mensal da sua família? | String (A-Q) |
| Q010 | Na sua residência tem computador? | String (A-E) |
| Q022 | Na sua residência tem telefone celular? | String (A-D) |
| Q024 | Na sua residência tem acesso à Internet? | String (A-B) |
| Q025 | Você tem quarto para dormir? | String (A-B) |

### Mapeamento Q002 (Escolaridade do Pai)

| Código | Descrição |
|--------|-----------|
| A | Nunca estudou |
| B | Não completou a 4ª série/5º ano |
| C | Completou a 4ª série/5º ano |
| D | Completou a 8ª série/9º ano |
| E | Completou o Ensino Médio |
| F | Completou a Faculdade |
| G | Completou a Pós-graduação |
| H | Não sei |

### Mapeamento Q006 (Renda Familiar)

| Código | Faixa de Renda |
|--------|----------------|
| A | Nenhuma renda |
| B | Até R$ 1.212,00 |
| C | R$ 1.212,01 - R$ 1.818,00 |
| D | R$ 1.818,01 - R$ 2.424,00 |
| E | R$ 2.424,01 - R$ 3.030,00 |
| F | R$ 3.030,01 - R$ 3.636,00 |
| G | R$ 3.636,01 - R$ 4.848,00 |
| H | R$ 4.848,01 - R$ 6.060,00 |
| I | R$ 6.060,01 - R$ 7.272,00 |
| J | R$ 7.272,01 - R$ 8.484,00 |
| K | R$ 8.484,01 - R$ 9.696,00 |
| L | R$ 9.696,01 - R$ 10.908,00 |
| M | R$ 10.908,01 - R$ 12.120,00 |
| N | R$ 12.120,01 - R$ 14.544,00 |
| O | R$ 14.544,01 - R$ 18.180,00 |
| P | R$ 18.180,01 - R$ 24.240,00 |
| Q | Acima de R$ 24.240,00 |

## Variáveis de Contexto

| Código | Descrição | Valores |
|--------|-----------|---------|
| TP_DEPENDENCIA_ADM_ESC | Dependência administrativa | 1=Federal, 2=Estadual, 3=Municipal, 4=Privada |
| TP_LOCALIZACAO_ESC | Localização | 1=Urbana, 2=Rural |
| TP_PRESENCA_CN | Presença Ciências da Natureza | 0=Faltou, 1=Presente, 2=Eliminado |
| TP_PRESENCA_CH | Presença Ciências Humanas | 0=Faltou, 1=Presente, 2=Eliminado |
| TP_PRESENCA_LC | Presença Linguagens | 0=Faltou, 1=Presente, 2=Eliminado |
| TP_PRESENCA_MT | Presença Matemática | 0=Faltou, 1=Presente, 2=Eliminado |
| TP_STATUS_REDACAO | Status da redação | 1=Sem problemas, 2-9=Diferentes anulações |

## Features Criadas (Engenharia)

| Feature | Descrição | Cálculo |
|---------|-----------|---------|
| MEDIA_GERAL | Média das 5 notas | (CN+CH+LC+MT+REDACAO)/5 |
| DESVIO_PADRAO_NOTAS | Consistência do desempenho | std([CN,CH,LC,MT,REDACAO]) |
| RANGE_NOTAS | Diferença entre maior e menor nota | max - min |
| TAMANHO_ESCOLA | Categoria do tamanho | Pequena<50, Média 50-200, Grande>200 |
| CATEGORIA_DESEMPENHO | Performance geral | Baixo<400, Médio 400-600, Alto>600 |

## Transformações Aplicadas

### Encoding
- **One-Hot:** CO_UF_ESC, TP_DEPENDENCIA_ADM_ESC, TP_LOCALIZACAO_ESC
- **Label:** Variáveis Q (questões socioeconômicas)

### Normalização
- **StandardScaler:** Todas as features numéricas (média=0, desvio=1)

### Agregação por Escola
Os dados são agregados por escola calculando:
- Média das notas dos alunos
- Média da renda (Q006 convertida para valor numérico)
- Contagem de alunos
- Moda das categorias categóricas
