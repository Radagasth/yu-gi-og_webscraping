Mi proyecto personal de webscraping usando https://ygoprodeck.com a base python
se divide en tres archivos diferentes 
Scraptorneos.py = obtiene las url necesariaas de las primeras 33 paginas de torneos https://ygoprodeck.com/tournaments/', da como resultado un excel (torneos.xlsx) con las url de los torneos 
UrlTorneo_dks.py toma como base las url de torneos almacenada en torneos.xlsx y crea un nuevo excel (decks.xlsx) con las url de los decks que se tienen registro 
Por ultimo ScrapCard.py toma como base las url de los mazos almacenadas en decks.xlsx y extrae las listas completas de cartas de todos los masos.
