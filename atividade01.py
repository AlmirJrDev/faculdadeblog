import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar


def obter_cotacao_dolar_mensal(mm_yyyy: str):
    
    
    try:
    
        first_date = datetime.strptime("072016", "%m%Y")
        dia_inicial = 1
        dia_final = calendar.monthrange(first_date.year, first_date.month)[1]

        data_inicial = f"{first_date.month:02d}-{dia_inicial:02d}-{first_date.year}"
        data_final = f"{first_date.month:02d}-{dia_final:02d}-{first_date.year}"
        
        url_base = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        url_completa = (
            f"{url_base}CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
            f"@dataInicial='{data_inicial}'&@dataFinalCotacao='{data_final}'&$format=json"
        )
        



        response = requests.get(url_completa)
        response.raise_for_status()
        data = response.json()

        if not data.get('value'):
            return f"Não foram encontradas cotações para o período {mm_yyyy}."


        df_api = pd.DataFrame(data['value'])
        df_api['dataHoraCotacao'] = pd.to_datetime(df_api['dataHoraCotacao'])
        df_api['Data'] = df_api['dataHoraCotacao'].dt.date
        df_api = df_api[['Data', 'cotacaoVenda']].sort_values('Data')
        
        print(f"✓ {len(df_api)} cotações obtidas da API")
        print(f"  Período: {df_api['Data'].min()} a {df_api['Data'].max()}\n")

   
        start_date = datetime(first_date.year, first_date.month, dia_inicial).date()
        end_date = datetime(first_date.year, first_date.month, dia_final).date()
        
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D').date
        df_completo = pd.DataFrame({'Data': all_dates})
        

        df_completo = df_completo.merge(df_api, on='Data', how='left')
        

        df_completo['cotacaoVenda'] = df_completo['cotacaoVenda'].fillna(method='ffill')
        

        df_completo = df_completo.rename(columns={'cotacaoVenda': 'Cotação de Venda (R$)'})
        

        dias_preenchidos = df_completo['Cotação de Venda (R$)'].notna().sum() - len(df_api)
        if dias_preenchidos > 0:
            print(f"✓ {dias_preenchidos} dias sem cotação preenchidos com valores anteriores")

        mes_nome = first_date.strftime("%B").capitalize()
        ano = first_date.year
        
        fig = px.line(
            df_completo, 
            x='Data', 
            y='Cotação de Venda (R$)', 
            title=f'Cotação de Venda do Dólar (PTAX) - {mes_nome}/{ano}',
            labels={'Data': 'Data', 'Cotação de Venda (R$)': 'Cotação (R$)'},
            markers=True
        )
        

        fig.update_layout(
            hovermode='x unified',
            xaxis_title='Data',
            yaxis_title='Cotação (R$)',
            template='plotly_white',
            font=dict(size=12),
            title_font=dict(size=16, family='Arial, sans-serif'),
            showlegend=False,
            height=500
        )
        
        fig.update_traces(
            line=dict(color='#0066cc', width=2),
            marker=dict(size=4)
        )
        

        output_path = f"atividade1_cotacao_dolar_{mm_yyyy}.html"
        fig.write_html(output_path, include_plotlyjs='cdn')
        
        print(f"\n✓ Gráfico salvo em: {output_path}")
        print(f"  Abra o arquivo no navegador para visualizar o gráfico interativo!")
        
        return f"Gráfico gerado com sucesso: {output_path}"

    except requests.exceptions.RequestException as e:
        return f"Erro: Falha ao acessar a API do BCB. {e}"
    except Exception as e:
        return f"Ocorreu um erro: {e}"



if __name__ == "__main__":
    print("=" * 70)
    print("ATIVIDADE 1 - COTAÇÃO DO DÓLAR POR PERÍODO")
    print("=" * 70)
    print()

    mes_ano = "072016"
    
    if len(mes_ano) != 6 or not mes_ano.isdigit():
        print("\n❌ Formato inválido! Use MMYYYY (ex: 082021)")
    else:
        print()
        resultado = obter_cotacao_dolar_mensal(mes_ano)
    
    print("\n" + "=" * 70)
    input("\nPressione ENTER para fechar...")