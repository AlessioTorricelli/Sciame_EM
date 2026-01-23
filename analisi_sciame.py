"""
Modulo analisi_sciame.py

Contiene le funzioni necessarie per analizzare l'andamento medio del profilo longitudinale dello sciame e dei suoi parametri.
"""

import numpy as np
import sciame

def profilo_medio(E0, ec_elettrone, ec_positrone, dE_X0, s, tipo, n):
	
	"""
	Simula uno sciame più volte e ne calcola i valori medi.
	
	Parametri:
		E0 (float): Energia della particella iniziale [MeV]
		ec_elettrone (float): Energia critica per gli elettroni nel materiale in esame [MeV]
		ec_positrone (float): Energia critica per i positroni nel materiale in esame [MeV]
		dE_X0 (float): Perdita per ionizzazione in una lunghezza di radiazione [MeV/cm]
		s (float): Passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		tipo (str): Tipo della particella iniziale (elettrone, positrone, fotone)
		n (int): Numero di simulazioni da eseguire
	
	Ritorna:
	risultati (dict): contiene
		- 'E_med' (list): Energia media depositata per ogni passo [MeV]
        - 'E_err' (list): Errore standard dell'energia media depositata [MeV]
        - 'n_med' (list): Numero medio di particelle per ogni passo
        - 'n_err' (list): Errore standard del numero medio di particelle
        - 'E_cum_med' (list): Energia cumulata media [MeV]
        - 'E_cum_err' (list): Errore standard dell'energia cumulata media [MeV]
        - 'distanza' (list): Coordinata longitudinale dello sciame (in unità di X0)
	"""
	if n <= 0:
		raise ValueError(f'Il numero n di simulazioni da ripetere per ogni valore di energia deve essere positivo')
	
	Energia = []
	n_particelle = []

	for i in range(n):
		
		E_step, n_part, E_tot = sciame.simulazione(E0, ec_elettrone, ec_positrone, dE_X0, s, tipo)
		
		Energia.append(E_step)
		n_particelle.append(n_part)
		
	massimo = max(len(p) for p in n_particelle)
	mat_en = np.zeros(n, massimo))
	mat_part = np.zeros(n, massimo))
	for i in range(n):
		for j in range(massimo):
			if len(Energia[i]) > j:
				mat_en[i][j] = Energia[i][j]
				mat_part[i][j] = particelle[i][j]

	E_med = np.mean(mat_en, axis=0)
	E_err = np.std(mat_en, axis=0)/np.sqrt(len(particelle))
	n_med = np.mean(mat_part, axis=0)
	n_err = np.std(mat_part, axis=0)/np.sqrt(len(particelle))

	mat_en_cum = np.cumsum(mat_en, axis=1)
	E_cum_med = np.mean(mat_en_cum, axis=0)
	E_cum_err = np.std(mat_en_cum, axis=0) / np.sqrt(n)
		
	distanza = [i * s for i in range(massimo)]
		
	risultati = {'E_med': E_med,
				 'E_err': E_err,
   				 'n_med': n_med,
				 'n_err': n_err,
				 'E_cum_med': E_cum_med,
				 'E_cum_err': E_cum_err,
				 'distanza': distanza}	
		
	return risultati



