# 2023-10-18 - Charlie, sprint 3
## Ändringar/tillägg (i ingen speciell ordning):

### Profile-manager
- Skapade en ny modell för profile-table i DB, som är knuten till user-table via foreign key
- Backend för att kunna skapa, uppdatera och ta bort profiler
- Tog bort placeholder profilerna, la till loop som hämtar alla profiler från databasen och visar i samma format som placeholders
    - Avatar-bilderna är nu "random"
- La till ikoner/funktion för edit och delete på profilerna
- Finputsade struktur/placering etc på profilerna

### Task-manager
- Ändrade task_management frontend-delarna till bootstrap för behålla samma stil
- La till backend-funktion för att fetcha profiler från db för att kunna visa i listan
- La till loop som visar profilerna i "Användar"-listan istället för hårdkodade namn

### Övrigt (all kod)
- Städade kod, tog bort onödiga attribut, mellanslag, tomma rader etc
- Strukturerade om i koden
    - Flyttade all styling från profile_manager till CSS:en samt tog bort massa onödiga divs och klasser
    - Wrappade alla html:er som "extends layout.html" i en <body class="body">, lite frågetecken på denna men det gjorde koden mer konsekvent, och kunde då ta bort en del styling (typ margins etc) från div:ar som ska hålla samma stil. Detta löste också en bugg som jag upptäckte där "Household" samt ikonen inte följde med på alla sidor
    - La till enstaka kommentarer för scripts
- Ändrade/fixade sidebar:en
    - La till ett script och funktionalitet för att highlighta den aktiva sidan i sidebar:en
    - Ändrade namnen för att göra det mer lättläst och tydligt. "Tasks" är nu "Home", eftersom det är den första sidan man ska se ändå. (Allt detta är bara förslag)
- La till en "Log in" knapp som visas istället för logout om man inte är inloggad i navbar-ikonen (if-sats som kollar session.get("user"))
- La till en Changelog.md här i mappen, kanske kan användas framöver när någon gör stora förändringar?