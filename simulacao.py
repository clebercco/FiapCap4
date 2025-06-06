import pandas as pd
from datetime import datetime
import io

def ler_arquivo():
    data = pd.read_csv('rs_flood_data.csv')

    data['date'] = pd.to_datetime(data['date'])
    data['nivel_rio_m'] = pd.to_numeric(data['nivel_rio_m'], errors='coerce')
    data['deslocados_total'] = pd.to_numeric(data['deslocados_total'], errors='coerce').fillna(0)
    
    valid_risks = ['Baixo', 'Médio', 'Alto']
    data['risco_nivel'] = data['risco_nivel'].apply(lambda x: x if x in valid_risks else 'Desconhecido')
    
    return data

def determine_response(risk_level, river_level):
    if risk_level == 'Baixo' or river_level < 2.0:
        return "Status de Segurança: Monitoramento contínuo, nenhuma ação necessária."
    elif risk_level == 'Médio' or (river_level >= 2.0 and river_level < 4.0):
        return "Alerta: Preparação recomendada, risco moderado de inundação."
    elif risk_level == 'Alto' or river_level >= 4.0:
        return "Evacuação: Risco elevado de inundação, iniciar evacuação imediata."
    else:
        return "Status desconhecido: Verificar dados e sensores."

def simular(data):
    print("Simulação de Cenários de Inundação:")
    print("-" * 50)
    
    for index, row in data.iterrows():
        date = row['date'].strftime('%Y-%m-%d')
        river_level = row['nivel_rio_m']
        risk_level = row['risco_nivel']
        displaced = row['deslocados_total']
        
        response = determine_response(risk_level, river_level)
        
        print(f"Data: {date}")
        print(f"Nível do Rio: {river_level:.2f} metros")
        print(f"Risco: {risk_level}")
        print(f"Deslocados: {displaced:.0f}")
        print(f"Resposta do Sistema: {response}")
        print("-" * 50)


def run_tests(data):
    print("Executando Testes do Sistema:")
    print("-" * 50)
    
    # Test 1: Low risk scenario
    test_data_low = {'risco_nivel': 'Baixo', 'nivel_rio_m': 1.0}
    print("Teste 1 - Baixo Risco (1.0m):")
    print(determine_response(test_data_low['risco_nivel'], test_data_low['nivel_rio_m']))
    
    # Test 2: Medium risk scenario
    test_data_medium = {'risco_nivel': 'Médio', 'nivel_rio_m': 3.0}
    print("\nTeste 2 - Risco Médio (3.0m):")
    print(determine_response(test_data_medium['risco_nivel'], test_data_medium['nivel_rio_m']))
    
    # Test 3: High risk scenario
    test_data_high = {'risco_nivel': 'Alto', 'nivel_rio_m': 5.0}
    print("\nTeste 3 - Risco Alto (5.0m):")
    print(determine_response(test_data_high['risco_nivel'], test_data_high['nivel_rio_m']))
    
    # Test 4: Invalid data
    test_data_invalid = {'risco_nivel': 'Desconhecido', 'nivel_rio_m': None}
    print("\nTeste 4 - Dados Inválidos:")
    print(determine_response(test_data_invalid['risco_nivel'], test_data_invalid['nivel_rio_m']))
    
    print("-" * 50)

def main():

    data = ler_arquivo()
    simular(data)
    run_tests(data)

if __name__ == "__main__":
    main()