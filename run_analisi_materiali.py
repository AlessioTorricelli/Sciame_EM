"""
Script per la simulazione e la visualizzazione statistica dei parametri medi dello sciame elettromagnetico.

Esegue la simulazione dello sciame per energie spaziate logaritmicamente in un intervallo dato e per diversi materiali.
Calcola i valori medi con relativi errori di:
	Energia totale depositata
	Numero massimo di particelle
	Distanza massima raggiunta
	Posizione del massimo
	
I dati ottenuti per ogni materiale possono essere rappresentati o sovrapposti o separatamente.

Parametri accettati (argparse):
    E0_min (float): Energia iniziale minima dell'intervallo di simulazione [MeV]
    E0_max (float): Energia iniziale massima dell'intervallo di simulazione [MeV]
    n (int): Numero di simulazioni da eseguire per ogni valore di energia
    nE (int): Numero di valori di energia da considerare nell'intervallo
    s (float): Passo di avanzamento in frazioni di X0 (s in (0,1])
    tipo (str): Tipo di particella iniziale (elettrone, positrone, fotone)
    --singoli (flag): Se presente, i grafici vengono mostrati singolarmente, non sovrapposti

Esempio di utilizzo:
    python3 run_analisi_materiali.py 30 10000 10 100 0.1 positrone --singoli
"""

import argparse
import analisi_sciame as an
import plot_sciame as plot

parser = argparse.ArgumentParser(description='Simulazione sciami elettromagnetici')
parser.add_argument('E0_min', type = float , help = "Energia iniziale minima dell'intervallo di simulazione [MeV]")
parser.add_argument('E0_max', type = float , help = "Energia iniziale massima dell'intervallo di simulazione [MeV]")
parser.add_argument('n', type = int,  help = 'Numero di simulazioni eseguite per ogni valore di energia' )
parser.add_argument('nE', type = int, help = "Numero di valori di energia nell'intervallo")
parser.add_argument('s', type = float , help = 'Passo di avanzamento in frazioni di X0')
parser.add_argument('tipo', type = str, help = 'Tipo di particella iniziale (elettrone, positrone fotone)')
parser.add_argument('--singoli', action = 'store_false', help = 'I grafici dei materiali vengono visualizzati singolarmente, non sovrapposti')
args = parser.parse_args()

#materiali = {'materiale': [ec_elettrone, ec_positrone, dE_X0, X0, color]}
materiali = {'NaI': [13.37, 12.94, 4.785, 2.588, 'purple'],
			 'Standard rock': [49.13, 47.74, 4.472, 10.02, 'green']
			 }

Energie, risultati = an.sciame_stat(args.E0_min, args.E0_max, materiali, args.s, args.tipo, args.nE, args.n)

if args.singoli:
	plot.confronto_materiali(Energie, risultati)

if not args.singoli:
	plot.singoli_materiali(Energie, risultati)
