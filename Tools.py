import random


def get_input(prompt, acceptable_answers):
    print(prompt)
    for c, ans_c in enumerate(acceptable_answers):
        print(str(c + 1), end="")
        print(": ", end="")
        print(ans_c)
    print("")
    res = input("")

    try:
        within_range = 1 <= int(res) <= len(acceptable_answers)

        if not within_range:
            raise IndexError

        res = acceptable_answers[int(res) - 1]

    except ValueError:
        print("Please enter a number between 1 and " + str(len(acceptable_answers)), end="\n\n")
        return get_input(prompt, acceptable_answers)
    except IndexError:
        print("Your number was out of range.")
        print("Please enter a number between 1 and " + str(len(acceptable_answers)), end="\n\n")
        return get_input(prompt, acceptable_answers)

    return res


# heads is true
def coin_toss():
    flip = random.randint(0, 1)
    if flip == 0:
        return True
    else:
        return False
