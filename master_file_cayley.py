import time, os, psutil, networkx as nx, pickle
# import matplotlib.pyplot as plt
from graphviz import Digraph
process = psutil.Process(os.getpid())


class Letter:
    def __init__(self, _symbol, _exponent=0):
        # this is the construction of the class of Letter which is
        # essentially the cornerstone of all of this as homomorphisms,
        # Words, and Groups will all be made up in some way of Letters.
        # _symbol explains what the character will be and exponent will
        # denote if it is the inverse or not (here represented with
        # capitalization).
        # If I'm referencing the class Letter the L will be capitalized.

        # sets the Letter's
        if len(_symbol) != 1:
            raise Exception("I only take letters with length one")
        self._symbol = _symbol.lower()

        # decides the Letter's exponent or case
        if _symbol == _symbol.upper():
            exponent_check = -1
        else:
            exponent_check = 1
        if _exponent == 0:
            _exponent = exponent_check
        if abs(_exponent) != 1:
            raise Exception("only -1/1 for exponent")

        self._exponent = _exponent

        # these are my training wheels
        self._paranoid = True

    def get_str(self):
        # this returns the Letter as a string i.e. a or A
        if self._exponent == 1:
            self_str = self._symbol
        else:
            self_str = self._symbol.upper()
        return self_str

    def __eq__(self, other):
        # this lets me test if two Letter objects are representing
        # the same thing
        if self._paranoid:
            if not isinstance(other, Letter):
                raise Exception("comparing apples and oranges here pal")

        self_str = self.get_str()
        othr_str = other.get_str()
        return self_str.__eq__(othr_str)

    def __hash__(self):
        # this turns the Letter into a hashable datatype by returning the
        # string version
        self_str = self.get_str()
        return self_str.__hash__()

    def __str__(self):
        # this allows the letter to be called by the print function and return
        # the actual string representation rather than the Letter object
        self_str = self.get_str()
        return self_str

    def check_cancels(self, a_letter):
        # if a Letter cancels with another, they have to have the same symbol, but
        # opposite exponents. This checks that and returns true or false
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("a letter can't cancel with "
                                "something that's not a letter")

        if self._symbol == a_letter._symbol:
            return self._exponent != a_letter._exponent
        return False

    def check_capital(self):
        # this checks if the Letter is an inverse or not and returns true or false
        return self._exponent == -1

    def return_inv_letter(self):
        # this returns a Letter's inverse without changing the Letter itself.
        inv_letter = Letter(self._symbol, self._exponent * -1)
        return inv_letter


