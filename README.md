# 📊 Desempenho das Vendas no E-commerce Brasileiro

## Análise e Visualização de Dados

Projeto acadêmico desenvolvido para a disciplina de **Análise e Visualização de Dados**, com o objetivo de realizar a extração, tratamento, transformação e organização de dados públicos de comércio eletrônico brasileiro utilizando um modelo dimensional em **Esquema Estrela**.

---

## 👨‍🏫 Informações Acadêmicas

**Disciplina:** Análise e Visualização de Dados  
**Professor:** Davi Maia  
**Turma:** 4º Período | Noite

### 👥 Equipe

- Arthur Barreto
- Gustavo Scalise
- Filipe Gonçalves
- Marcos Bino

---

## 🎯 Objetivo

Analisar e estruturar dados públicos de comércio eletrônico brasileiro, permitindo a organização das informações de vendas em um modelo dimensional adequado para análises e futuras visualizações no Power BI.

O projeto contempla a construção de um processo **ETL (Extract, Transform, Load)** utilizando Python e Pandas, gerando as dimensões e a tabela fato que compõem o esquema estrela.

---

## 📂 Fonte dos Dados

Os dados utilizados são provenientes do conjunto de dados **Brazilian E-Commerce Public Dataset by Olist**, disponibilizado publicamente no Kaggle.

Foram utilizadas as seguintes bases:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_products_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_sellers_dataset.csv`

---

## ⭐ Modelo Dimensional — Esquema Estrela

O projeto utiliza um **Esquema Estrela**, composto por uma tabela fato central e quatro tabelas dimensão.

### Tabela Fato

**F_Vendas**

Contém os registros relacionados às vendas e seus valores financeiros.

### Tabelas Dimensão

- **D_Cliente** — informações dos clientes
- **D_Produto** — informações dos produtos
- **D_Vendedor** — informações dos vendedores
- **D_Tempo** — informações relacionadas às datas

Estrutura:

```text
                    D_Cliente
                        |
                        |
D_Produto -------- F_Vendas -------- D_Vendedor
                        |
                        |
                     D_Tempo