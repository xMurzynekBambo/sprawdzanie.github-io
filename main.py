import os
import random
import requests
import time

# Lokalna wersja aplikacji
LOCAL_VERSION = "0.03"
# Adres URL pliku z aktualną wersją
VERSION_URL = "https://xmurzynekbambo.github.io/sprawdzanie.github-io/version.txt"
co_ma_pobrac = "https://xmurzynekbambo.github.io/sprawdzanie.github-io/main.py"
lokalna_nazwa_pliku = "main.py"

class GameState:
    def __init__(self, nr_pokoj=0, gracz_hp=100, gold=0, przeciwnik_dmg=None, dmg=None):
        self.nr_pokoj = nr_pokoj
        self.gracz_hp = gracz_hp
        self.gold = gold
        self.przeciwnik_dmg = przeciwnik_dmg or random.randint(3, 7)
        self.dmg = dmg or random.randint(6, 10)

# Narzędzia

def wyczysc_ekran():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/macOS
        os.system('clear')

def sprawdz_wersje():
    try:
        response = requests.get(VERSION_URL, timeout=5)
        if response.status_code == 200:
            server_version = response.text.strip()
            if server_version > LOCAL_VERSION:
                print("/pobierz")
                co_zrobic = input()
                if(co_zrobic=="/pobierz"):
                    pobierz_plik(co_ma_pobrac, lokalna_nazwa_pliku)
                else:
                    exit()
            else:
                return True
        else:
            print("Nie udało się sprawdzić aktualnej wersji")
            time.sleep(5)
            exit()
    except requests.ConnectionError as e:
        print(f"Brak połączenia z serwerem: {e}")
        return False
    except Exception as e:
        print(f"Wystąpił błąd podczas sprawdzania wersji: {e}")
        return False

