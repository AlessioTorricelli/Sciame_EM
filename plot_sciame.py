'''
Modulo plot_sciame.py

Contiene le funzioni per visualizzare i grafici del profilo longitudinale e dei parametri dello sciame.
'''

import numpy as np
import analisi_sciame as an
import matplotlib.pyplot as plt

def visualizza_profilo(E_min, E_max, ec_elettrone, ec_positrone, dE_X0, s, tipo, n, X0):
	
	"""
	Genera tre grafici in colonna riportando in funzione della distanza (in unità di X0):
	- Numero di particelle presenti ad ogni passo per 3 valori di enegia inizale
	- Energia persa per ionizzazione an ogni passo per 3 valori di enegia inizale [MeV]
	- Energia cumulata persa per ionizzazione ad ogni passo per 3 valori di enegia inizale [MeV]
	I tre valori di energia sono E_min, E_max e il valore centrale tra questi.
	
	Parametri:
		E_min (float): Valore minimo di energia per cui vengono eseguite le simulazioni [MeV]
		E_max (float): Valore massimo di energia per cui vengono eseguite le simulazioni [MeV]
		ec_elettrone (float): Energia critica per gli elettroni nel materiale in esame [MeV]
		ec_positrone (float): Energia critica per i positroni nel materiale in esame [MeV]
		dE_X0 (float): Perdita per ionizzazione in una lunghezza di radiazione [MeV/cm]
		s (float): Passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		tipo (str): Tipo della particella iniziale (elettrone, positrone, fotone)
		n (int): Numero di simulazioni da eseguire
		X0 (float): Lunghezza di radiazione [cm]
		
	Ritorna:
		None
	"""
	
	if E_min < 0 or E_max < 0:
		raise ValueError("L'energia minima e massima devono essere entrambe positive")
	
	E0 = np.linspace(E_min, E_max, 3)
	
	fig, ax = plt.subplots(3,1, figsize = (12,9), sharex = True)
	fig.suptitle( f"Profilo medio di {n} sciami a diversi valori di energia", fontweight='bold',  fontsize=16)
	
	color = ['cornflowerblue', 'mediumseagreen', 'salmon']
	for i, e in enumerate(E0):
		
		risultati = an.profilo_medio(e, ec_elettrone, ec_positrone, dE_X0, s, tipo, n, X0)
		
		ax[0].errorbar(risultati['distanza'], risultati['n_med'], risultati['n_err'], label = f'{e:.0f} MeV', marker = '.', color = color[i])
		ax[1].errorbar(risultati['distanza'], risultati['E_med'], risultati['E_err'], label = f'$E_0$ = {e:.0f} MeV', marker = '.', color = color[i])
		ax[2].errorbar(risultati['distanza'], risultati['E_cum_med'], risultati['E_cum_err'], label = f'$E_0$ = {e:.0f} MeV', marker = '.', color = color[i])
		

	titoli = ['Numero medio di particelle per passo',
			  'Energia media persa per ogni passo',
			  'Energia cumulativa media persa a ogni passo']
	y_label = [r'$\bar{N}$',
			   r'$\overline{\Delta E}$ [MeV]',
			   r'$\bar{E}$ [MeV]']

	for i in range(3):
		ax[i].set_title(titoli[i], fontsize = 14)
		ax[i].grid(True, linestyle = '--', alpha = 0.5, color = 'gray')
		ax[i].set_ylabel(y_label[i], fontsize = 14, labelpad = 20)

	ax[0].legend(title =  'Energia iniziale:', title_fontweight = 'bold, 'fontsize = 10, loc = 'upper right')
	
	ax[2].set_xlabel(r'distanza [$X_0$]', fontsize = 14)
	fig.subplots_adjust(hspace=0.4)	

	plt.show()
	
	
	
