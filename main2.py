import requests
import time
# Lokalna wersja aplikacji
LOCAL_VERSION = "0.02"

# Adres URL pliku z aktualną wersją
VERSION_URL = "https://xmurzynekbambo.github.io/sprawdzanie.github-io/version.txt"

def check_ingame():
    try:
        # Pobieranie aktualnej wersji z serwera
        print(f"Łączenie z {VERSION_URL}...")
        response = requests.get(VERSION_URL, timeout=5)
        
        if response.status_code == 200:
            server_version = response.text.strip()
            if server_version > LOCAL_VERSION:
                print("pobierz nowa wersja")
                time.sleep(5)
                exit
            else:
                return True  # Kontynuuj skrypt
        else:
            print("Nie udało się sprawdzić aktualnej wersji")
            time.sleep(5)
            exit
    except requests.ConnectionError as e:
        print(f"Brak połączenia z serwerem: {e}")
        return False
    except Exception as e:
        print(f"Wystąpił błąd podczas sprawdzania wersji: {e}")
        return False  # Zatrzymaj w przypadku błędu

def check_version_and_run():
    try:
        # Pobieranie aktualnej wersji z serwera
        print(f"Łączenie z {VERSION_URL}...")
        response = requests.get(VERSION_URL, timeout=5)
        
        if response.status_code == 200:
            server_version = response.text.strip()
            print(f"Aktualna wersja serwera: {server_version}")
            
            # Porównanie wersji
            if server_version > LOCAL_VERSION:
                print(f"Używasz starej wersji aplikacji ({LOCAL_VERSION}).")
                print(f"Najnowsza wersja to {server_version}. Zaktualizuj aplikację, aby kontynuować.")
                return False  # Zatrzymaj skrypt
            else:
                print(f"Używasz najnowszej wersji ({LOCAL_VERSION}).")
                return True  # Kontynuuj skrypt
        else:
            print("Nie udało się sprawdzić aktualnej wersji")
            time.sleep(5)
            exit
    except requests.ConnectionError as e:
        print(f"Brak połączenia z serwerem: {e}")
        return False
    except Exception as e:
        print(f"Wystąpił błąd podczas sprawdzania wersji: {e}")
        return False  # Zatrzymaj w przypadku błędu

