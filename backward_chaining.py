from production import AND, OR, IF, THEN, match, populate, simplify, pretty_goal_tree
pokemon_rules = [

    IF(
        AND(
            "(?x) is fire type",
            "(?y) is grass type"
        ),
        THEN("(?x) has advantage over (?y)")
    ),

    IF(
        AND(
            "(?x) is water type",
            "(?y) is fire type"
        ),
        THEN("(?x) has advantage over (?y)")
    ),

    IF(
        AND(
            "(?x) is electric type",
            "(?y) is water type"
        ),
        THEN("(?x) has advantage over (?y)")
    )
]

pokemon_facts = [
    "charizard is fire type",
    "venusaur is grass type",
    "blastoise is water type",
    "pikachu is electric type",
    "gyarados is water type"
]


def backchain_to_goal_tree(rules, hypothesis):
    goals = [hypothesis]

    for rule in rules:
        conclusion = rule.consequent()

        bindings = match(conclusion, hypothesis)

        if bindings is None:
            continue

        antecedent = rule.antecedent()

        if isinstance(antecedent, AND):
            subgoals = []

            for part in antecedent:
                new_hypothesis = populate(part, bindings)

                subgoals.append(
                    backchain_to_goal_tree(
                        rules,
                        new_hypothesis
                    )
                )

            goals.append(AND(subgoals))

        elif isinstance(antecedent, OR):
            subgoals = []

            for part in antecedent:
                new_hypothesis = populate(part, bindings)

                subgoals.append(
                    backchain_to_goal_tree(
                        rules,
                        new_hypothesis
                    )
                )

            goals.append(OR(subgoals))

        else:
            new_hypothesis = populate(
                antecedent,
                bindings
            )

            goals.append(
                backchain_to_goal_tree(
                    rules,
                    new_hypothesis
                )
            )

    return simplify(OR(goals))


print("Goal tree for Charizard vs Venusaur:")
print(
    backchain_to_goal_tree(
        pokemon_rules,
        "charizard has advantage over venusaur"
    )
)

print()

print("Goal tree for Pikachu vs Gyarados:")
print(
    backchain_to_goal_tree(
        pokemon_rules,
        "pikachu has advantage over gyarados"
    )
)