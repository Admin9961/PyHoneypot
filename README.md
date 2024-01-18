Questo script è un honeypot che raccoglie le seguenti informazioni da chi prova a collegarcisi: Indirizzo IP, User-Agent, contenuto e tipo di richiesta (GET/POST), geolocalizzando automaticamente l'IP. Richiede Python3, e nello script dovete modificare il listener in accordo con le vostre esigenze.

Ho bindato all'honeypot un HTML-body con la possibilità di includere un'immagine per emulare il comportamento di un sito web. L'honeypot è fornito di un logger che salva i risultati in un output.
