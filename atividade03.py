import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def calcular_regressao_linear(arquivo_x='X.txt', arquivo_y='y.txt'):

    try:

        X_data = np.loadtxt(arquivo_x)
        y_data = np.loadtxt(arquivo_y)
        
        print(f"Dados carregados: {len(X_data)} observações")
        print(f"X varia de {X_data.min():.2f} a {X_data.max():.2f}")
        print(f"y varia de {y_data.min():.2f} a {y_data.max():.2f}")
        
       
        X_matriz = np.vstack([np.ones(len(X_data)), X_data]).T
        


        beta = np.linalg.inv(X_matriz.T @ X_matriz) @ X_matriz.T @ y_data
        a, b = beta[0], beta[1] 
        
        print(f"\nCoeficientes calculados:")
        print(f"  Intercepto (a): {a:.4f}")
        print(f"  Coeficiente Angular (b): {b:.4f}")
        print(f"  Equação: y = {a:.4f} + {b:.4f} * x")
        
  
        y_pred = a + b * X_data
        

        ss_res = np.sum((y_data - y_pred) ** 2)  
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2) 
        r_squared = 1 - (ss_res / ss_tot)
        print(f"  R²: {r_squared:.4f}")
        

        fig = go.Figure()
        

        fig.add_trace(go.Scatter(
            x=X_data,
            y=y_data,
            mode='markers',
            name='Dados Observados',
            marker=dict(color='blue', size=5, opacity=0.6)
        ))
        
        fig.add_trace(go.Scatter(
            x=X_data,
            y=y_pred,
            mode='lines',
            name=f'Regressão Linear (R²={r_squared:.3f})',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title='Regressão Linear: Anos de Estudo vs. Salário',
            xaxis_title='Anos de Estudo (X)',
            yaxis_title='Salário (y)',
            hovermode='closest',
            template='plotly_white',
            showlegend=True
        )
        

        output_path = "regressao_linear.html"
        fig.write_html(output_path, include_plotlyjs='cdn')
        
        return f"Gráfico  gerado com sucesso: {output_path}"
        
    except FileNotFoundError as e:
        return f"Erro: Arquivo não encontrado - {e}"
    except Exception as e:
        return f"Erro ao tentar relizar ação: {e}"

if __name__ == "__main__":
    print("=" * 70)
    print("=" * 70)

 
  
    print("\n--- Regressão Linear ---")
    resultado_3 = calcular_regressao_linear('X.txt', 'y.txt')
    print(resultado_3)
    
    print("\n" + "=" * 70)
    print("EXECUÇÃO CONCLUÍDA!")
    print("=" * 70)