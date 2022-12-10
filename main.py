import PySimpleGUI as sg
from time import time

def criar_janela():
    sg.theme('black')
    layout = [
        [sg.Push(), sg.Image('remove.png', pad=0, enable_events=True, key='-CLOSE-')],
        [sg.VPush()],
        [sg.Text('', font='Young 50', key='-TIME-')],
        [sg.Button('Start', button_color=('#FFFFFF', '#FF0000'), border_width=0, key='-STARTSTOP-'), sg.Button('Lap', button_color=('#FFFFFF', '#FF0000'), border_width=0, key='-LAP-', visible=False)],
        [sg.Column([[]], key='-LAPS-')],
        [sg.VPush()]
    ]

    return sg.Window(
        'Cronômetro',
        layout,
        size=(300, 300),
        no_titlebar=True,
        element_justification='center')

janela = criar_janela()
tempo_inicial = 0
solicitacao = False
volta = 1

while True:
    evento, values = janela.read(timeout = 10)
    if evento in (sg.WIN_CLOSED, '-CLOSE-'):
        break


    if evento == '-STARTSTOP-':
        if solicitacao:
            # from active to stop
            solicitacao = False
            janela['-STARTSTOP-'].update('Reset')
            janela['-LAP-'].update(visible=False)

        # parar o reset
        else:
            if tempo_inicial > 0:
                janela.close()
                janela = criar_janela()
                tempo_inicial = 0
                volta = 1

            # inicio para solicitacao
            else:
                tempo_inicial = time()
                solicitacao = True
                janela['-STARTSTOP-'].update('Stop')
                janela['-LAP-'].update(visible=True)

    if solicitacao:
        tempo_decorrido = round(time() - tempo_inicial, 1)
        janela['-TIME-'].update(tempo_decorrido)

    if evento == '-LAP-':
        janela.extend_layout(janela['-LAPS-'], [[sg.Text(volta), sg.VSeparator(), sg.Text(tempo_decorrido)]])
        volta += 1

janela.close()