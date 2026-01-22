# Sciame_EM
La cartella contiene i file necessari per la simulazione di sciami elettromagnetici e la visualizzazione delle loro caratteristiche.
La cartella contiene tre moduli:
  sciame.py
  Contiene le classi particella, fotone e una funzione di simulazione di un signolo sciame

  analisi_sciame.py
  Contiene due funzioni utili all'analisi statistica di uno sciame.
  con le funzioni implementate è possibile ottenere informazioni relative:
    al profilo medio di uno sciame per diversi valori di energia
    ai parametri medi dello sciame in funzione dell'energia della particella iniziale per diversi materiali

  plot_sciame.py
  Contiene tre funzioni utili a visualizzare i dati forniti dalle funzioni presenti in analisi_sciame.py
  Le funzioni presenti permettono di:
    visualizzare il profilo medio dello sciame in funzione della distanza percosrsa.
    visualizzare i parametri medi ottenuti in ogni materiale
    (I vari materiali possono essere riportati sovrapposti o in grafici differenti)

Nella cartella sono poi presenti due script per l'esecuzione:

  run_profilo_sciame.py:
    Lo script 
    simula più volte lo sciame per tre diversi valori di energia e calcola i valori medi dei risultati ottenuti
    produce un grafico di questi in funzione della distanza percorsa (in unità della lunghezza di radiazione)

    per un corretto funzionamento devono essere passati da riga di comando i seguenti parametri:
    E_min: Energia iniziale minima [MeV].
    E_max: Energia iniziale massima [MeV].
    ec_elettrone: Energia critica per elettroni [MeV].
    ec_positrone: Energia critica per positroni [MeV].
    dE_X0: Perdita per ionizzazione [MeV/X0].
    s: Passo di avanzamento in frazioni di X0 (s in (0,1])
    tipo: Tipo di particella iniziale (elettrone, positrone, fotone).
    n: Numero di simulazioni per ogni valore di energia.

    Esempio di utilizzo:
    
  