class Word:
    def __init__(self, a_list=[]):
        # a Word is an object which consists of a list of Letters
        # whenever I am referring to an object which is of the class
        # Word in comments I'll capitalize the first letter. when
        # I am referencing variables, if I expect it to be a word I will
        # label it as a_word to differentiate from a_str or a_list
        # when a new word is created I will call it that or something more
        # specific to its importance. i.e. inv_word = inverse word

        for entry in a_list:
            if not isinstance(entry, Letter):
                raise Exception("I only add letters")

        self._list = a_list

        # yep, the training wheels are everywhere
        self._paranoid = True

    def return_word_str(self):
        # returns the Word's list of Letters as just a string
        word_str = ""
        for entry in self._list:
            word_str = word_str + entry.get_str()
        return word_str

    def return_str_list(self):
        # returns the Word's list of Letters as a list of strings
        word_list = []
        for entry in self._list:
            word_list.append(entry.get_str())
        return word_list

    def return_letter_list(self):
        word_list = []
        for entry in self._list:
            word_list.append(entry)
        return word_list

    def __eq__(self, other):
        # this allows two Words to be compared to see if they are the same
        # string. Ordinarily, the class stores both as separate data instances
        # so this just allows them to be tested if they represent the same data
        self_str = self.return_word_str()
        othr_str = other.return_word_str()
        return self_str.__eq__(othr_str)

    def __hash__(self):
        # this returns the word as a hashable object as instances of classes
        # are not ordinarily hashable objects
        self_str = self.return_word_str()
        return self_str.__hash__()

    def __str__(self):
        # this allows the word to be printed when the print function is called,
        # which makes testing if the results are accurate easier
        self_str = self.return_word_str()
        return self_str.__str__()

    def add_word(self, a_word):
        # this takes a Word and adds a second Word to the end of it
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("I only add words")
        self._list.extend(a_word._list)

    def add_str(self, a_str):
        # this takes a Word and converts each character into a Letter before adding
        # it to the Word's list of Letters
        if self._paranoid:
            if not isinstance(a_str, str):
                raise Exception("This isn't a string")
        for character in a_str:
            letter = Letter(character)
            self._list.append(letter)

    def add_letter(self, a_letter):
        # this takes a Word and adds a Letter to the list of Letters
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("who are you trying to fool, not a letter")
        self._list.append(a_letter)

    def return_word_len(self):
        # this returns an integer which is the length of the Word, or number of
        # entries in the Word's list
        length_int = len(self._list)
        if self._paranoid:
            if not isinstance(length_int, int):
                raise Exception("what did you do? why is len not returning a number")
        return length_int

    def return_inv_word(self):
        # this returns an inverse Word, which would be changing all
        # cases to the inverse and reversing the list. I.e. aBAb's inverse is BabA
        inv_word = Word([])
        for a_letter in self._list:
            inv_word._list.append(a_letter.return_inv_letter())
        inv_word._list.reverse()
        return inv_word

    def return_word_letter(self, i):
        # this returns the 'i'th letter in the Word
        if self._paranoid:
            if not isinstance(i, int):
                raise Exception("how am i supposed to count when you're not giving me numbers")
        word_letter = self._list[i]
        return word_letter

    def return_reverse(self):
        # this returns a Word who's order has been reversed, but the tenses not changed
        # this becomes useful when adding Words that reduce to the empty word, but can't
        # just be run through the return_inv_word ie. aA = Aa
        reverse_word = Word([])
        reverse_word.add_word(self)
        reverse_word._list.reverse()
        return reverse_word

    def set_reduced(self):
        # this takes a Word and sets it to its reduced form, or eliminates all
        # instances of a Letter being next to its inverse by eliminating both the
        # Letter and the inverse. i.e. AbbaABa eventually eliminates to Aba
        if self.return_word_len() <= 0:
            return self
        for i in range(self.return_word_len() - 1):
            a_letter = self._list[i]
            next_letter = self._list[i + 1]
            if a_letter.check_cancels(next_letter):
                del self._list[i + 1]
                del self._list[i]
                return self.set_reduced()
        return self

    def return_word_multiplication(self, a_word):
        # this takes two Words and adds them together and then reduces the combination
        # of the two Words. it also does so without altering either Word so those pieces
        # of data still exist
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("not a word, homes")

        multiplied_word = Word()
        multiplied_word.add_word(self)
        multiplied_word.add_word(a_word)

        multiplied_word.set_reduced()
        return multiplied_word

    def check_identity(self):
        # when we move on to Groups, we don't reduce, but instead we allow Words
        # such as aA in order to construct properly the non reduced Words of the
        # Free Group. This checks if it is an instance of one of those reducible
        # Words.
        # we use a test Word as we don't want to reduce the actual Word

        test_word = Word([])
        test_word.add_word(self)
        test_word.set_reduced()
        if test_word.return_word_len() == 0:
            return True
        return False