def pobierz_plik(co_ma_pobrac, lokalna_nazwa_pliku):
    try:
        print("Pobieranie pliku...")
        response = requests.get(co_ma_pobrac, timeout=10)
        if response.status_code == 200:
            with open(lokalna_nazwa_pliku, "wb") as file:
                file.write(response.content)
            print(f"Plik został pomyślnie pobrany jako {lokalna_nazwa_pliku}.")
        else:
            print(f"Błąd podczas pobierania pliku: {response.status_code}")
    except requests.ConnectionError:
        print("Nie udało się połączyć z serwerem. Sprawdź swoje połączenie internetowe.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

# Funkcje gry

def zapisz_gre(game_state, nazwa_zapisu):
    folder_zapisow = "saves"
    if not os.path.exists(folder_zapisow):
        os.makedirs(folder_zapisow)

    sciezka_zapisu = os.path.join(folder_zapisow, f"{nazwa_zapisu}.txt")
    with open(sciezka_zapisu, "w") as file:
        file.write(f"nr_pokoj {game_state.nr_pokoj}\n")
        file.write(f"gracz_hp {game_state.gracz_hp}\n")
        file.write(f"gold {game_state.gold}\n")
        file.write(f"przeciwnik_dmg {game_state.przeciwnik_dmg}\n")
        file.write(f"dmg {game_state.dmg}\n")
    print(f"Gra zapisana pomyślnie w pliku {sciezka_zapisu}.")

def wczytaj_gre(nazwa_zapisu):
    folder_zapisow = "saves"
    sciezka_zapisu = os.path.join(folder_zapisow, f"{nazwa_zapisu}.txt")
    try:
        with open(sciezka_zapisu, "r") as file:
            dane = {}
            for linia in file:
                klucz, wartosc = linia.strip().split(" ")
                dane[klucz] = int(wartosc)
            return GameState(
                nr_pokoj=dane.get("nr_pokoj", 0),
                gracz_hp=dane.get("gracz_hp", 100),
                gold=dane.get("gold", 0),
                przeciwnik_dmg=dane.get("przeciwnik_dmg", random.randint(3, 7)),
                dmg=dane.get("dmg", random.randint(6, 10))
            )
    except FileNotFoundError:
        print("Zapis o podanej nazwie nie istnieje.")
        return None

def walka_z_przeciwnikiem(game_state):
    print("Uwaga! Znalazłeś się w zasadzce!")
    przeciwnik_hp = random.randint(1, 10)
    print(f"HP przeciwnika: {przeciwnik_hp}")

    while przeciwnik_hp > 0 and game_state.gracz_hp > 0:
        print(f"Twoje HP: {game_state.gracz_hp}")
        komenda = input("Podaj komendę: ")

        if komenda == "/napierdalaj":
            game_state.gold += int(game_state.dmg * 0.10)
            przeciwnik_hp -= game_state.dmg
            if przeciwnik_hp <= 0:
                print("Rozgromiłeś przeciwnika!")
            else:
                game_state.gracz_hp -= game_state.przeciwnik_dmg
        else:
            print("Nieznana komenda!")

    if game_state.gracz_hp <= 0:
        print("Zginąłeś! Gra kończy się.")
        return False
    return True

def przeszukaj_pokoj(game_state):
    print("Przeszukujesz pokój...")
    znaleziono = random.choice(["zloto", "bron"])
    if znaleziono == "zloto":
        zgold = random.randint(10, 50)
        game_state.gold += zgold
        print(f"Znalazłeś {zgold} złota. Masz teraz {game_state.gold}.")
    else:
        print("Znalazłeś nową broń!")

def wyswietl_statystyki(game_state):
    print(f"Twoje statystyki: HP = {game_state.gracz_hp}, Pokój = {game_state.nr_pokoj}, Złoto = {game_state.gold}")

# Główna funkcja gry

def rozpocznij_gre():
    game_state = GameState()

    print("Chcesz wczytać grę czy rozpocząć nową? (/wczytaj lub Enter)")
    komenda = input("Podaj komendę: ")

    if komenda == "/wczytaj":
        nazwa_zapisu = input("Podaj nazwę zapisu do wczytania: ")
        stan_gry = wczytaj_gre(nazwa_zapisu)
        if stan_gry:
            game_state = stan_gry
        else:
            return
    else:
        print("Rozpoczynasz nową grę!")

    while True:
        
        komenda = input("\nPodaj komendę: ")
        wyczysc_ekran()
        if komenda == "/komendy":
            print("Dostępne komendy:\n",
                  "/dalej - przechodzisz do kolejnego pokoju\n",
                  "/przeszukaj - przeszukujesz pokój\n",
                  "/statystyki - wyświetla twoje statystyki\n",
                  "/save - zapisuje stan gry\n",
                  "/wczytaj - wczytuje stan gry\n",
                  "/wyjdz - zakończ grę\n",
                  "/boss - walka z bossem (po 50 pokoju)")

        elif komenda == "/dalej":
            game_state.nr_pokoj += 1
            print(f"\nWchodzisz do pokoju nr {game_state.nr_pokoj}.")

            if game_state.nr_pokoj % 10 == 0:
                game_state.przeciwnik_dmg += 10
                print(f"Obrażenia przeciwnika wzrosły! Teraz zadaje {game_state.przeciwnik_dmg} obrażeń.")

            if random.choice([True, False]):
                if not walka_z_przeciwnikiem(game_state):
                    break
            else:
                print("To jest bezpieczny pokój. Możesz kontynuować.")

        elif komenda == "/przeszukaj":
            przeszukaj_pokoj(game_state)

        elif komenda == "/statystyki":
            wyswietl_statystyki(game_state)

        elif komenda == "/save":
            nazwa_zapisu = input("Podaj nazwę zapisu: ")
            zapisz_gre(game_state, nazwa_zapisu)

        elif komenda == "/wyjdz":
            print("Wychodzenie z gry...")
            break

        else:
            print("Nieznana komenda. Spróbuj ponownie.")

if __name__ == "__main__":
    if sprawdz_wersje():
        rozpocznij_gre()
