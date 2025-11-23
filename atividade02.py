import requests
import folium
from folium import Map, Marker, Icon
from datetime import datetime


TOKEN = "61756b035b33e703fabea8cf1bd83aaa98410962815d19aac6d351f674dca75c"

class MonitoramentoOnibus:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.base_url = "http://api.olhovivo.sptrans.com.br/v2.1"
        self.autenticar()
    
    def autenticar(self):

        url = f"{self.base_url}/Login/Autenticar?token={self.token}"
        response = self.session.post(url)
        if response.text == "true":
            print("✓ Autenticação realizada com sucesso!")
        else:
            print("✗ Falha na autenticação")
            raise Exception("Erro ao autenticar na API")
    
    def buscar_linhas(self, termo_busca):

        url = f"{self.base_url}/Linha/Buscar?termosBusca={termo_busca}"
        response = self.session.get(url)
        return response.json()
    
    def buscar_paradas(self, codigo_linha):
        
        url = f"{self.base_url}/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
        response = self.session.get(url)
        return response.json()
    
    def buscar_posicoes(self, codigo_linha):
     
        url = f"{self.base_url}/Posicao/Linha?codigoLinha={codigo_linha}"
        response = self.session.get(url)
        return response.json()
    
    def criar_mapa(self, codigo_linha, nome_linha):
   
        print(f"\n🚌 Buscando dados da linha {nome_linha}...")
        

        paradas = self.buscar_paradas(codigo_linha)
        print(f"✓ Encontradas {len(paradas)} paradas")

        dados_posicao = self.buscar_posicoes(codigo_linha)
        veiculos = dados_posicao.get('vs', [])
        hora_consulta = dados_posicao.get('hr', 'N/A')
        print(f"✓ Encontrados {len(veiculos)} ônibus em circulação")
        print(f"✓ Horário da consulta: {hora_consulta}")
        
 
        if paradas:
            lat_centro = sum(p['py'] for p in paradas) / len(paradas)
            lon_centro = sum(p['px'] for p in paradas) / len(paradas)
        else:
            lat_centro, lon_centro = -23.5505, -46.6333  
        

        mapa = Map(
            location=[lat_centro, lon_centro],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        

        for parada in paradas:
            Marker(
                location=[parada['py'], parada['px']],
                popup=folium.Popup(
                    f"<b>Parada: {parada['np']}</b><br>"
                    f"Endereço: {parada['ed']}<br>"
                    f"Código: {parada['cp']}",
                    max_width=300
                ),
                tooltip=parada['np'],
                icon=Icon(color='blue', icon='stop', prefix='fa')
            ).add_to(mapa)
        
    
        for veiculo in veiculos:
            acessivel = "Sim" if veiculo.get('a', False) else "Não"
            timestamp = veiculo.get('ta', 'N/A')
            
            Marker(
                location=[veiculo['py'], veiculo['px']],
                popup=folium.Popup(
                    f"<b>🚍 Ônibus - Prefixo: {veiculo['p']}</b><br>"
                    f"Acessível: {acessivel}<br>"
                    f"Última atualização: {timestamp}<br>"
                    f"Coordenadas: ({veiculo['py']:.6f}, {veiculo['px']:.6f})",
                    max_width=300
                ),
                tooltip=f"Ônibus {veiculo['p']}",
                icon=Icon(color='red', icon='bus', prefix='fa')
            ).add_to(mapa)
        

        legenda_html = f'''
        <div style="position: fixed; 
                    top: 10px; right: 10px; 
                    width: 280px; 
                    background-color: white; 
                    border:2px solid grey; 
                    z-index:9999; 
                    font-size:14px;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            <h4 style="margin-top:0;">Linha {nome_linha}</h4>
            <p><i class="fa fa-stop" style="color:blue"></i> <b>Paradas:</b> {len(paradas)}</p>
            <p><i class="fa fa-bus" style="color:red"></i> <b>Ônibus ativos:</b> {len(veiculos)}</p>
            <p><b>Horário:</b> {hora_consulta}</p>
            <hr style="margin: 8px 0;">
            <small>Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small>
        </div>
        '''
        mapa.get_root().html.add_child(folium.Element(legenda_html))
        

        arquivo = f"mapa_linha_{codigo_linha}.html"
        mapa.save(arquivo)
        print(f"\n✓ Mapa salvo em: {arquivo}")
        
        return mapa



if __name__ == "__main__":

    monitor = MonitoramentoOnibus(TOKEN)
    

    print("\n📋 Buscando linhas disponíveis...")
    linhas = monitor.buscar_linhas("Paulista")
    
    print(f"\nEncontradas {len(linhas)} linhas. Primeiras 5:")
    for i, linha in enumerate(linhas[:5]):
        print(f"{i+1}. Linha {linha['lt']} - {linha['tp']} → {linha['ts']} (código: {linha['cl']})")
    

    codigo_linha = 2503 
    nome_linha = "2780-10"
    

    mapa = monitor.criar_mapa(codigo_linha, nome_linha)
    
    print("\n✅ Processamento concluído!")
    print("📍 Legenda:")
    print("   🔵 Pins azuis = Paradas da linha")
    print("   🔴 Pins vermelhos = Ônibus em tempo real")