import pandas as pd
import random #É válido ressaltar que essa é uma biblioteca que já vem no pacote padrão do python
import time #É válido ressaltar que essa é uma biblioteca que já vem no pacote padrão do python
from azure.iot.device import IoTHubDeviceClient, Message 
import duckdb

#String de conexão do dispositivo
connection_string ="HostName=PlataformaPreditiva.azure-devices.net;DeviceId=STM32;SharedAccessKey=9JQUXFqr1S1oeKc8XP3OlvEr+U9zXMCKJPmeIamlzDM="
                    

#Inicializa o cliente do dispositivo
client = IoTHubDeviceClient.create_from_connection_string(connection_string)

#Se conectar ao banco de dados
#conn = duckdb.connect("plataforma.duckdb")
#con.close()
#con = duckdb.connect('plataforma.duckdb')
#with duckdb.connect('plataforma.duckdb') as con:
class BACKEND:
    def predicaoCorrente(con):
        #while True:
            #Simulação de corrente elétrica de um motor específico
        correnteEletrica = random.uniform(5, 15)

            #Criar uma mensagem JSON
        mensagemCorrente = Message(f'{{"Corrente detectada:" {correnteEletrica}}}')

            #Enviar a mensagem para o IoT Hub
        #client.send_message(mensagemCorrente)
        print(f"Mensagem enviada: {mensagemCorrente}")

        inserindoErrodecorrentenoBanco = """INSERT INTO correnteEletrica(testeNome, parametro, horariodoTeste) VALUES (?, ?, CURRENT_TIMESTAMP);"""
        con.execute(inserindoErrodecorrentenoBanco, ('corrente', correnteEletrica))





                #BACKEN.enviar_telemetria()
                #BACKEND.precisadeManutencao()



                #Intervalo de uma mensagem para outra
                #time.sleep(5)

            #con.close()


    def enviar_telemetria(con):
            #while True:
            # Simula dados de telemetria
        temperatura = random.uniform(20, 30)
        umidade = random.uniform(30, 70)

            # Cria uma mensagem JSON
        mensagem = Message(f'{{"temperatura": {temperatura}, "umidade": {umidade}}}')

            # Envia a mensagem para o IoT Hub
        #client.send_message(mensagem)
        print(f"Mensagem enviada: {mensagem}")

            #Inserindo parâmetros de temperatura no banco
        inserindoErrodeTemperaturanoBanco = """INSERT INTO parametroTemperatura(testeNome, valorTemperatura, valorUmidade, horariodoTeste) VALUES (?, ?, ?, CURRENT_TIMESTAMP);"""
        con.execute(inserindoErrodeTemperaturanoBanco, ('temperatura', temperatura, umidade))

            # Intervalo entre as mensagens
            #time.sleep(5)






    def precisadeManutencao(con):
            #Definir algumas váriaveis que servirão como referência para os valores médios de cada parâmetro
        valorReferenciaCorrenteAlto = 145
        valorReferenciaTemperaturaAlto = 2995
        valorReferenciaUmidadeAlto = 6995
        valorReferenciaCorrenteBaixo = 55
        valorReferenciaTemperaturaBaixo = 2005
        valorReferenciaUmidadeBaixo = 3001

            #Consultas para trazer a média de cada parâmetro
        correnteMedia = con.execute("SELECT SUM(parametro) AS soma_parametro FROM (SELECT parametro FROM correnteEletrica ORDER BY id DESC LIMIT 10) subquery").fetchone()[0]
        temperaturaMedia = con.execute("SELECT SUM(valorTemperatura) AS soma_temperatura FROM (SELECT valorTemperatura FROM parametroTemperatura ORDER BY id DESC LIMIT 100) subquery").fetchone()[0]
        umidadeMedia = con.execute("SELECT SUM(valorUmidade) AS soma_umidade FROM (SELECT valorUmidade FROM parametroTemperatura ORDER BY id DESC LIMIT 100) subquery").fetchone()[0]


            #Aqui estamos fazendo a inserção no banco de dados caso ocorra um problema nos nívei de corrente
        if correnteMedia > 145:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('corrente', True))

        if correnteMedia < 55:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('corrente', False))


            #Aqui estamos fazendo uma inserção no banco de dados caso ocorra um problema nos níveis de temperatura
        if temperaturaMedia > 2995:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('temperatura', True))

        if temperaturaMedia < 2005:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('temperatura', False))


            #Aqui estamo fazendo uma inserção no banco de dados caso ocorra um problema nos níveis de umidade
        if umidadeMedia > 6995:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('umidade', True))

        if umidadeMedia < 3005:
            con.execute("INSERT INTO manutencaoPreventiva(problema, alto, dataidentificada) VALUES (?, ?, CURRENT_TIMESTAMP)", ('umidade', False))
            
    
    def limpaHistoricodeCorrente(con):
        idmaximo = con.execute("SELECT MAX(id) - 100 FROM correnteEletrica").fetchone()
        con.execute("DELETE FROM correnteEletrica WHERE id < ?", (idmaximo))
        
    def limpaHistoricoTemperatura(con):
        idtemperaturaMaximo = con.execute("SELECT MAX(id) - 300 FROM parametroTemperatura").fetchone()
        con.execute("DELETE FROM parametroTemperatura WHERE id < ?", (idtemperaturaMaximo))
    
    
    def funcaoMain():
            #String de conexão do dispositivo
        connection_string = "HostName=PlataformaPreditiva.azure-devices.net;DeviceId=STM32;SharedAccessKey=9JQUXFqr1S1oeKc8XP3OlvEr+U9zXMCKJPmeIamlzDM="

            #Inicializa o cliente do dispositivo
        client = IoTHubDeviceClient.create_from_connection_string(connection_string)

            #Se conectar ao banco de dados
            #conn = duckdb.connect("plataforma.duckdb")
            #con.close()
            #con = duckdb.connect('plataforma.duckdb')
            #with duckdb.connect('plataforma.duckdb') as con:
            #while True:
        with duckdb.connect('plataforma.duckdb') as con:
            BACKEND.predicaoCorrente(con)
            BACKEND.enviar_telemetria(con)
            BACKEND.precisadeManutencao(con)
            BACKEND.limpaHistoricodeCorrente(con)
            BACKEND.limpaHistoricoTemperatura(con)
            con.close()
            time.sleep(5)
            
        
        
#try:
    #BACKEND.funcaoMain()
#except KeyboardInterrupt:
    #print("Simulação interrompida.")
#finally:
    ##con.close()
    #client.shutdown()