class Hom:
    def __init__(self, a_dict={}):
        # this is the constructor for a Homomorphism. This has been organized as a
        # dictionary in this language. It is the best data structure for telling me
        # "a" maps to "ab"
        self._dict = {}

        for key, item in a_dict:
            if not isinstance(key, Letter):
                raise Exception("not a letter, my dude")
            if not isinstance(item, Word):
                raise Exception("can't map to something that's not a word")

            self._dict[key] = item

        # training wheels are best for everyone
        self._paranoid = True

    def add_entry(self, a_letter, a_word):
        # this will add another entry to the dictionary or homomorphism that only accepts
        # a Letter going to a Word
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("not a letter, friend. i only add letters")
            if not isinstance(a_word, Word):
                raise Exception("not a word, and i only work with words, pal")
            for key in self._dict.keys():
                if a_letter == key:
                    print("well, you're writing over another entry with " + a_letter.get_str()
                          + " but i guess that's ok, just be wary")

        self._dict.update({a_letter: a_word})

    def return_str_dict(self):
        # this will return a dictionary that is equivalent to the homomorphism but with
        # strings instead of Letter and Word objects
        str_dict = {}
        for key, items in self._dict.items():
            letter_string = key.get_str()
            word_string = items.return_word_str()
            str_dict[letter_string] = word_string
        return str_dict

    def call_entry(self, a_letter):
        # this returns the Word that corresponds to the Letter in the homomorphism.
        # If the Letter inputted is the inverse of the letter in the homomorphism, it will
        # output the inverse word. i.e. a => ab, A => BA
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("I only can call Letters, bud")

        for key, a_word in self._dict.items():
            if a_letter == key:
                if a_letter.check_capital():
                    return a_word.return_inv_word()
                return a_word

    def check_keys(self, a_letter):
        # this checks to see if a Letter is one of the keys to the dictionary, or if
        # this homomorphism sends a certain character to a specific Word, or just itself
        if self._paranoid:
            if not isinstance(a_letter, Letter):
                raise Exception("not a letter, and i only do letters")
        for key in self._dict.keys():
            if a_letter == key:
                return True
        return False

    def return_word_application(self, a_word):
        # this takes a Word as its input and transforms it according to the rules of the
        # homomorphism. if a Letter exists in the word, but not in the homomorphism it sends
        # the letter to itself. This also returns a new word, so the original isn't changed
        hom_applied_word = Word()
        for i in range(a_word.return_word_len()):
            word_letter = a_word.return_word_letter(i)
            if self.check_keys(word_letter):
                hom_entry = self.call_entry(word_letter)
                for character in hom_entry.return_str_list():
                    letter = Letter(character)
                    hom_applied_word.add_letter(letter)
            else:
                hom_applied_word.add_letter(word_letter)

        return hom_applied_word


class WordTrie:
    def __init__(self):
        # a Trie (which is like an attempt not a plant) is a data
        # structure that lets me store things in a series of dictionaries
        # that can then be searched. For my purposes, it serves as an easily
        # searchable list (although it's not really that) which will be used
        # to store cosets of different Words

        self.root = dict()
        self._paranoid = True

    def add_word(self, word):
        # seeing as the Trie doesn't allow for any Words to be saved to it in
        # its creation, all Words must be added to it after the fact. add_Word
        # allows for one Word to be added at a time, there are other methods for
        # adding lists of Words, but considering we're using iterables, it seemed
        # like a good idea to include one that just adds a single Word
        entry = self.root
        if self._paranoid:
            if not isinstance(word, Word):
                raise Exception("Not a word")
        word_list = word.return_letter_list()
        for letter in word_list:
            entry = entry.setdefault(letter, {})
        entry.setdefault("__")

    # doesn't work in the word version
    # def print_trie(self):
    #     entry = self.root
    #     for items in entry:
    #         print(entry)
    #         entry = entry[items]

    def search_trie(self, word):
        # this allows the user to search the Trie and establish whether
        # an entry exists. This has a good function either for seeing if something
        # is equal to any entry in the Trie OR if an entry already exists.
        if self._paranoid:
            if not isinstance(word, Word):
                raise Exception("I can only search for WORDS in my Trie of WORDS")
        entry = self.root
        for letter in word.return_letter_list():
            if letter not in entry:
                return False
            entry = entry[letter]
        if "__" in entry:
            return True
        return False

    def add_word_list(self, word_list: list):
        # this allows for a list of words to be added to a Trie at once
        # rather than calling add_Word half a hundred times.
        if self._paranoid:
            if not isinstance(word_list, list):
                raise Exception("this has to be a list")
            for entry in word_list:
                if not isinstance(entry, Word):
                    raise Exception("and it has to be a list of WORDS")

        for word in word_list:
            self.add_word(word)


