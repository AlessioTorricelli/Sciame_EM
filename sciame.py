"""
Modulo sciame.py

Contiene classi per particelle (elettroni e positroni) e fotoni, e una funzione di simulazione di uno sciame.

"""


import numpy as np
		
class Particella:
	
	"""
	Rappresenta una particella carica dello sciame
	
	Attributi:
	
	E (float): energia della particella
	tipo (str): tipo della particella (elettrone o positrone)
	
	Metodi:
	
	evoluzione: simula l'evoluzione della particella in un passo
	esclusione: esclude la particella dallo sciame
	step: esegue un passo di evoluzione della particella
	"""
	
	def __init__(self, E0, tipo):
		
		self.E = E0
		
		if tipo == 'elettrone' or tipo == 'positrone' :
			self.tipo = tipo
		
		else:
			raise ValueError(f'La classe Particella non ammette "{tipo}" come tipo, inserire "elettrone" o "positrone".')
	
	def evoluzione(self, sciame, s, dE_X0, ec, E_ion):
		
		"""
		Simula la perdita di energia per ionizzazione e l'eventuale emissione di un fotone per Bremsstrahlung 
		
		Parametri: 
		
		sciame (list): lista della particelle o fotoni allo step successivo
		s (float): passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		dE_X0 (float): energia persa per ionizzazione in una lunghezza di radiazione
		ec (float): energia critica della particella
		E_ion (float): energia depositata per ionizzazione nel passo corrente
		
		Ritorna:
		
		E_ion (float): energia depositata aggiornata (dopo l'evoluzione)
		"""
		
		if self.E > dE_X0 * s:
				
			self.E = self.E - dE_X0 * s
			E_ion += dE_X0 * s
		
		if self.E > ec :
				
			p = np.random.random()
			
			if p > np.exp( -s ):
				
				sciame.append( Fotone(self.E/2) )
				self.E = self.E/2
			
		sciame.append(self)
		
		return E_ion
	
	def esclusione(self, E_ion):
		
		"""
		Esclude una particella dallo sciame aggiornando l'energia persa per ionizzazione
		
		Parametri:
		
		E_ion (float): energia depositata per ionizzazione nel passo corrente
		
		Ritorna:
		
		E_ion (float): energia depositata aggiornata
		"""
		
		En = np.random.uniform(0, self.E)
		E_ion += En
		self.E = 0
		return E_ion
		
	def step(self, s, sciame, E_ion, ec_elettrone, ec_positrone, dE_X0):
		
		"""
		Simula un passo per una particella
		
		Parametri:
		
		s (float): passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		sciame (list): lista della particelle o fotoni presenti allo step successivo
		E_ion (float): energia depositata per ionizzazione prima che la particella esegua lo step
		ec_elettrone (float): energia critica per gli elettroni nel materiale considerato
		ec_positrone (float): energia critica per i positroni nel materiale considerato
		dE_X0 (float): energia persa per ionizzazione in una lunghezza di radiazione
		
		Ritorna:
		
		E_ion: energia totale depositata per ionizzazione dopo lo step
		"""
		
		if self.E < dE_X0 * s:
		
			E_ion = self.esclusione(E_ion)
	
		else:
			if self.tipo == 'elettrone':
			
				E_ion = self.evoluzione(sciame, s, dE_X0, ec_elettrone, E_ion)
		
			else:
			
				E_ion = self.evoluzione(sciame, s, dE_X0, ec_positrone, E_ion)
			
		return E_ion
		
