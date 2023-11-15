import serial
import csv
from drawnow import drawnow
import matplotlib.pyplot as plt


# Função para atualizar o gráfico em tempo real
def atualizar_grafico():
    plt.subplot(3, 1, 1)
    plt.plot(dados_tempo, dados_X, label='Eixo X')
    plt.title('Dados do Acelerômetro em Tempo Real')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (g)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(dados_tempo, dados_Y, label='Eixo Y')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (g)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(dados_tempo, dados_Z, label='Eixo Z')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (g)')
    plt.legend()


# Inicializa a comunicação serial com o Arduino
ser = serial.Serial('COM5', 9600)  # Substitua 'COM5' pela porta serial apropriada

# Inicializa listas vazias para armazenar os dados
dados_tempo = []
dados_X = []
dados_Y = []
dados_Z = []

# Cria uma figura para a plotagem
plt.ion()
first_line = True

# Abre o arquivo CSV para escrita
with open('dados_acelerometro.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Escreve o cabeçalho no arquivo
    csv_writer.writerow(['Tempo (s)', 'Aceleração X (g)', 'Aceleração Y (g)', 'Aceleração Z (g)'])

    # Loop principal
    while True:
        try:
            # Lê uma linha da porta serial
            linha = ser.readline()

            decoded_line = linha.decode(errors='replace').strip()

            if first_line:
                first_line = False
                continue

            # Divide os dados em tempo, X, Y e Z
            data = decoded_line.split(',')
            t, X, Y, Z = map(float, data)

            # Adiciona os dados às listas
            dados_tempo.append(t)
            dados_X.append(X)
            dados_Y.append(Y)
            dados_Z.append(Z)

            # Escreve os dados no arquivo CSV
            csv_writer.writerow([dados_tempo[-1], dados_X[-1]])

            # Atualiza o gráfico
            drawnow(atualizar_grafico)

        except KeyboardInterrupt:
            # Fecha a conexão serial e sai do loop ao pressionar Ctrl+C
            ser.close()
            break