class Cache:
    def __init__(self, key_list: list):
        # the purpose of cache is to take the yielded cosets of different
        # Words and store them in one place so as to not have to generate
        # the entire coset again. It does this by creating a dictionary of
        # Words to their Tries which store the cosets.

        self._dict = {}
        self._paranoid = True
        self._bool_dict = {}
        self._dict_list = {}

        if self._paranoid:
            for entry in key_list:
                if not isinstance(entry, Word):
                    raise Exception("all my keys are words, guy")

        for i in range(len(key_list)):
            a_word = key_list[i]
            a_word_trie = WordTrie()
            a_word_trie.add_word(a_word)
            self._dict[a_word] = a_word_trie
            self._bool_dict[a_word] = False
            self._dict_list[a_word] = [a_word]

    def create_coset(self, a_word):
        # this allows for a new coset (or Trie, as it is being stored here)
        # to be added to the Cache. it does so by checking if a Word is already
        # in the Cache. if not, then a new coset is added.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("i only use words as keys, pal")
            for key in self._dict.keys():
                if key == a_word:
                    raise Exception("I'm not making you a coset, you already have one")

        a_word_trie = WordTrie()
        a_word_trie.add_word(a_word)
        self._dict[a_word] = a_word_trie
        self._bool_dict[a_word] = False
        self._dict_list[a_word] = [a_word]

    def add_to_coset(self, a_word, a_word_equiv):
        # this takes a Word and searches for it in the keys. If it is in the
        # keys then it will add the word equivalent to the trie that is
        # associated with it. It does this by searching the cache for the Word,
        # finding the trie, and adding the word to it.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("i can only search for words")
            if not isinstance(a_word_equiv, Word):
                raise Exception("I'm only adding words to this Trie")
            check = False
            for key in self._dict.keys():
                if a_word == key:
                    check = True
                    break
            if not check:
                raise Exception("this word doesn't have a Trie yet")

        for key in self._dict.keys():
            if key == a_word:
                self._dict[key].add_word(a_word_equiv)
                self._dict_list[key].append(a_word_equiv)
                self._bool_dict[key] = False

    def check_complete(self, a_word):
        # this checks if a coset has been completed. It essentially forces the
        # user to mark a coset complete and if a Word's equivalent is added, the
        # complete check is put back to false to ensure that the user is consciously
        # adding an equivalent word to the Trie.
        for key in self._bool_dict.keys():
            if key == a_word:
                return self._bool_dict[key]

    def mark_coset_complete(self, a_word):
        # this is the method that allows the user to set a coset as complete
        for key in self._bool_dict.keys():
            if key == a_word:
                self._bool_dict[key] = True

    def check_key(self, a_word):
        # this can be used to check that a word is even in the cache before
        # things are called upon
        for key in self._dict.keys():
            if key == a_word:
                return True
        return False

    def get_coset_trie(self, a_word):
        # this calls forth the coset in case it ever needs to be referenced
        # or set to a variable which would be easier than typing the whole thing
        # out over and over again.
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("only words homes")
            check = False
            for key in self._dict.keys():
                if a_word == key:
                    check = True
                    break

            if not check:
                raise Exception("not in the keys, pal. add it and try again")

        return self._dict[a_word]

    def get_coset_list(self, a_word):
        # this is made to generate a list of all of the entries so that the entries
        # of the list can be yielded one at a time
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("words, bruv, words. how many times...")
        for key in self._dict_list.keys():
            if a_word == key:
                return self._dict_list[key]


class StringTrie:
    def __init__(self):
        self.root = dict()

    def add_str(self, a_str):
        entry = self.root
        for char in a_str:
            entry = entry.setdefault(char, {})
        entry.setdefault("__")

    def print_trie(self):
        entry = self.root
        for items in entry:
            print(entry)
            entry = entry[items]

    def search_trie(self, a_str):
        entry = self.root
        for char in a_str:
            if char not in entry:
                return False
            entry = entry[char]
        if "__" in entry:
            return True
        return False

    def add_str_list(self, word_list: list):
        for entry in word_list:
            self.add_str(entry)