def confronto_materiali(Energie, risultati):
	"""
	Genera due pannelli con due grafici ciascuno in funzione dell'enegia E0 della particella iniziale.
	In ogni grafico sono presenti i dati relativi ai vari materiali in esame.
	-Pannello1: Energia totale depositata e numero massimo medio di particelle
	-pannello2: Distanza massima media raggiunta e posizione media del massimo
	
	Parametri:
		Energie (np.array): Energie usate per eseguire le simulazioni [MeV]
		risultati (dict): Ogni chiave è il nome del materiale (str) e il valore è un dict contenente:
				-'En' (list): Energia totale media depositata per ionizzazione per ogni valore di energia [MeV]
				-'En_err' (list): Errore standard dell'energia totale media depositata [MeV]
				-'n_max' (list): Numero massimo medio di particelle presenti nello sciame per ogi valore di energia
				-'n_max_err' (list): Errore standard del numero massimo medio di particelle
				-'dist_max' (list): Distanza massima raggiunta in media dallo sciame per ogni valore di energia [cm]
				-'dist_max_err' (list): Errore standard della distanza massima raggiunta [cm]
				-'massimo' (list): Distanza media alla quale si ha il numero massimo di particelle per ogni valore di energua [cm]
				-'massimo_err' (list): Errore standard della distanza media alla quale si ha il numero massimo di particelle [cm]
				-'color' (str): Colore da utilizzare per rappresentare nei grafici il materiale
		Ritorna:
			None
	"""
	
	ylabel = [r'$\overline{E}_{ion}/E_0$', r'$\overline{d}_{stop}$ [cm]', r'$\overline{N}$', r'$\overline{d}_{max}$ [cm]']	
	
	fig1, ax1 = plt.subplots(2,1, figsize  = (13, 8), sharex = True)
	fig2, ax2 = plt.subplots(2,1, figsize  = (13, 8), sharex = True)

	fig1.suptitle(r'Frazione di $\mathbf{E_0}$ depositata e distanza raggiunta', fontweight='bold', fontsize = 16)
	fig2.suptitle('Numero massimo di particelle e posizione del massimo', fontweight='bold', fontsize = 16)
	for materiale in risultati:
		
		ax1[0].errorbar(Energie, risultati[materiale]['En']/Energie, risultati[materiale]['En_err']/Energie, fmt = '.', label = materiale ,color = risultati[materiale]['color'])
		ax2[0].errorbar(Energie, risultati[materiale]['n_max'], risultati[materiale]['n_max_err'], fmt = '.', label = materiale, color = risultati[materiale]['color'])
		ax1[1].errorbar(Energie, risultati[materiale]['dist_max'], risultati[materiale]['dist_max_err'], fmt = '.', label = materiale, color = risultati[materiale]['color'])
		ax2[1].errorbar(Energie, risultati[materiale]['massimo'], risultati[materiale]['massimo_err'], fmt = '.', label = materiale, color = risultati[materiale]['color'])	
			
	for i in range(0,2):
			
		ax1[i].set_ylabel(ylabel[i], fontsize = 14, labelpad = 20)
		ax1[i].grid(True, linestyle = '--', alpha = 0.5, color = 'gray')
		ax1[i].set_xscale('log')
		ax1[i].legend(fontsize = 14)
		
		ax2[i].set_ylabel(ylabel[i+2], fontsize = 14, labelpad = 20)
		ax2[i].grid(True, linestyle = '--', alpha = 0.5, color = 'gray')
		ax2[i].set_xscale('log')
		ax2[i].legend(fontsize = 14)
		
	ax1[1].set_xlabel(r'$E_0$ [MeV]', fontsize = 14)
	ax2[1].set_xlabel(r'$E_0$ [MeV]', fontsize = 14)	

	fig1.tight_layout()
	fig2.tight_layout()
	
	plt.show()
		
	

def singoli_materiali(Energie, risultati):
	
	"""
	Genera due pannelli per ogni materiale con due grafici ciascuno in funzione dell'enegia E0 della particella iniziale.
	
	Parametri:
		Energie (np.array): Energie usate per eseguire le simulazioni [MeV]
		risultati (dict): Ogni chiave è il nome del materiale (str) e il valore è un dict contenente:
				-'En' (list): Energia totale media depositata per ionizzazione per ogni valore di energia [MeV]
				-'En_err' (list): Errore standard dell'energia totale media depositata [MeV]
				-'n_max' (list): Numero massimo medio di particelle presenti nello sciame per ogi valore di energia
				-'n_max_err' (list): Errore standard del numero massimo medio di particelle
				-'dist_max' (list): Distanza massima raggiunta in media dallo sciame per ogni valore di energia [cm]
				-'dist_max_err' (list): Errore standard della distanza massima raggiunta [cm]
				-'massimo' (list): Distanza media alla quale si ha il numero massimo di particelle per ogni valore di energua [cm]
				-'massimo_err' (list): Errore standard della distanza media alla quale si ha il numero massimo di particelle [cm]
				-'color' (str): Colore da utilizzare per rappresentare nei grafici il materiale
		Ritorna:
			None
	"""
	
	ylabel = [r'$\overline{E}_{ion}/E_0$', r'$\overline{d}_{stop}$ [cm]', r'$\overline{N}$', r'$\overline{d}_{max} [cm]$']	
	
	for materiale in risultati:
		
		fig1, ax1 = plt.subplots(2,1, figsize  = (13, 8), sharex = True)
		fig2, ax2 = plt.subplots(2,1, figsize  = (13, 8), sharex = True)
		
		fig1.suptitle(fr'Frazione di $\mathbf{{E_0}}$ depositata e distanza raggiunta in "{materiale}"', fontweight='bold', fontsize=16)
		fig2.suptitle(f'Numero massimo di particelle e posizione del massimo in "{materiale}"', fontweight='bold', fontsize=16)
		
		ax1[0].errorbar(Energie, risultati[materiale]['En']/Energie, risultati[materiale]['En_err']/Energie, fmt = '.' ,color = risultati[materiale]['color'])
		ax2[0].errorbar(Energie, risultati[materiale]['n_max'], risultati[materiale]['n_max_err'], fmt = '.', color = risultati[materiale]['color'])
		ax1[1].errorbar(Energie, risultati[materiale]['dist_max'], risultati[materiale]['dist_max_err'], fmt = '.', color = risultati[materiale]['color'])
		ax2[1].errorbar(Energie, risultati[materiale]['massimo'], risultati[materiale]['massimo_err'], fmt = '.', color = risultati[materiale]['color'])	
				
		for i in range(2):
				
			ax1[i].set_ylabel(ylabel[i], fontsize = 14, labelpad = 20)
			ax1[i].grid(True, linestyle = '--', alpha = 0.5, color = 'gray')
			ax1[i].set_xscale('log')
			
			ax2[i].set_ylabel(ylabel[i+2], fontsize = 14, labelpad = 20)
			ax2[i].grid(True, linestyle = '--', alpha = 0.5, color = 'gray')
			ax2[i].set_xscale('log')
		
		ax1[1].set_xlabel(r'$E_0$ [MeV]', fontsize = 14)
		ax2[1].set_xlabel(r'$E_0$ [MeV]', fontsize = 14)

		fig1.tight_layout()
		fig2.tight_layout()
		
		plt.show()	



