from names import FIRST, LAST, SCOPE_TEAMS
from random import choice, randint
import pandas as pd

RESPONSES = 65

def new_response():
    row = []
    row.append(choice(FIRST) + " " + choice(LAST))
    for _ in SCOPE_TEAMS:
        row.append(randint(1, 5))
    return row

def main():
    data = [new_response() for _ in range(RESPONSES)]
    cols = ["Name"] + SCOPE_TEAMS
    df = pd.DataFrame(data, columns=cols)
    df.to_csv('../responses.csv', index=False)



if __name__ == "__main__":
    main()