class NewGroup:
    def __init__(self, generator_list, relator_list, upper_limit):
        construction_start = time.time()
        # here is the construction of the class Group. Each Group must have
        # a list of generators and a list of relators. Unlike the other classes
        # I didn't design methods to add generators or relators after the initial
        # construction of the class. As the name specifies, this version of Group
        # uses iterable functions (generators) to yield a value. This frees up
        # space as an entire list need not be created if the first values suffices.
        # The generators must all be Letters and the relators Words.
        self._generator_list = []
        self._relator_list = []
        self._relator_len_list = []
        self._relator_len_max = 0
        self._relator_len_min = 0

        # this feels like putting training wheels on a 747 but maybe that's what
        # 747s need. after all, crashing a 747 is worse than crashing a bike
        self._paranoid = True

        for entry in generator_list:
            if not isinstance(entry, Letter):
                raise Exception("noooo")
            self._generator_list.append(entry)
            if entry.return_inv_letter() not in self._generator_list:
                self._generator_list.append(entry.return_inv_letter())

        for entry in relator_list:
            if not isinstance(entry, Word):
                raise Exception("...i don't know what to say anymore")
            for i in range(entry.return_word_len()):
                if entry.return_word_letter(i) not in self._generator_list:
                    raise Exception("i'm not working with relators that "
                                    "don't send to my generators, sorry pal")
            self._relator_list.append(entry)
            self._relator_len_list.append(entry.return_word_len())

        for entry in self._relator_list:
            if entry.return_inv_word() not in self._relator_list:
                self._relator_list.append(entry.return_inv_word())
            if entry.return_reverse() not in self._relator_list:
                self._relator_list.append(entry.return_reverse())

        # Instead of doing cache stuff here, I'm going to create a trie here that
        # will be the normal closure of the relators.
        self._upper_limit = upper_limit
        self._ncor = WordTrie()
        identity = Word([])
        for entry in self.yield_coset_new(identity, self._upper_limit):
            self._ncor.add_word(entry)

        print("construction time: % s seconds \n" % (round(time.time() - construction_start, 3)))
        # print(process.memory_info().rss / 10 ** 6)

    def yield_coset_new(self, a_word, max_length):
        # this function creates a generator that will spit out the next item
        # which is equivalent to the inputted word. It accomplishes this by
        # inserting the relators in every possible position in the Word, and
        # yields that word. Once it goes through all positions and relators,
        # it goes through the previously yielded Words and runs on them.
        # it stores them in a list local to the function. It was the only way
        # to prevent duplicates from coming up
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("I'm gonna lose it. words only")
            if not isinstance(max_length, int):
                raise Exception("we're working with math and you can't tell "
                                "me an integer to work with?")

        def _insert_relators(a_str, a_rule):
            # as the variable names suggest, this only takes strings as inputs.
            # Because this requires cutting up and gluing together objects, it's
            # easier to work with mutable objects than the Words or Letters
            for i in range(len(a_str)):
                if i == 0:
                    new_str = a_rule + a_str
                    yield new_str
                else:
                    head_a_str = a_str[:i]
                    tail_a_str = a_str[i:]
                    new_str = head_a_str + a_rule + tail_a_str
                    yield new_str
            new_str = a_str + a_rule
            yield new_str

        def _iterate_with_words(product_trie, word_rule_list, list_to_expand,
                                fresh_list, max_length_here):
            # As you can tell by how it is called below, this will be called until.
            # the list to expand is empty. What this means is that this process will
            # iterate until nothing is added for a full cycle through everything in the
            # fresh list. I got rid of the coset list because nothing was being done
            # with that information. This will take more memory than if I wasn't storing
            # them at all but we still need to protect against duplicates. The trie also
            # makes searching for things in it faster.
            fresh_list.clear()
            for a_fresh_word in list_to_expand:
                for a_rule in word_rule_list:
                    if not a_fresh_word.return_word_len() + a_rule.return_word_len() > max_length_here:
                        a_str = a_fresh_word.return_word_str()
                        a_rule_str = a_rule.return_word_str()
                        for new_string in _insert_relators(a_str, a_rule_str):
                            new_word = Word([])
                            new_word.add_str(new_string)
                            if not product_trie.search_trie(new_word):
                                product_trie.add_word(new_word)
                                fresh_list.append(new_word)
                                yield new_word
            list_to_expand.clear()
            list_to_expand.extend(fresh_list)

        # this takes the coset of the word and adds itself as well as the
        # list for expansion and expands it. then whenever the expansion
        # list has entries to expand, the program will run and the iterable
        # will continue to run

        coset_trie = WordTrie()
        coset_trie.add_word(a_word)
        expand_me = [a_word]
        yield a_word

        while expand_me:
            newly_added = []
            coset_producer = _iterate_with_words(coset_trie, self._relator_list,
                                                 expand_me, newly_added, max_length)
            for member in coset_producer:
                yield member

    def yield_coset_of_len(self, a_word, the_len):
        # this calls the yield coset method but only outputs them if the length is equal to
        # the length specified. so if I wanted only the members with length 3 it will output
        # only them
        if self._paranoid:
            if not isinstance(a_word, Word):
                raise Exception("not a word, homes")
            if the_len > self._upper_limit:
                raise Exception("sorry i don't yield words with lengths greater than"
                                "my upper limit")

        total_coset = self.yield_coset_new(a_word, the_len)
        for member in total_coset:
            if member.return_word_len() == the_len:
                yield member

    def yield_non_reduced_words(self, max_len):
        # the purpose of this method is to create a iterable that will hand the
        # program the members of the set of the non reduced words on the generators
        # one at a time. This saves the space of having to generate the entire list
        # similarly to how the yield coset was aimed at not creating and saving the entire
        # list of Words

        if self._paranoid:
            if max_len > self._upper_limit:
                raise Exception("sorry i don't make words with lengths greater than"
                                "my upper limit")

        def _add_generators(letter_list, product_list, new_list):
            # this takes the generators, and the list of Words which are already non-reduced
            # members, and adds the generators to the members of that list, yielding them
            # one at a time.
            new_product_list = []
            for letter in letter_list:
                for old_word in new_list:
                    non_reduced_word = Word([])
                    non_reduced_word.add_word(old_word)
                    non_reduced_word.add_letter(letter)
                    if non_reduced_word not in product_list:
                        if non_reduced_word not in new_product_list:
                            new_product_list.append(non_reduced_word)
                            yield non_reduced_word
            product_list.extend(new_product_list)
            new_list.clear()
            new_list.extend(new_product_list)

        # this then takes an empty list and runs the _add_generators. So the first iteration
        # will return the generators, and the next will return their combinations, and so on

        identity = Word([])
        non_reduced_word_list = [identity]
        fresh_list = [identity]
        for i in range(max_len):
            nrw_iterable = _add_generators(self._generator_list, non_reduced_word_list, fresh_list)
            for j in nrw_iterable:
                yield j

    def test_equals(self, word1, word2, num):
        # this takes two Words and tests if they are equals. it does so by combining a Word
        # (word1 in this case) with the second Word's inverse. The logic of this being that
        # if A = B then A*B^-1 = I where I is the identity. However, some words require more
        # than just that, so we create a iterator for the coset of this new word and test each
        # entry against a Word yielded from the normal closure of the relators. We obtain this
        # normal closure of the relators by creating a coset for the identity.
        # also i set num like that for fun, and it'll help with figuring out how long the words
        # have to be to get them to properly reduce

        if self._paranoid:
            if not isinstance(word1, Word):
                raise Exception("only words; the first one is not one")
            if not isinstance(word2, Word):
                raise Exception("still only working with words")
            if not isinstance(num, int):
                raise Exception("see earlier comment about not knowing integers")
            if num > self._upper_limit:
                raise Exception("sorry i don't search for words with lengths greater than"
                                "my upper limit")

        word1_word2inv = Word([])
        word1_word2inv.add_word(word1)
        word1_word2inv.add_word(word2.return_inv_word())
        # print(word1.return_word_str() + " == " + word2.return_word_str() + "?")

        coset_w1w2inv = self.yield_coset_new(word1_word2inv, num)

        for w1w2inv_equiv in coset_w1w2inv:
            # ncor is normal closure of the relators, with the length of the equivalent to w1w2inv
            # being tested against the ncor being the maximum length
            if self._ncor.search_trie(w1w2inv_equiv):
                # print('equal')
                return True
        # print("not equal")
        return False

    def yield_elems_of_quotient(self, len_of_non_reduced, num_of_test_equals):
        # this method yields from the group each element of the quotient. it does so
        # by creating an iterable which yields the next member of the set of non reduced
        # Words on the Free group and tests if they are equal to members of the elements
        # of the quotient. if they aren't they then are yielded forward.
        if self._paranoid:
            if len_of_non_reduced > self._upper_limit:
                raise Exception("sorry no words with lengths greater than my upper limit")
            if num_of_test_equals > self._upper_limit:
                raise Exception("sorry no words with lengths greater than my upper limit")

        total = 0
        for t in range(len_of_non_reduced + 1):
            total = total + 4**t

        # overall_start_time = time.time()
        identity = Word([])
        elem_of_quotient = [identity]

        freegroup_nonreduced = self.yield_non_reduced_words(len_of_non_reduced)
        i = 0
        for a_word in freegroup_nonreduced:
            # print("I'm " + a_word.return_word_str())
            admitted = True
            # start_time = time.time()

            for existing_elem in elem_of_quotient:
                # print("I'm being tested against " + existing_elem.return_word_str())
                if self.test_equals(a_word, existing_elem, num_of_test_equals):
                    # print("didn't make it \n")
                    admitted = False
                    break

            # print("this took %s seconds \n" % (round(time.time() - start_time, 3)))
            i = i+1
            # print(str(i) + " of " + str(total - 1) + " completed")

            if admitted:
                # print("made it \n")
                elem_of_quotient.append(a_word)
                # print("memory used so far (in MB): ")
                # print(process.memory_info().rss / 10 ** 6)
                yield a_word

        # print("Overall time: %s seconds" % (round(time.time() - overall_start_time, 3)))
        # print("There are " + str(len(elem_of_quotient)) + " entries")
        # print("memory use:")
        # print(process.memory_info().rss / 10 ** 6)

    def list_generators(self):
        # this returns all of the generators in a list. This is done so that when the
        # Letters need to be added in graph form, it doesn't assume which letters to append.
        a_list = []
        for entry in self._generator_list:
            a_list.append(entry)
        return a_list

    def list_non_inv_generators(self):
        a_list = []
        for entry in self._generator_list:
            if not entry.check_capital():
                a_list.append(entry)

        return a_list

    def list_relator_strings(self):
        relator_list = []
        for entry in self._relator_list:
            relator_list.append(entry.return_word_str())
        return relator_list

    def list_generator_strings(self):
        generator_list = []
        for entry in self.list_non_inv_generators():
            generator_list.append(entry.get_str())
        return generator_list


