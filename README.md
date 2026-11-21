# 🦠 Análise Exploratória e POO aplicadas a dados de COVID-19

> Painel interativo com as decisões da **CONITEC** sobre tecnologias e diretrizes para tratamento e prevenção da Covid-19, desenvolvido em Python com Programação Orientada a Objetos.

**Tema:** Ciência & Tecnologia
**Disciplina:** Programação Orientada a Objetos – Ciência de Dados e Inteligência Artificial

---

## 🎯 Objetivo

Converter as tabelas brutas dos registros da CONITEC em **gráficos analíticos e interativos**.

## ❓ Pergunta central

**Como a POO torna esses registros fáceis de explorar, comparar e interpretar?**

## 🔎 Perguntas da análise

1. Qual foi a decisão mais frequente do Ministério da Saúde?
2. Qual a comparação entre a análise inicial e a análise final da CONITEC?
3. Em que época houve mais demandas?
4. Quem fez mais demandas?
5. Qual o intervalo entre a demanda e a publicação?

## 📊 Fonte de dados

Dados públicos: **Tecnologias e Diretrizes para tratamento e prevenção da Covid-19** (CONITEC / Ministério da Saúde).

🔗 *[https://dadosabertos.saude.gov.br/dataset/tecnologias-e-diretrizes-para-tratamento-e-prevencao-da-covid-19]*

## 🧱 Arquitetura orientada a objetos

| Classe | Responsabilidade |
|---|---|
| `FonteDados` / `FonteCSV` / `FonteXLS` | Carregar os dados brutos |
| `TratadorDados` | Limpeza e filtros genéricos |
| `AnalisadorDados` | Regras específicas da CONITEC e cálculo dos indicadores |
| `Indicador` | Representa um KPI com formatação no padrão brasileiro |
| `Visualizador` | Geração dos gráficos interativos |
| `Dashboard` | Organiza KPIs, gráficos e tabela no painel |

```
Fonte (CSV/XLS) ──► TratadorDados ──► AnalisadorDados ──► Visualizador / Dashboard
```

## ▶️ Como executar

```bash
pip install -r requirements.txt
```

1. Abra o notebook `sistema_de_analise.ipynb` no Google Colab.
2. Execute as células em ordem.
3. Envie a planilha da CONITEC (`.xlsx`, `.xls` ou `.csv`) quando solicitado.
4. Use o filtro de decisão para explorar o painel.

## ✅ Testes

Os testes automatizados cobrem todas as classes e o fluxo completo do sistema.

```bash
python -m pytest test_projeto_poo.py -v
```

## 👥 Equipe

*Arthur Catto Ribeiro, Catherine Luisa Bueno de Oliveira, Gabriel Bustamante, 
Tales Dias Akutagawa, Tomas Gonçalves Arslan*
