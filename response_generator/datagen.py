from names import FIRST, LAST
from random import choice, randint
import pandas as pd

SCOPE_TEAMS = [
        "New Balance Press",
        "New Balance Stitch",
        "Accelerate Wind",
        "Blue Origin",
        "BU Wise",
        "Linevision",
        "Santos Volpe",
        "Microsoft NERD",
        "Mass EEC",
        "Moderna",
        "Pfizer",
        "Amazon Robotics",
        "Boston Scientific",
]

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

