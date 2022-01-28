import argparse

# input all keywords
# start capital letter
# generate password file
output = []


def main():
    # read all keywords
    input_keywords = []

    print("Enter firstname of target")
    firstname = input()
    input_keywords.append(firstname)

    print("Enter lastname of target:")
    lastname = input()
    input_keywords.append(lastname)

    print("Year of birth:")
    year = input()
    input_keywords.append(year)

    print("Month of birth:")
    newInput = input()
    input_keywords.append(newInput)

    while newInput != "":
        print("Next keyword:")
        newInput = input()
        input_keywords.append(newInput)

    # password pattern
    firstname = firstname.lower()
    lastname = lastname.lower()
    if len(year) == 4:
        input_keywords.append(year[2:])

    guess_numbers = ["0", "1", "2", "3", year, year[2:]]
    guess_special_char = ["!", ".", "_", "-"]

    if special_char:
        # use special chars between keywords
        for spec_char in guess_special_char:
            for number in guess_numbers:
                addToList(firstname + spec_char)
                addToList(lastname + spec_char)
                addToList(spec_char + firstname)
                addToList(spec_char + lastname)

                addToList(firstname + spec_char + number)
                addToList(lastname + spec_char + number)

            addToList(firstname + lastname + spec_char)
            addToList(lastname + firstname + spec_char)

            for number in guess_numbers:
                addToList(firstname + lastname + spec_char + number)
                addToList(lastname + firstname + spec_char + number)

            addToList(firstname + lastname)
            addToList(lastname + firstname)

            addToList(firstname + spec_char + lastname)
            addToList(lastname + spec_char + firstname)

            for number in guess_numbers:
                addToList(firstname + spec_char + lastname + number)
                addToList(lastname + spec_char + firstname + number)
    else:
        # simple combinations without special chars
        addToList(firstname)
        addToList(lastname)
        addToList(firstname + lastname)
        addToList(lastname + firstname)

        for number in guess_numbers:
            addToList(firstname + number)
            addToList(lastname + number)
            addToList(firstname + lastname + number)
            addToList(lastname + firstname + number)

        addToList(startCapitalLetter(firstname) + startCapitalLetter(lastname))
        addToList(startCapitalLetter(lastname) + startCapitalLetter(firstname))

        for number in guess_numbers:
            addToList(
                startCapitalLetter(firstname) + startCapitalLetter(lastname) + number
            )
            addToList(
                startCapitalLetter(lastname) + startCapitalLetter(firstname) + number
            )

    # remove the last emtpy keyword
    input_keywords = input_keywords[:-1]

    # add all keyword combinations
    for keyword in input_keywords:
        keyword = keyword.lower()
        addToList(keyword)
        addToList(startCapitalLetter(keyword))

        for number in guess_numbers:
            addToList(keyword + number)
            addToList(startCapitalLetter(keyword) + number)
            addToList(number + keyword)
            addToList(number + startCapitalLetter(keyword))

        for keyword_2 in input_keywords:
            keyword = keyword.lower()
            if keyword == keyword_2:
                # keyword 1 and 2 are the same
                continue
            else:
                addToList(keyword + keyword_2)
                addToList(keyword_2 + keyword)
                addToList(startCapitalLetter(keyword) + startCapitalLetter(keyword_2))
                addToList(startCapitalLetter(keyword_2) + startCapitalLetter(keyword))

                if special_char:
                    for spec_char in guess_special_char:
                        addToList(keyword + keyword_2 + spec_char)
                        addToList(keyword_2 + keyword + spec_char)
                        addToList(
                            startCapitalLetter(keyword)
                            + startCapitalLetter(keyword_2)
                            + spec_char
                        )
                        addToList(
                            startCapitalLetter(keyword_2)
                            + startCapitalLetter(keyword)
                            + spec_char
                        )

                        addToList(keyword + keyword_2)
                        addToList(keyword_2 + keyword)
                        addToList(
                            startCapitalLetter(keyword)
                            + startCapitalLetter(keyword_2)
                        )
                        addToList(
                            startCapitalLetter(keyword_2)
                            + startCapitalLetter(keyword)
                        )
                else:
                    for number in guess_numbers:
                        addToList(keyword + keyword_2 + number)
                        addToList(keyword_2 + keyword + number)
                        addToList(
                            startCapitalLetter(keyword)
                            + startCapitalLetter(keyword_2)
                            + number
                        )
                        addToList(
                            startCapitalLetter(keyword_2)
                            + startCapitalLetter(keyword)
                            + number
                        )

                        addToList(keyword + number + keyword_2)
                        addToList(keyword_2 + number + keyword)
                        addToList(
                            startCapitalLetter(keyword)
                            + number
                            + startCapitalLetter(keyword_2)
                        )
                        addToList(
                            startCapitalLetter(keyword_2)
                            + number
                            + startCapitalLetter(keyword)
                        )

def addToList(string):
    # generate password file
    if string not in output:
        print(string)
        f = open(output_file, "a")
        f.write(string + "\n")
        f.close()
        output.append(string)

def startCapitalLetter(string):
    # start capital letter
    return string.capitalize()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate password list based on target inputs."
    )
    parser.add_argument(
        "-o", type=str, default="./passwords.txt", help="Path to output file"
    )
    parser.add_argument(
        "-special", type=bool, default=False, help="Add special characters"
    )
    args = parser.parse_args()
    output_file = args.o
    special_char = args.special
    main()