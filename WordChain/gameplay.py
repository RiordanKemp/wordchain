from pickle import EMPTY_DICT

openingStr = """Welcome to NAME PENDING (word chain??)!"""
difficultyDetails = "\nHard Mode requires child words to be +-1 in length relative to their parent."
hardmodeEnabled = "\nYou've chosen to play on Hard Mode.  Hard Mode requires child words to be +-1 in length relative to their parent."
exitMessage = "Thanks for playing! Exiting now..."
reset_message = "Resetting the round now.."
word_doesnt_exist_error = "This word does not exist."

difficultyOn = False

directory_str = "dict_directory"

alphabet_dict = {}
words_dict = {}
numb_dict = {}
starting_words_set = set()
already_used_words_set = set()
valid_letters_dict = {}

import os
import os.path
import re
import csv
import random
from operator import itemgetter


#Dictionary CSV file: https://www.bragitoff.com/2016/03/english-dictionary-in-csv-format/

def difficulty():
    hardmodeBool = False
    input_difficulty = input("\nDo you want to play Hard Mode? (Y = Yes, 0 = Details, Other = No)")

    while (input_difficulty == "0"):
        print(difficultyDetails)
        input_difficulty = input("\nDo you want to play Hard Mode? (Y = Yes, 0 = Details, Other = No)")

    if (input_difficulty.lower() == "y"):
        hardmodeBool = True
        print(hardmodeEnabled)

    return hardmodeBool


def open_files():
    readers_list = []

    for file in os.listdir(directory_str):
        filename = os.fsdecode(file)

        file_path = os.path.join(directory_str, filename)
        file_reader = open(file_path, 'r')
        csv_reader = csv.reader(file_reader)
        readers_list.append(csv_reader)

    return readers_list


def organize_dictionary(filereader_list):


    for reader in filereader_list:
        line_count = 0
        for line in reader:
            line_count += 1

            if (line_count == 1):
                line_str = ' '.join(line)
                letter_key = line_str[0]
                #print("line str:", line_str, "line:", line)
                #print("line_str[0]:", line_str[0])
                #print("letter key:", letter_key)

            if (line_count % 2 == 1 and line_count != 1):
                line_str = ' '.join(line)
                split_line = line_str.split()
                word_key = split_line[0]
                word_key = re.sub(r'[^a-zA-Z0-9]', '', word_key)
                word_def = ' '.join(split_line[1::])
                word_addition(word_key, word_def, letter_key)


def word_addition(word_key, word_def, letter_key):
    if len(word_key) < 3:
        return

    if letter_key not in alphabet_dict:
        alphabet_dict[letter_key] = words_dict

    if word_key not in alphabet_dict[letter_key]:
        alphabet_dict[letter_key][word_key] = word_def

    else:
        marked_def = "1581199358571" + word_def
        alphabet_dict[letter_key][word_key] += marked_def
        numb_dict[word_key] = 1

    if len(word_key) > 8:
        starting_words_set.add(word_key)


def first_word(parent_word, difficultyOn):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nINITIAL WORD\nParent: {}".format(parent_word))
    input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")

    while input_str != "0":
        input_str = input_str.capitalize()

        if input_str == "0":
            break

        if input_str not in words_dict:
            print(word_doesnt_exist_error)
            input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")
            continue

        if input_str in already_used_words_set:
            print("You already used this word.")
            input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")
            continue

        letter_use_dict = {}
        character_limit_exceeded = False
        invalid_character_used = False
        overused_letter = ""
        invalid_character = ""

        for letter in valid_letters_dict:
            letter_use_dict[letter] = valid_letters_dict[letter]

        for character in input_str:
            character = character.lower()
            if character not in valid_letters_dict:
                invalid_character_used = True
                invalid_character = character
                break
            letter_use_dict[character] -= 1
            if (letter_use_dict[character] < 0):
                character_limit_exceeded = True
                overused_letter = character

        if (invalid_character):
            print("You used letter {}, which is not part of the parent word.".format(invalid_character))
            input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")
            continue

        if (character_limit_exceeded):
            overuse_count = valid_letters_dict[letter] - letter_use_dict[character]
            print("You used the letter {}, but the maximum is {}.".format(overused_letter, overuse_count, valid_letters_dict[letter]))
            input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")
            continue

        input_length = len(input_str)
        parent_length = len(parent_word)
        different_length = parent_length - input_length
        if (different_length > 1 or different_length < -1) and difficultyOn:
            print("This word should have {} to {} characters, but it has {} instead.".format(parent_length - 1, parent_length + 1, input_length))
            input_str = input("\nConstruct a word using only letters from the Parent Word, or 0 + ENTER to reset the round:")
            continue

        already_used_words_set.add(input_str)
        return input_str

    return 0






