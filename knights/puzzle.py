from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

players = ["A", "B", "C"]

# Base Rules for game
# All players must be either a Knight or a Knave, but not both
base_rules = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)

knowledge0 = And(
    base_rules,

    # if the sentence is truthful, A is a Knight
    Biconditional(sentence0, AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1 = And(AKnave, BKnave)

knowledge1 = And(
    base_rules,
    # if the sentence is truthful, A is a Knight
    Biconditional(sentence0, AKnight)
)

# Puzzle 2
# A says "We are the same kind."
sentence2a = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave),
)
# B says "We are of different kinds."
sentence2b = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight),
)

knowledge2 = And(
    base_rules,

    # If A is truthful, A is a knight
    Implication(
        sentence2a,
        AKnight,
    ),

    # If B is truthful, B is a knight
    Implication(
        sentence2b,
        BKnight,
    )

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentence3a = Or(AKnight, AKnave)

# B says "A said 'I am a knave'."
sentence3b1 = AKnave

# B says "C is a knave."
sentence3b2 = CKnave

# C says "A is a knight."
sentence3c = AKnight


knowledge3 = And(
    base_rules,

    # If A is truthful, A is a Knight
    Implication(sentence3a, AKnight),

    # If both of B's statements are trutuful, B is a Knight
    Implication(
        And(sentence3b1, sentence3b2),
        BKnight
    ),

    # If C is truthful, C is a knight
    Implication(
        sentence3c, CKnight
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