def main_script():
    import random
    import os


    # Początkowe wartości statystyk gracza i przeciwnika
    gold = 0  # Ilość złota posiadanego przez gracza
    nrpokoj = 0  # Numer aktualnego pokoju
    gracz_hp = 100  # Punkty życia gracza
    przeciwnik_dmg = random.randint(3, 7)  # Losowe obrażenia przeciwnika na początku

    # Tworzenie folderu do zapisywania gier, jeśli nie istnieje
    save_folder = "saves"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)


    # Funkcja do zapisywania gry
    def save_game(save_name, nrpokoj, gracz_hp, gold, przeciwnik_dmg):
        save_path = os.path.join(save_folder, f"{save_name}.txt")
        with open(save_path, "w") as file:
            # Dane są zapisywane w losowej kolejności, co utrudnia manipulację plikiem
            data = [("1", nrpokoj), ("2", gracz_hp), ("3", przeciwnik_dmg), ("4", gold)]
            random.shuffle(data)
            for key, value in data:
                file.write(f"{key} {value}\n")
        print(f"Gra zapisana pomyślnie w pliku {save_path}.")


    # Funkcja do wczytywania gry
    def load_game(save_name):
        save_path = os.path.join(save_folder, f"{save_name}.txt")
        try:
            with open(save_path, "r") as file:
                data = {}
                # Wczytywanie danych i mapowanie do odpowiednich zmiennych
                for line in file:
                    key, value = line.strip().split(" ")
                    data[key] = int(value)
                nrpokoj = data.get("1", 0)
                gracz_hp = data.get("2", 100)
                przeciwnik_dmg = data.get("3", 3)
                gold = data.get("4", 0)
                return nrpokoj, gracz_hp, przeciwnik_dmg, gold
        except FileNotFoundError:
            print("Zapis o podanej nazwie nie istnieje.")
            return None


    # Ekran początkowy gry
    print("0.0.0.0.0.0")
    print("\n\n")
    print("Chcesz wczytać grę czy rozpocząć nową? (/wczytaj lub Enter)")
    komenda = input("Podaj komendę: ")

    # Obsługa wczytywania gry
    if komenda == "/wczytaj":
        save_name = input("Podaj nazwę zapisu do wczytania: ")
        game_data = load_game(save_name)
        if game_data:
            nrpokoj, gracz_hp, przeciwnik_dmg, gold = game_data
            print(f"Stan gry wczytany pomyślnie. Jesteś w pokoju nr {nrpokoj}. Twoje HP: {gracz_hp}. Złoto: {gold}.")
        else:
            exit()  # Zamykanie gry, jeśli nie można wczytać zapisu
    else:
        # Rozpoczęcie nowej gry
        print("\nMasz przejsc przez pokoje i zabic bossa pozdro")
        
    # Główna pętla gry
    while True:
        komenda = input("\nPodaj komendę: ")
        check_ingame()
        # Wyświetlanie dostępnych komend
        if komenda == "/komendy":
            print("Dostępne komendy:\n",
                "/dalej - przechodzisz do kolejnego pokoju\n",
                "/przeszukaj - przeszukujesz pokój\n",
                "/statystyki - wyświetla twoje statystyki\n",
                "/save - zapisuje stan gry\n",
                "/wczytaj - wczytuje stan gry\n",
                "/wyjdz - zakończ grę\n",
                "/boss - napierdalaj bosa(po 50 pokoju)")

        # Przejście do kolejnego pokoju
        elif komenda == "/dalej":
            nrpokoj += 1
            print(f"\nWchodzisz do pokoju nr {nrpokoj}.")
            if nrpokoj % 10 == 0:  # Co 10 pokoi przeciwnik staje się silniejszy
                przeciwnik_dmg += 10
                print(f"Obrażenia przeciwnika wzrosły! Teraz zadaje {przeciwnik_dmg} obrażeń.\n")
                input("wcisnij ENTER aby kontynuowac\n")
                print("witaj w sklepie\n")
                

            # Losowanie rodzaju pokoju
            pokoj = random.choice(["Zasadzka w Korytarzu", "Bezpieczny Pokój\n"])
            print(f"Wchodzisz do pokoju: {pokoj}")

            if pokoj == "Zasadzka w Korytarzu":
                print("Uwaga! Znalazłeś się w zasadzce!")
                hp = random.randint(1, 10)  # Losowe HP przeciwnika
                print(f"HP przeciwnika: {hp}")

                # Walka z przeciwnikiem
                while hp > 0 and gracz_hp > 0:
                    print(f"Twoje HP: {gracz_hp}")
                    komenda = input(f"Co chcesz zrobić? (Obrażenia przeciwnika: {przeciwnik_dmg})\nPodaj komendę: ")

                    if komenda == "/napierdalaj":
                        dmg = random.randint(5, 8)  # Losowe obrażenia zadawane przeciwnikowi
                        print(f"Zadajesz {dmg} obrażeń przeciwnikowi.\n")
                        hp -= dmg
                        if hp <= 0:
                            print("Rozgromiłeś przeciwnika!\n")
                        else:
                            print(f"Przeciwnikowi zostało {hp} HP.")
                            gracz_hp -= przeciwnik_dmg  # Gracz otrzymuje obrażenia
                            print(f"Przeciwnik zadaje {przeciwnik_dmg} obrażeń. Twoje HP: {gracz_hp}")
                    else:
                        print("Nieznana komenda! Spróbuj ponownie.")

                # Koniec gry, jeśli gracz umarł
                if gracz_hp <= 0:
                    print("Zginąłeś! Gra kończy się.")
                    break
            else:
                print("To jest bezpieczny pokój. Możesz kontynuować.")

        # Przeszukiwanie pokoju
        elif komenda == "/przeszukaj":
            print("Przeszukujesz pokój...")
            znaleziono = random.choice(["zloto", "bron"])  # Losowanie nagrody
            if znaleziono == "zloto":
                zgold = random.randint(10, 50)
                gold += zgold
                print(f"Znalazłeś {zgold} złota. Masz teraz {gold}.")
            else:
                print("Znalazłeś nową broń!")
        elif komenda=="/boss":
            if(nrpokoj>=50):
                print("cwel")
            else:
                print(f"jestes w pokoju {nrpokoj} a potrzebujesz byc w conajmniej 50")

        # Wyświetlanie statystyk gracza
        elif komenda == "/statystyki":
            print(f"Twoje statystyki: HP = {gracz_hp}, Pokój = {nrpokoj}, Obrażenia przeciwnika = {przeciwnik_dmg}, Złoto = {gold}")

        # Zapis gry
        elif komenda == "/save":
            save_name = input("Podaj nazwę zapisu: ")
            save_game(save_name, nrpokoj, gracz_hp, gold, przeciwnik_dmg)

        # Wyjście z gry
        elif komenda == "/wyjdz":
            print("Wychodzenie z gry...")
            break

        # Obsługa nieznanych komend
        else:
            print("Nieznana komenda. Spróbuj ponownie.")


if check_version_and_run():
    main_script()
else:
    print("Skrypt zatrzymany z powodu braku zgodności wersji.")