def sciame_stat(E0_min, E0_max, materiali, s, tipo, nE, n):
	
	"""
	Esegue più simulazioni dello sciame per diversi valori di energia spaziati logaritmicamente nell'intervallo dato.
	
	Parametri:
		E0_min (float): Valore minimo dell'intervallo di energie in cui vengono eseguite le simulazioni [MeV]
		E0_max (float): Valore massimo dell'intervallo di energie in cui vengono eseguite le simulazioni [MeV]
		materiali (dict): Contiente le informazioni dei parametri in esame.
			Ogni chiave è il nome del materiale (str) e il valore è una lista contenente:
			-ec_elettrone (float): Energia critica per gli elettroni nel materiale in esame [MeV]
			-ec_positrone (float): Energia critica per i positroni nel materiale in esame [MeV]
			-dE_X0 (float): Perdita per ionizzazione in una lunghezza di radiazione [MeV/cm]
			-X0 (float): Lunghezza di radiazione [cm]
			-colore (str): Colore da utilizzare per rappresentare nei grafici il materiale 
		s (float): Passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		tipo (str): Tipo della particella iniziale (elettrone, positrone, fotone)
		nE (int): Numero di valori di energia da considerare nell'intervallo scelto
		n (int): Numero di simulazioni da eseguire per ogni valore di energia
	
	Ritorna:
		Energie (np.array): Contiene le nE energie utilizzate.
		risultati (dict): Contiene i risultati  per ogni materiale.
				Ogni chiave è il nome del materiale (str) e il valore è un dict contenente:
				-'En' (list): energia totale media depositata per ionizzazione per ogni valore di energia [MeV]
				-'En_err' (list): errore standard dell'energia totale media depositata [MeV]
				-'n_max' (list): numero massimo medio di particelle presenti nello sciame per ogi valore di energia
				-'n_max_err' (list): errore standard del numero massimo medio di particelle
				-'dist_max' (list): distanza massima raggiunta in media dallo sciame per ogni valore di energia [cm]
				-'dist_max_err' (list): errore standard della distanza massima raggiunta [cm]
				-'massimo' (list): distanza media alla quale si ha il numero massimo di particelle per ogni valore di energua [cm]
				-'massimo_err' (list): errore standard della distanza media alla quale si ha il numero massimo di particelle [cm]
				-'color' (str): nome del colore da utilizzare per rappresentare nei grafici il materiale
	"""
	
	if E0_min < 0 or E0_max > 0:
		raise ValueError('Inserire valori di energia  positivo')
		
	if nE < 0 or n < 0:
		raise ValueError("'nE' e 'n' devono essere entrambi positivi")
		
	risultati = {}
	
	esponente_min = np.log10(E0_min)
	esponente_max = np.log10(E0_max)
	Energie = np.logspace(esponente_min, esponente_max, nE)
	
	for materiale in materiali:
		
		En = []                 #Energia media depositata per ogni E0
		En_err = []
				
		n_max = []				#Numero massimo medio di particelle per ogni E0
		n_max_err = []
			
		dist_max = []			#Distanza massima media raggiunta dallo sciame per ogni E0
		dist_max_err = []
				
		massimo = []			#Distanza media alla quale si trova il massimo dello sciame per ogni E0
		massimo_err = []

		for i in range(nE):
				
			En_simulazione = []   		 # n energie depositate per una E0
			n_max_simulazione = []		 # n numeri massimi di particelle per una E0
			n_passi = []		 		 # n numeri di passi eseguiti per una E0
			indice_massimo = []	 		 # n indici dove si trova il valore del massimo per una E0 
				
				
			for j in range(n):
					
				E_step, n_part, E_tot = sciame.simulazione(Energie[i], materiali[materiale][0], materiali[materiale][1], materiali[materiale][2] , s, tipo)

				En_simulazione.append(E_tot)
				n_max_simulazione.append(np.max(n_part))
				n_passi.append(len(n_part))
				indice_massimo.append(np.argmax(n_part))
					
				
			En.append(np.mean(En_simulazione))
			En_err.append(np.std(En_simulazione, ddof = 1)/np.sqrt(n))
				
			n_max.append(np.mean(n_max_simulazione))
			n_max_err.append(np.std(n_max_simulazione, ddof = 1)/np.sqrt(n))
				
			dist_max.append(np.mean(n_passi) * s * materiali[materiale][3])
			dist_max_err.append(np.std(n_passi, ddof = 1)/np.sqrt(n) * s * materiali[materiale][3])
			
			massimo.append(np.mean(indice_massimo) * s * materiali[materiale][3])
			massimo_err.append(np.std(indice_massimo, ddof = 1)/np.sqrt(n) * s * materiali[materiale][3])
			
			
		risultati[materiale] = {'En': En,
								'En_err': En_err,
								'n_max': n_max,
								'n_max_err': n_max_err,
								'dist_max': dist_max,
								'dist_max_err': dist_max_err,
								'massimo': massimo,
								'massimo_err': massimo_err,
								'color': materiali[materiale][4]}	
								
	return Energie, risultati