class Fotone:
	
	"""
	Rappresenta un fotone dello sciame
	
	Attributi:
	
	E (float): energia del fotone
	tipo (str): tipo della particella (fotone)
	
	Metodi:
	
	evoluzione: simula l'evoluzione della particella in un passo
	esclusione: esclude la particella dallo sciame
	step: esegue un passo di evoluzione della particella
	"""
	
	def __init__(self, E0):
		
		self.E = E0
		self.tipo = 'fotone'
	
	def evoluzione(self, sciame, s):
		
		"""
		Simula l'eventuale interazione di un fotone e l'emissione di un positrone e di un elettrone
		
		Parametri:
		
		sciame (list): lista della particelle o fotoni presenti allo step successivo
		s (float): passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		
		Ritorna:
		
		None
		"""
		
		p = np.random.random()
		if p > np.exp( -(7 * s )/ 9 ):
			sciame.append( Particella(self.E/2, 'elettrone') )
			sciame.append( Particella(self.E/2, 'positrone') )
		else:
			sciame.append(self)
	
	def esclusione(self, E_ion):
		
		"""
		Esclude una particella dallo sciame aggiornando l'energia persa per ionizzanione
		
		Parametri:
		
		E_ion (float): energia depositata per ionizzazione nel passo corrente
		
		Ritorna:
		
		E_ion (float): energia depositata aggiornata
		"""
		
		En = np.random.uniform(0, self.E)
		E_ion += En
		self.E = 0
		return E_ion
		
	def step(self, s, sciame, E_ion, ec_elettrone = None, ec_positrone = None, dE_X0 = None):
	
		"""
		Simula un passo per un fotone
		
		Parametri:
		
		s (float): passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
		sciame (list): lista della particelle o fotoni presenti allo step successivo
		E_ion (float): energia depositata per ionizzazione prima che il fotone esegua lo step
		ec_elettrone (float, opzionale): non utilizzato nella funzione, presente per compatibilità con la classe particella
		ec_positrone (float, opzionale): non utilizzato nella funzione, presente per compatibilità con la classe particella
		dE_X0 (float, opzionale): non utilizzato nella funzione, presente per compatibilità con la classe particella
		
		Ritorna:
		
		E_ion(float): energia totale depositata per ionizzazione dopo lo step
		"""
		
		if self.E > 2 * 0.511:
		
			self.evoluzione(sciame, s)
		
		else:
		
			E_ion = self.esclusione(E_ion)
	
		return E_ion
		

def simulazione(E0, ec_elettrone, ec_positrone, dE_X0, s, tipo):
	
	"""
	Simula uno sciame elettromagnetico
	
	Parametri:
	
	E0 (float): energia della particella iniziale
	ec_elettrone (float): energia critica per gli elettroni nel materiale in esame
	ec_positrone (float): energia critica per i positroni nel materiale in esame
	dE_X0 (float): perdita per ionizzazione in una lunghezza di radiazione
	s (float): passo di avanzamento della simulazione in frazioni di X0 (s in (0, 1])
	tipo (str): tipo della particella iniziale (elettrone, positrone, fotone) 
	
	Ritorna:
	
	E_step(list): energia depositata per ionizzazione in ogni step
	n_part(list): numero di particelle dello sciame in ogni step
	E_tot(float): energia totale depositata per ionizzazione
	"""

	sciame_i = []
	sciame_f = []
	n_part = [1]
	E_step = [0]
	n_steps = 0
	
	if E0 < 0 or ec_positrone < 0 or ec_elettrone < 0 or dE_X0 < 0:
		raise ValueError('Inserire valori di energia positivi')
		
	if s <= 0 or s > 1:
		raise ValueError("Il passo s deve essere compreso nell'intervallo (0,1]")
	
	if tipo == 'fotone':
		
		sciame_i.append(Fotone(E0))
	
	elif tipo == 'elettrone' or tipo == 'positrone':
		
		sciame_i.append(Particella(E0, tipo))
	
	else:
		raise ValueError("Inserire 'elettrone', 'positrone' o 'fotone' come particella iniziale")
	
	
	while len(sciame_i) != 0:
		n_steps += 1
		E_ion = 0
		
		for part in (sciame_i):
			
			E_ion = part.step(s, sciame_f, E_ion, ec_elettrone, ec_positrone, dE_X0)	
		
		E_step.append(E_ion)
		
		n_part.append(len(sciame_f))
		
		sciame_i = sciame_f
		sciame_f = []			
	
	E_tot = np.sum(E_step)
	return E_step, n_part, E_tot