def child_word(parent_word, previous_word, difficultyOn):


    starting_letter = previous_word[-1].capitalize()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nCHILD WORD\nParent: {}\nPREVIOUS: {}".format(parent_word, previous_word))
    input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))

    while input_str != "0":
        input_str = input_str.capitalize()

        if input_str == "0":
            break

        if input_str not in words_dict:
            print(word_doesnt_exist_error)
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue

        if input_str in already_used_words_set:
            print("You already used this word.")
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue

        letter_use_dict = {}
        character_limit_exceeded = False
        invalid_character_used = False
        overused_letter = ""
        invalid_character = ""

        for letter in valid_letters_dict:
            letter_use_dict[letter] = valid_letters_dict[letter]

        for character in input_str:
            character = character.lower()
            if character not in valid_letters_dict:
                invalid_character_used = True
                invalid_character = character
                break
            letter_use_dict[character] -= 1
            if (letter_use_dict[character] < 0):
                character_limit_exceeded = True
                overused_letter = character

        if (invalid_character):
            print("You used letter {}, which is not part of the parent word.".format(invalid_character))
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue

        if (character_limit_exceeded):
            overuse_count = valid_letters_dict[letter] - letter_use_dict[character]
            print("You used the letter {}, but the maximum is {}.".format(overused_letter, overuse_count, valid_letters_dict[letter]))
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue

        input_length = len(input_str)
        parent_length = len(parent_word)
        different_length = parent_length - input_length
        if (different_length > 1 or different_length < -1) and difficultyOn:
            print("This word should have {} to {} characters, but it has {} instead.".format(parent_length - 1, parent_length + 1, input_length))
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue

        if (input_str[0] != starting_letter):
            print("This word should start with {}, but it starts with {} instead.".format(starting_letter, input_str[0]))
            input_str = input("\nConstruct a word using only letters from the Parent Word and starting with {}, or 0 + ENTER to end the round:".format(starting_letter))
            continue


        already_used_words_set.add(input_str)

        return "1", input_str
    return "0", input_str

def main():

    print(openingStr)
    input_play = input("\nDo you want to play a game of NAME PENDING? (yes/no):")
    if input_play.lower() == "no":
        print(exitMessage)
        return

    while input_play.lower() != "no":

        starting_words_set.clear()
        valid_letters_dict.clear()
        already_used_words_set.clear()

        alphabet_dict.clear()
        words_dict.clear()
        numb_dict.clear()

        difficultyOn = difficulty()

        readers_list = open_files()

        organize_dictionary(readers_list)

        parent_word = random.choice(list(starting_words_set))

        while True:
            input_str = input("You may choose a Parent Word for this round.  Press ENTER to choose randomly instead:")

            if input_str == "":
                break

            if input_str.capitalize() not in words_dict:
                print(word_doesnt_exist_error)
                continue

            else:
                parent_word = input_str.capitalize()
                break

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nThis round's PARENT WORD will be: {}.".format(parent_word))
        for character in parent_word:
            character = character.lower()
            if character not in valid_letters_dict:
                valid_letters_dict[character] = 0
            valid_letters_dict[character] += 1

        already_used_words_set.add(parent_word)

        letter = parent_word[0]
        definition = alphabet_dict[letter][parent_word]

        if parent_word in numb_dict.keys():
            definition = definition.split('1581199358571')
            definition = '\n '.join(definition)
            print("This word has multiple definitions:\n", definition)

        else:
            print("This word has one definition:\n", definition)

        input("\nPress ENTER to continue.")

        initial_word = first_word(parent_word, difficultyOn)
        if (initial_word == 0):
            print(reset_message)
            continue

        word_chain = []
        word_chain_length = 1
        word_chain.append(initial_word)

        run_int, prior_word = child_word(parent_word,initial_word, difficultyOn)
        if run_int == "1":
            word_chain_length += 1
            word_chain.append(prior_word)

        while run_int == "1":
            run_int, prior_word = child_word(parent_word, prior_word, difficultyOn)
            if run_int == "1":
                word_chain_length += 1
                word_chain.append(prior_word)

        word_chain_str = "---".join(word_chain)
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nYour Word Chain: {}\nLength: {}".format(word_chain_str, len(word_chain)))

        input_play = input("\nDo you want to play another round of NAME PENDING? (yes/no):")
        if input_play.lower() == "no":
            print(exitMessage)
            return

main()