class Cayley:
    # the purpose of this class is to store the data from previously
    # generated Groups and produce Cayley graphs from that data. In fact,
    # if I can, I can also create a program that will output a bunch of
    # text that can be fed into different
    def __init__(self):
        self._paranoid = True
        self._graph = nx.DiGraph()
        self._constr_time = 0

    def read_newgraph(self, a_group, num1, num2):
        # this is the same code i've been using to output all of the group graphics so far (so any and
        # all networkx/matplotlib graphics). i allowed for the user to input the numerator and denominator
        # as that would be simpler. the purpose of this class is in part to limit the computational effort
        # for each yielding of edges, etc. However, if this is just being called and the graph hasn't been
        # constructed yet then we might as well give the user some choice.
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("only groups with this method")

        construction_start = time.time()

        color_list = ['b', 'r', 'c', 'm', 'y', 'k']

        identity = Word([])
        elements = [identity]
        non_e_elements = a_group.yield_elems_of_quotient(num1, num2)
        for entry in non_e_elements:
            elements.append(entry)

        i = 0

        generators = a_group.list_non_inv_generators()

        for member in elements:
            # print(member)
            for j in range(len(generators)):
                gen_letter = generators[j]
                elem_with_letter = Word([])
                elem_with_letter.add_word(member)
                elem_with_letter.add_letter(gen_letter)
                # print(elem_with_letter)
                for member_2 in elements:
                    if a_group.test_equals(elem_with_letter, member_2, num2):
                        # print(elem_with_letter.return_word_str() + " == " + member_2.return_word_str())
                        # print(member.return_word_str() + " is connected to " + member_2.return_word_str() +
                        # " by " + gen_letter.get_str())
                        self._graph.add_edges_from([(member, member_2)], color=color_list[j])
                        break

            i = i + 1
            print(str(i) + " out of " + str(len(elements)) + " completed \n")

        print(str(self._graph.number_of_nodes()) + " is the number of nodes")
        print(str(self._graph.number_of_edges()) + " is the number of edges")

        pickel = input("Do you want me to pickle this graph? Y/N ")
        if pickel.lower() == 'y':
            self.pickle_me()

        group_p = input("Do you want me to pickle this group? Y/N ")
        if group_p.lower() == "y":
            self.pickle_my_group(a_group)

        self._constr_time = round(time.time() - construction_start, 3)

    def read_pickle(self, a_str):
        # this allows the user to input a pickle file for the graph rather
        # than having to generate the graph every time.
        self._graph = pickle.load(open(a_str, 'rb'))

        if not self._graph.nodes():
            raise Exception("there might be a problem, no nodes")

    def read_pickle_group(self, a_str, numerator, denominator):
        # this allows for a cayley object to read in a group from a pickle
        # rather than having to generate the group every time. This massively
        # increases the efficiency for larger groups.

        a_group = pickle.load(open(a_str, 'rb'))
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("This didn't read in a group")

        self.read_newgraph(a_group, numerator, denominator)

    def feed_pickle(self):
        # this takes a string input for the file name and feeds it to read pickle
        file_name = input("Please type the exact document name into this input: ")

        self.read_pickle(file_name)

    def draw(self):
        # this draws the graph that has been stored in the cayley object.
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("There's nothing to print, you haven't populated me with a graph yet")

        # word labels
        word_labels = {}
        for i in self._graph.nodes():
            word_labels[i] = i.return_word_str()

        # edge colors
        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u, v in edges]

        options = {
            'node_color': 'yellow',
            'node_size': 400,
        }
        pos = nx.spring_layout(self._graph)

        save_file = input("Do you want me to save this file? Y/N ")
        if save_file.lower() == 'y':
            denom = int(input("denominator? numbers only please "))
            group = str(input("what group is this? i.e. g2, g3, etc. "))
            version_num = str(input("what version i.e. 1, 2, etc. "))
            imagename = "ngroup.cayley." + group + ".(4," + str(denom) + ") - " + version_num + ".png"
            plt.savefig(imagename)

        plt.subplot()
        nx.draw(self._graph, pos, **options, labels=word_labels, edge_color=colors)
        plt.show()

    def pickle_me(self):
        input_name = str(input("What do you want me to name the pickle file "))
        filename = 'pickles/' + input_name + ".txt"
        print('hello')
        pickle.dump(self._graph, open(filename, 'wb'))
        print("saved to: "+filename)

    def pickle_my_group(self, a_group):
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("This is only for pickling groups")

        group_name = str(input("What should I name this group pickle? "))
        filename = 'pickles/' + group_name + ".txt"
        pickle.dump(self._graph, open(filename, 'wb'))
        print("saved to: " + filename)

    def export_gv(self):
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("I need a graph first")

        graphviz_output = Digraph()

        nodes = self._graph.nodes()
        for node in nodes:
            graphviz_output.node(node.return_word_str())

        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u, v in edges]
        print(colors)
        i = 0
        for (u, v) in edges:
            print(i)
            graphviz_output.edge(u.return_word_str(), v.return_word_str(), colors[i])
            i = i+1

        print(graphviz_output.source)
        # graphviz_output.render('test_output/group_cayley_output.gv')

    def for_saving(self):
        # make a method for saving the image and the data on the image rather than outputting it to the console

        # also include the memory and the runtime, and maybe even the group so that it can't be confused.

        # i made methods that list the generators and relators in lists of strings

        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("There's nothing to save, you haven't populated me with a graph yet")

        # word labels
        word_labels = {}
        for i in self._graph.nodes():
            word_labels[i] = i.return_word_str()

        # edge colors
        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u, v in edges]

        options = {
            'node_color': 'yellow',
            'node_size': 400,
        }

        pos = nx.spring_layout(self._graph)

        nx.draw(self._graph, pos, **options, labels=word_labels, edge_color=colors)

        plt.savefig("savefigure.png")

        numbers = open("savefile.txt", 'w')

        # numbers.write(str( + " are the generators\n"))
        # numbers.write(str( + " are the relators\n"))

        numbers.write(str(self._graph.number_of_nodes()) + " is the number of nodes\n")
        numbers.write(str(self._graph.number_of_edges()) + " is the number of edges\n")
        numbers.write(str(self._constr_time) + " is how long it took to build the graph\n")

        numbers.close()
