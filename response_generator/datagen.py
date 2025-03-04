from names import FIRST, LAST, SCOPE_TEAMS
from random import choice, randint
import pandas as pd

RESPONSES = 65
NAMES = [choice(FIRST) + " " + choice(LAST) for  _ in range(RESPONSES)]

def new_response(name):
    row = []
    row.append(name)

    # Team preferences (random)
    for _ in SCOPE_TEAMS:
        row.append(randint(1, 5))

    # add 0-2 Antipreferences (random)
    antiprefs = []
    for _ in range(randint(0, 2)):
        to_add = choice(NAMES)
        while to_add in antiprefs or to_add == name:
            to_add = choice(NAMES)
        antiprefs.append(to_add)

    row.append(tuple(antiprefs))



    return row

def main():
    data = [new_response(name) for name in NAMES]
    cols = ["Name"] + SCOPE_TEAMS + ["Antipreferences"]
    df = pd.DataFrame(data, columns=cols)
    df.to_json('responses.json')

if __name__ == "__main__":
    main()

