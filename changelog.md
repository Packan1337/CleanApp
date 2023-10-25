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

# 2023-10-18 - Charlie, sprint 3
## Bugfixes
- Fixade felhantering för "Manage profiles" + "Manage tasks", nu ombeds man logga in om man inte är det istället för att få ett error
- Fixade fetchen för profilerna i "Manage tasks", nu hämtas bara profilerna för den inloggade användaren

# 2023-10-24 - Charlie, sprint 4
## Ändringar på db_models.py, app.py
- Ändrade hur tabellerna skapas, tog bort __init__ delarna helt då detta är onödigt och kan skapa problem.
    - I app.py behövdes då koden för new_user ändras (från positional args till keyword args)
    - La till __tablename__ för att explicit sätta namn på tabellerna för att undvika problem
    - Ändrade task_title i Tasks till unique=True för att undvika att samma task läggs till flera gånger
- Ändrade hela add_list_to_taskdb funktionen till "initialize_tasks", 
som nu insertar listan med tasks (dicts) och sedan kollar i dbn varje gång appen startas om task_title redan finns och lägger bara till de som inte finns.
- Ändrade task_id till id i tabellen Tasks för att vara konsekvent med andra tabeller
- La till ondelete="CASCADE" till profiles och assigned_tasks (task_id, profile_id) för att den datan också ska tas bort om usern tas bort (Om parent tas bort tas också children bort)
- Ändrade "användare-lista" i dropdown-listorna i task_management.html till "profil-lista"
- Ändrade "value" för profilerna i dropdown-listorna till profil-namn istället för "användare1"
- La till en check för profil-listan i task_management.html, om den är tom så visas ett meddelande istället för en tom lista

# 2023-10-26 - Charlie, sprint 4
## Generella ändringar/tillägg
- La till en textruta för task-description i task_management.html
- La till datum och vecka i index.html
- Strukturerade om/snyggade till generellt i task_management.html
- La till ett meddelande i index.html om det inte finns några profiler
- Fixade om lite/fixade en bugg i databasen med cascade så att det nu funkar som tänkt

