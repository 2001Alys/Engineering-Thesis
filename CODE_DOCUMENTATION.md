# Dokumentacja

Narzędzie do analizy sentymentu danych z serwisu Reddit podzielone jest na moduły, które współpracują ze sobą w celu przetwarzania i wizualizacji danych. Aplikacja umożliwia pobieranie postów, analizowanie ich sentymentu oraz ocenę wiarygodności na podstawie metadanych. Generowanie interaktywnego raportu HTML pozwala na interpretowanie wyników analizy za pomocą wykresów, tabel i szczegółowych informacji. Struktura aplikacji została zaprojektowana z myślą o efektywności i przejrzystości, umożliwiając wielowątkowe pobieranie danych. Cały proces jest zautomatyzowany, pozwala na optymalizację pobierania danych.

## Opis plików projektowych

- **check_trust_factor.py** - Moduł odpowiedzialny za wyznaczanie współczynnika zaufania. Przeprowadza analizę danych dotyczących autora postu, subreddita oraz samego postu w celu oszacowania, jak wiarygodne mogą być pobierane informacje.

- **generate_html.py** - Moduł ten generuje raport końcowy w formacie HTML.

- **GUI.py** - Moduł odpowiedzialny za interfejs użytkownika. Tworzy okno dialogowe, które umożliwia użytkownikowi interakcję z aplikacją.

- **main.py** - Główny plik łączący wszystkie funkcje. Koordynuje przepływ danych pomiędzy poszczególnymi modułami, zapewniając, że aplikacja działa płynnie.

- **make_charts.py** - Moduł generujący grafy, wykresy oraz tabele. Wykorzystuje dane zebrane i przetworzone przez pozostałe moduły w celu wizualizacji wyników.

- **search_reddit.py** - Moduł pobierający metadane z serwisu Reddita w celu wyznaczenia analizy sentymentu postów oraz współczynnika zaufania pobieranych elementów.

- **sentiment_analysis.py** - Moduł wyznaczający biegunowość analizy sentymentu pobranych metadanych z serwisu Reddit.

- **style.css** - Arkusz stylów odpowiedzialny za estetykę raportu HTML. Zawiera style, które poprawiają wygląd raportu i zwiększają jego czytelność.

## Przedstawienie i krótki opis funkcji

Podrozdział przedstawia krótki opis funkcji zawartych w modułach narzędzia projektowego. Opis funkcji wraz z modułem do jakiego przynależą:

### check_trust_factor.py

- **change_date_timestamp()** - Przekształca datę na rozszerzony format ISO 8601 (rok-miesiąc-dzień godzina:minuta:sekunda).

- **check_Subreddit()** - Oblicza współczynnik zaufania dla subredditu, uwzględniając m.in. wielkość aktywnej społeczności oraz czas istnienia subredditu.

- **check_Profile_info()** - Oblicza współczynnik zaufania dla autora postu, na podstawie takich parametrów jak: statusy konta, aktywność oraz wiek konta.

- **check_Post()** - Oblicza współczynnik zaufania dla samego postu, uwzględniając współczynnik zaufania autora postu i subreddita do jakiego przynależy post, jego czas istnienia oraz ocenę użytkowników.

- **analyze_trust_factor()** - Łączy wszystkie powyższe analizy współczynników zaufania i zapisuje je do wartości w celu wizualizacji wyników reprezentującej ogólny poziom zaufania do treści.

### generate_html.py

- **generate_distribution_rows()** - Generuje tabelę przedstawiającą rozkład analizy sentymentu komentarzy postów.

- **generate_details_rows()** - Tworzy tabele zawierające metadane postów oraz komentarzy.

- **generate_section()** - Generuje sekcje związane z sentymentem.

- **generate_html()** - Łączy wszystkie sekcje w całość, generuje i eksportuje kompletny raport HTML.

### GUI.py

- **reduce_query_count()** - Sprawdza ilość zapytań dostępnych do wykorzystania, w celu zarządzania i ograniczenia komunikacji z serwerem Reddita.

- **Pozostała część pliku** - Reszta pliku nie jest podzielona na funkcje, odpowiada za utworzenie interfejsu do komunikacji z użytkownikiem, w którym można wprowadzać zapytania i uzyskiwać wyniki analizy.

### main.py

- **count_query()** - Oblicza liczbę zapytań na podstawie liczby analizowanych postów, aby zoptymalizować proces i uniknąć ograniczeń komunikacji z serwerem Reddita.

 - **fetch_post_data()** - Integruje funkcje pobierające informacje o poście, subredditcie i autorze postu zapewniając pełen zestaw danych do dalszej analizy.

 - **link_posts_to_comments()** - Wykonuje wielowątkowe przeszukiwanie połączeń między postem a komentarzem, przyspiesza przetwarzanie dużych ilości danych.

- **link_search_analize()** - Główna pętla aplikacji łącząca wszystkie kluczowe funkcje, realizuje cały proces analizy.

### make_charts.py

- **make_pie_chart()** - Generuje wykres kołowy przedstawiający rozkład biegunowości sentymentu.

- **make_line_chart()** - Tworzy wykres liniowy pokazujący zależność czasu do liczby upvotes, wskazujący na popularność postu w czasie.

- **make_word_cloud()** - Generuje chmurę słów na podstawie pobranych tytułów oraz zawartości postów, pozwala użytkownikowi zobaczyć najczęściej pojawiające się słowa.

- **print_post_details()** - Tworzy tabelę z metadanymi postów, ułatwia wizualizację szczegółów wpisów.

### search_reddit.py

- **errory()** - Obsługuje komunikaty HTTP związane z serwerem Reddita, pomaga zarządzać wyjątkami podczas pobierania danych.

- **search_Home_post_id()** - Pobiera listę postów o określonej frazie.

- **search_Post_Comments()** - Pobiera zawartość postów wraz z komentarzami.

- **searchProfile_info()** - Pobiera niezbędne dane o autorze postu potrzebne do oceny wiarygodności danego redditora.

- **searchSubreddit_info()** - Pobiera dane o subredditcie, w którym został umieszczony post, pozwala dokonać analizy oceny wiarygodności subredditu.

### sentiment_analysis.py

- **vader()** - Analizuje sentyment z wykorzystaniem modelu VADER, zaprojektowanego do analizy tekstów w mediach społecznościowych.

- **analyze_posts()** - Analizuje tytuły i opis postu, co pozwala ocenić ogólny nastrój związany z danym wpisem.

- **label_vader()** - Etykietuje wyniki sentymentu na podstawie analizy VADER przypisując odpowiednie kategorie sentymentu.

- **analyze_comments()** - Analizuje sentyment każdego pobranego komentarza, daje pełniejszy obraz nastrojów w dyskusji.

- **count_sentiment()** - Sumuje wyniki analizy sentymentu, pozwala uzyskać podział sentymentów dla całej wyszukiwanej frazy.

- **count_upvotes()** - Sumuje wyniki analizy sentymentu, dzięki czemu można uzyskać podział sentymentów dla całej wyszukiwanej frazy. Następnie łączy sentyment z liczbą upvotes, co pozwala zobaczyć, które komentarze o danym wydźwięku cieszyły się największym uznaniem wśród użytkowników Reddita.
