<<<<<<< HEAD
# Create a txt file of all pokemon names using the
# pokebase API.

import pokebase as pb


pokemon_number = 1 # first pokemon_number (Bulbasaur)
with open('pokemon.txt', 'w') as f:
    try:
        while True:
            pokemon_name = pb.pokemon(pokemon_number).name
            f.write("{}\n".format(pokemon_name))
            print("Wrote {} to file".format(pokemon_name))
            pokemon_number += 1
    except ValueError:
=======
# Create a txt file of all pokemon names using the
# pokebase API.

import pokebase as pb


pokemon_number = 1 # first pokemon_number (Bulbasaur)
with open('pokemon.txt', 'w') as f:
    try:
        while True:
            pokemon_name = pb.pokemon(pokemon_number).name
            f.write("{}\n".format(pokemon_name))
            print("Wrote {} to file".format(pokemon_name))
            pokemon_number += 1
    except ValueError:
>>>>>>> 1d31ab3da431678da55a73cdf6d4a425d5cb1ee1
        print("Done writing to file.")