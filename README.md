# Sciame_EM

Questo repository contiene i file necessari per la simulazione di sciami elettromagnetici, l'analisi statistica delle caratteristiche fisiche di questi e la loro visualizzazione.

---

## Struttura del Progetto

Il progetto è suddiviso in tre moduli principali e due script di esecuzione.

---

### Moduli

#### 1. `sciame.py`
Contiene:
* Le classi `Particella` e `Fotone`.
* Una funzione per la simulazione di un singolo sciame.

#### 2. `analisi_sciame.py`
Modulo dedicato all'analisi statistica degli sciami.  
Permette di ottenere:
* Il profilo medio dello sciame per diversi valori di energia.
* I parametri medi  in funzione dell'energia della particella iniziale per diversi materiali.

#### 3. `plot_sciame.py`
Consente la visualizzazione grafica dei risultati tramite tre funzioni che producono:
* Grafici del profilo medio in funzione della distanza percorsa.
* Confronto dei parametri medi tra diversi materiali (sovrapposti o separati).

---

### Script di Esecuzione

#### 1. `run_profilo_sciame.py`
Simula più volte lo sciame per tre valori di energia ($E_{min}$, $E_{max}$ e il valore medio) e calcola i valori medi di:
* Numero di particelle presenti
* Energia depositata per ionizzazione in ogni passo [MeV]
* Energia cumulativa depositata [MeV]
  
Produce tre grafici in funzione della distanza (in unità di lunghezza di radiazione $X_0$) delle quantità riportate sopra.


Parametri richiesti da riga di comando:
    
* Energia iniziale minima [MeV].
* Energia iniziale massima [MeV].
* Energia critica per elettroni [MeV].
* Energia critica per positroni [MeV].
* Perdita per ionizzazione [MeV/cm].
*  Lunghezza di radiazione [cm]
* Passo di avanzamento in frazioni di X0 (s in (0,1])
* Tipo di particella iniziale (elettrone, positrone, fotone).
* Numero di simulazioni per ogni valore di energia.

**Esempio di utilizzo:**
```
python3 run_profilo_sciame.py 2500 10000 13.37 12.94 4.785 2.588 0.1 positrone 100
```

    
#### 2. `run_analisi_mateirali.py`
Simula più volte uno sciame per valori di energia spaziati logaritmicamente nell'intervallo $(E_{min}, E_{max})$ e calcola i parametri medi. 
Il processo viene ripetuto per i materiali presenti nel dizionario interno (attualmente 'NaI' e 'Standard rock', ma espandibile).    
Produce grafici per i vari materiali (sovrapposti o separati) con i valori medi di:
* Energia totale depositata per ionizzazione [MeV]
* Numero massimo di particelle 
* Distanza massima raggiunta [cm]
* Posizione del massimo [cm]     

Tutti i grafici sono in funzione dell'energia della particella iniziale.
     
Parametri richiesti da riga di comando:
     
* Energia iniziale minima dell'intervallo di simulazione [MeV]
* Energia iniziale massima dell'intervallo di simulazione [MeV]
* Numero di simulazioni da eseguire per ogni valore di energia
* Numero di valori di energia da considerare nell'intervallo
* Passo di avanzamento in frazioni di X0 (s in (0,1])
* Tipo di particella iniziale (elettrone, positrone, fotone)
* --singoli (opzionale): Se presente, i grafici vengono mostrati singolarmente, non sovrapposti (consigliato se si aggiungono molti materiali)

**Esempio di utilizzo:**
```
python3 run_analisi_materiali.py 30 10000 10 100 0.1 positrone
```    
  
