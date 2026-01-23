"""
Script per la simulazione e la visualizzazione statistica del profilo medio dello sciame elettromagnetico.

Esegue più volte la simulazione dello sciame per tre differenti valori di energia.
Genera tre grafici in colonna riportando in funzione della distanza in unità di X0:
	- Numero medio di particelle presenti ad ogni passo per 3 valori di enegia inizale
	- Energia media persa per ionizzazione an ogni passo per 3 valori di enegia inizale
	- Energia media cumulata persa per ionizzazione ad ogni passo per 3 valori di enegia inizale
	I tre valori di energia sono E_min, E_max e il valore centrale tra questi due

Parametri accettati (argparse):
    E_min: Energia iniziale minima [MeV]
    E_max: Energia iniziale massima [MeV]
    ec_elettrone: Energia critica per elettroni [MeV]
    ec_positrone: Energia critica per positroni [MeV]
    dE_X0: Perdita per ionizzazione [MeV/cm]
    s: Passo di avanzamento in frazioni di X0 (s in (0,1])
    tipo: Tipo di particella iniziale (elettrone, positrone, fotone)
    n: Numero di simulazioni per ogni valore di energia
"""

import argparse
import plot_sciame as plot

parser = argparse.ArgumentParser(description='Simulazione e visualizzazione profilo sciame elettromagnetico')
parser.add_argument('E_min', type = float , help = 'Energia iniziale minima della particella [MeV]')
parser.add_argument('E_max', type = float , help = 'Energia iniziale massima della particella [MeV]')
parser.add_argument('ec_elettrone', type = float , help = 'Energia critica elettrone [MeV]')
parser.add_argument('ec_positrone', type = float , help = 'Energia critica positrone [MeV]')
parser.add_argument('dE_X0', type = float, help = 'Energia persa per ionizzazione in una lunghezza di radiazione [MeV]')
parser.add_argument('s', type = float , help = 'Passo di avanzamento in frazioni di X0 (s in (0,1])')
parser.add_argument('tipo',type = str, help = 'Tipo di particella iniziale (elettrone, positrone, fotone)')
parser.add_argument('n', type = int, help = 'Numero di simulazioni per ogni valore di energia')
args = parser.parse_args()

plot.visualizza_profilo(args.E_min, args.E_max, args.ec_elettrone, args.ec_positrone, args.dE_X0, args.s, args.tipo, args.n)

