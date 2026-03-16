import pandas as pd
import plotly.express as px
import os

print("-" * 50)
print("GERANDO RELATÓRIO PROFISSIONAL - JOSÉ LUIZ VIEIRA")
print("-" * 50)

try:
    # 1. CARREGAMENTO
    csv_file = 'samsung_global_sales_dataset.csv'
    if not os.path.exists(csv_file):
        print(f"ERRO: Arquivo {csv_file} não encontrado.")
        exit()

    df = pd.read_csv(csv_file)
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    # Limpeza para análise estatística
    df_corr = df.dropna(subset=['customer_rating', 'discount_pct', 'unit_price_usd'])

    # 2. GRÁFICOS DE DESEMPENHO (Cores ajustadas)
    print(">>> Criando visualizações principais...")
    fig_region = px.pie(df, values='revenue_usd', names='region', hole=0.4, 
                        title='Participação de Mercado por Região', 
                        color_discrete_sequence=px.colors.qualitative.Prism)

    revenue_cat = df.groupby('category')['revenue_usd'].sum().reset_index().sort_values(by='revenue_usd', ascending=False)
    fig_category = px.bar(revenue_cat, x='category', y='revenue_usd', 
                          title='Faturamento Total por Categoria', 
                          labels={'revenue_usd': 'Receita (USD)', 'category': 'Categoria'},
                          color='revenue_usd', color_continuous_scale='Blues')

    # 3. ANÁLISE ESTATÍSTICA (Ajuste visual para não ficar "feio")
    print(">>> Analisando correlações estatísticas...")
    
    # Gráfico de Dispersão: Desconto vs Nota (Agrupado por média para limpar o visual)
    df_grouped_rating = df_corr.groupby('discount_pct')['customer_rating'].mean().reset_index()
    fig_corr_discount = px.scatter(df_grouped_rating, x='discount_pct', y='customer_rating', 
                                  trendline="ols", title="Impacto do Desconto na Satisfação (Média)",
                                  labels={'discount_pct': 'Faixa de Desconto (%)', 'customer_rating': 'Nota Média'},
                                  color_discrete_sequence=['#034EA2'])

    # Gráfico de Preço vs Volume (Usando Densidade/Hexbin para limpar o visual)
    fig_corr_price = px.density_heatmap(df_corr, x='unit_price_usd', y='units_sold', 
                                       title="Densidade de Vendas: Preço vs. Quantidade",
                                       labels={'unit_price_usd': 'Preço (USD)', 'units_sold': 'Qtd Vendida'},
                                       nbinsx=30, nbinsy=10, color_continuous_scale='Viridis')

    # 4. MÉTRICAS
    receita_total = df['revenue_usd'].sum()
    unidades_totais = df['units_sold'].sum()
    ticket_medio = receita_total / unidades_totais
    correlacao_valor = df_corr['discount_pct'].corr(df_corr['customer_rating'])

    # 5. ESTRUTURA DO RELATÓRIO HTML (Agora 100% em Português)
    print(">>> Finalizando o layout em Português...")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Ciência de Dados - Caso Samsung</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; background-color: #f4f7f6; color: #333; }}
            .header {{ background-color: #034EA2; color: white; padding: 40px; text-align: center; }}
            .container {{ max-width: 1000px; margin: 20px auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .aviso-legal {{ background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; font-style: italic; }}
            .section-title {{ border-left: 6px solid #034EA2; padding-left: 15px; margin-top: 40px; color: #034EA2; font-size: 1.5em; }}
            .metric-container {{ display: flex; justify-content: space-between; margin: 25px 0; gap: 20px; }}
            .metric-card {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; flex: 1; text-align: center; border-radius: 10px; }}
            .metric-card h3 {{ margin: 0; font-size: 0.85em; color: #666; text-transform: uppercase; }}
            .metric-card p {{ margin: 10px 0 0; font-size: 1.4em; font-weight: bold; color: #034EA2; }}
            .insight-box {{ background: #eef2f7; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #2ecc71; line-height: 1.5; }}
            .graph-wrapper {{ margin: 40px 0; text-align: center; }}
            footer {{ text-align: center; margin-top: 60px; padding: 40px; border-top: 1px solid #eee; background: #fff; color: #888; }}
            .footer-name {{ font-weight: bold; color: #333; font-size: 1.2em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Análise Avançada de Dados: Estudo Global Samsung</h1>
        </div>

        <div class="container">
            <div class="aviso-legal">
                <strong>Nota Importante:</strong> Esta análise possui caráter estritamente <strong>didático e fictício</strong>. 
                Os dados aqui apresentados não são informações reais da empresa. Este projeto demonstra competência técnica 
                em Python, estatística e Business Intelligence.
            </div>

            <h2 class="section-title">1. Resumo de Performance</h2>
            <div class="metric-container">
                <div class="metric-card"><h3>Faturamento Total</h3><p>USD {receita_total:,.2f}</p></div>
                <div class="metric-card"><h3>Ticket Médio</h3><p>USD {ticket_medio:,.2f}</p></div>
                <div class="metric-card"><h3>Força da Correlação</h3><p>{correlacao_valor:.4f}</p></div>
            </div>

            <div class="insight-box">
                <strong>Insight Técnico:</strong> A correlação calculada indica a sensibilidade do cliente ao preço. 
                Gráficos de densidade foram aplicados para evitar a sobreposição de dados e permitir uma leitura clara 
                dos volumes de venda por faixa de preço.
            </div>

            <div class="graph-wrapper">
                {fig_region.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="graph-wrapper">
                {fig_category.to_html(full_html=False, include_plotlyjs=False)}
            </div>

            <h2 class="section-title">2. Ciência de Dados e Comportamento</h2>
            <p>Abaixo, analisamos se a estratégia de descontos afeta a percepção de valor do cliente e como o volume se comporta em diferentes níveis de preço.</p>
            
            <div class="graph-wrapper">
                {fig_corr_discount.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="graph-wrapper">
                {fig_corr_price.to_html(full_html=False, include_plotlyjs=False)}
            </div>

            <footer>
                <p>Relatório de Performance Comercial - Projeto de Portfólio</p>
                <p class="footer-name">José Luiz Vieira - Analista de Dados</p>
                <p>Especialista em Business Intelligence & Automação</p>
                <p>© {pd.Timestamp.now().year}</p>
            </footer>
        </div>
    </body>
    </html>
    """

    with open('analise_samsung.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("-" * 50)
    print("SUCESSO! O relatório em português foi gerado.")
    print("-" * 50)

except Exception as e:
    print(f"ERRO: {e}")