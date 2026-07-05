# Analiza nastrojów na podstawie metadanych w serwisie społecznościowym Reddit

## Cel projektu

Celem projektu jest identyfikacja dominujących emocji w dyskusjach prowadzonych na platformie Reddit na podstawie:

- treści postów,
- komentarzy użytkowników,
- metadanych autorów,
- informacji o subredditach.

Dodatkowo system wyznacza współczynnik zaufania, pozwalający ocenić wiarygodność analizowanych treści.

## Funkcjonalności

- Wyszukiwanie postów według frazy.
- Pobieranie danych z Reddit bez użycia oficjalnego API.
- Analiza sentymentu postów i komentarzy.
- Ocena wiarygodności autora oraz społeczności.
- Filtrowanie i sortowanie wyników.
- Generowanie raportów HTML z wykresami i tabelami.
- Wielowątkowe pobieranie danych.
- Walidacja danych wejściowych.
- Ochrona przed XSS i HTML Injection.

## Technologie

- Python
- PyScript
- HTML / CSS
- VADER Sentiment
- httpx
- JSON

## Wybór modelu analizy sentymentu

W ramach projektu porównano kilka modeli NLP:

- RoBERTa
- DistilBERT
- BERT
- NLTK
- TextBlob
- VADER

Po przeprowadzeniu testów wybrano VADER, który zapewnił najlepszy kompromis pomiędzy:

- dokładnością klasyfikacji,
- szybkością działania,
- prostotą wdrożenia i dostrajania.

Model został dodatkowo rozszerzony o kategorie pośrednie:

- Positive
- Positive-Neutral
- Neutral
- Negative-Neutral
- Negative

Pozwoliło to lepiej odwzorować emocjonalną złożoność analizowanych treści.

### Wyniki walidacji

Model został zweryfikowany na zbiorze Sentiment140 obejmującym ponad 20 000 próbek.

Dokładność klasyfikacji: **69%**

Macierz pomyłek dla modelu VADER na zewnętrznym zbiorze danych
<table>
  <thead>
    <tr>
      <th colspan="6">VADER</th>
    </tr>
    <tr>
      <th rowspan="2">Etykieta klasy</th>
      <th colspan="3">Liczba próbek przyporządkowanych do klasy</th>
      <th rowspan="2">Liczba poprawnych decyzji</th>
      <th rowspan="2">Liczba błędnych decyzji</th>
    </tr>
    <tr>
      <th>Pozytywne</th>
      <th>Neutralne</th>
      <th>Negatywne</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Pozytywne</td>
      <td>5941</td>
      <td>2041</td>
      <td>642</td>
      <td>5941</td>
      <td>2683</td>
    </tr>
    <tr>
      <td>Neutralne</td>
      <td>961</td>
      <td>6022</td>
      <td>2476</td>
      <td>6022</td>
      <td>3437</td>
    </tr>
    <tr>
      <td>Negatywne</td>
      <td>116</td>
      <td>542</td>
      <td>2781</td>
      <td>2781</td>
      <td>658</td>
    </tr>
    <tr>
      <td><b>Suma = 21522</b></td>
      <td><b>7018</b></td>
      <td><b>8605</b></td>
      <td><b>5899</b></td>
      <td><b>14744 (69%)</b></td>
      <td><b>6778 (31%)</b></td>
    </tr>
  </tbody>
</table>

## Ogólny schemat blokowy programu
<img width="511" height="572" alt="popr drawio (2)" src="https://github.com/user-attachments/assets/67478b88-21d9-4789-94e1-37e736410d22" />

## Pobieranie danych

System wykorzystuje zapytania HTTP do publicznych endpointów JSON serwisu Reddit, dzięki czemu nie wymaga:

- konta Reddit,
- kluczy API,
- autoryzacji OAuth.

Dla zwiększenia wydajności zastosowano:

- wielowątkowość,
- ograniczenie liczby pobieranych pól JSON,
- filtrowanie zbędnych komentarzy,
- kontrolę liczby zapytań.

Analiza obejmuje:

- post,
- komentarze,
- autora,
- subreddit.

## Współczynnik zaufania

Wynik wiarygodności obliczany jest na podstawie:

- aktywności autora,
- wieku konta,
- karmy użytkownika,
- aktywności subreddita,
- zaangażowania społeczności.

Pozwala to odróżnić treści publikowane przez wiarygodnych użytkowników od potencjalnie mniej wartościowych wpisów.

## Bezpieczeństwo

Projekt zawiera mechanizmy zwiększające bezpieczeństwo oraz stabilność działania.

### Walidacja danych

- sprawdzanie poprawności fraz,
- kontrola liczby analizowanych postów,
- obsługa błędów HTTP,
- komunikaty dla użytkownika.

### Ograniczanie zapytań

- limit liczby żądań,
- automatyczne odświeżanie limitu po upływie czasu,
- ochrona przed przeciążeniem serwera.

### Ochrona raportów

- zabezpieczenie przed XSS,
- zabezpieczenie przed HTML Injection,
- sanitizacja danych użytkownika.

## Testy i walidacja

Przeprowadzono testy:

- poprawności generowania raportów,
- działania komunikatów błędów,
- dokładności analizy sentymentu,
- walidacji HTML zgodnie ze standardami W3C.

Wyniki potwierdziły poprawność działania aplikacji oraz zgodność analizy emocji z wynikami narzędzi referencyjnych, takich jak Social Searcher.

## Wnioski

Projekt umożliwia skuteczną analizę sentymentu treści publikowanych na Reddit. Połączenie modelu VADER, analizy metadanych oraz współczynnika zaufania pozwala nie tylko określić emocjonalny wydźwięk dyskusji, ale również ocenić wiarygodność źródła.

Najważniejsze rezultaty:

- skuteczna analiza sentymentu Reddit,
- dokładność modelu VADER na poziomie 69%,
- wydajne pobieranie danych dzięki wielowątkowości,
- generowanie interaktywnych raportów HTML,
- zabezpieczenia przed błędami i atakami XSS.

## Publikacje naukowe
- **[Kurek A., Sikora – „Wykorzystanie modelu NLP do analizy emocjonalnych wzorców w treściach 2025.pdf"](https://wteii.uniwersytetradom.pl/wp-content/uploads/sites/12/2025/06/2_Kurek_Sikora_ESM_1_2025.pdf)**  
  *European Student Magazine*, nr 1/2025, ISSN 2956-834X

## Słowa kluczowe
Sentiment Analysis · NLP · Reddit · VADER · Web Scraping · Social Media Analytics
