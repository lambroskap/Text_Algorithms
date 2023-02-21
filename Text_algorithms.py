############################ CONTENTS ##########################################
# 1.  Text_inequality_algorithm
# 2.  Brute_force1_algorithm
# 3.  KMP_algorithm_algorithm
# 4.  Brute_force2_algorithm
# 5.  Boyer_Moore_bad_character_algorithm
# 6.  Boyer_Moore_good_suffix_algorithm
# 7.  NaiveZ_algorithm
# 8.  Z_algorithm
# 9.  KMR_algorithm
# 10. Longest_palindrome_substring_algorithm
# 11. Manacher's_algorithm
# 12. Perfect_square_algorithm
# 13. Square_algorithm
# 14. Huffman_algorithm
# 15. Lempel_Ziv_Welch_algorithm
# 16. Edit_distance_algorithm
# 17. Longest_common_subsequence_algorithm
# 18. Rabin_Karp_algorithm
# 19. Longest_no_repeating_substring_algorithm
# 20. Lyndon_words_algorithm
# 21. Suffix_tree_construction_algorithm
# 22. Ukkonen_algorithm
# 23. McCreaight_algorithm
# 24. String_matching_finite_automata_algorithm
# 25. Aho_corasick_algorithm

################################## IMPLEMENTATION ##############################

################################# Text_inequality ##############################

def text_inequality(text1: str, text2: str) -> bool:
    """

    We check if two texts are equals.
    We do that by comparing the two texts character by character
    from left to right.
    e.g. text1[0] == text2[0] If `True` we continue with the next characters,
    else the texts are not equals and we return `True`.

    :param text1: A `text` that the user defines.
    :param text2: A `text` that the user defines.
    :return: `False` if the two texts are equals.`True` otherwise.

    """

    m = len(text1)
    n = len(text2)
    i = 0
    while i < min(m, n):
        if text1[i] == text2[i]:
            i += 1
        else:
            return True
    return False


################################ Brute_force1 ##################################


def brute_force1(text: str, pattern: str) -> bool:
    """

    The algorithm checks if the patterns exists in text.
    We do that by checking every character of `pattern` with
    the characters of the `text` from left to right.

    :param text: A `text` that the user defines.
    :param pattern: A `pattern` that the user defines and we want
     to check if it exists in text.
    :return: `True` if pattern exists in text.`False` otherwise.

    """

    i = 0
    n = len(text)
    m = len(pattern)
    while i <= n - m:
        j = 0
        while j < m and pattern[j] == text[i + j]:
            j += 1
        if j == m:
            return True
        i += 1
    return False


############################### KMP ############################################

def KMPSearch(pattern: str, text: str) -> None:
    """

    We search if a pattern exists in text.
    We do that by checking consecutive characters of `pattern` with  consecutive
    characters of`text` starting with the first character of each one.
    If the characters match we continue with the next character of both text and
    pattern and goes on.In case of missmatch we now can start checking where the Bord
    table tells us too avoiding the technique that naive algorithm uses.

    :param pattern: A given `string`.
    :param text: The `text` in which we check if `pattern` exists.

    """

    m = len(pattern)
    n = len(text)

    # create Bord[] that will hold the longest prefix suffix
    # values for pattern
    Bord = [0] * m  # initialise the values of Bord[] equals to zero
    j = 0  # index for pat[]

    # We need to preprocess the pattern before we start the string match
    # (so we calculate the Bord[] list)
    computeBordList(pattern, m, Bord)
    print('*' * 32)
    i = 0  # index for text[]
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            print("Pattern {} was found at text {} at index {}.".format(pattern, text, i - j))
            j = Bord[j-1]

        # mismatch after j matches
        elif i < n and pattern[j] != text[i]:
            # Do not match Bord[0..Bord[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = Bord[j-1]
            else:
                i += 1


def computeBordList(pattern: str, m: int, Bord: list) -> None:
    """

    Calculates the failure table `Bord` for a given pattern.
    That's the list that we need before we start checking for
    string-matching. The length of the list `Bord` is equal with the
    length of pattern.

    :param pattern: A sting that we want to calculate his bord table.
    :param m: The length of pattern.

    """
    i = 0  # length of the previous longest prefix suffix

    Bord[0] = 0  # We take as granted that Bord[0] is always 0
    j = 1

    # the loop calculates Bord[] for i = 1 to m-1 where m:length of pattern
    while j < m:
        if pattern[i] == pattern[j]:
            i += 1
            Bord[j] = i
            j += 1
        else:
            # When the characters don't match we need to
            # check the value of i in order to know where
            # we have to check for the next possible match
            if i != 0:
                i = Bord[i-1]

                # Also, note that we do not increment i here
                # but it takes the value of Bord[i-1] so that
                # we can skip the already matched characters
            else:
                Bord[j] = 0
                j += 1
    print('The Bord table of the pattern is: {0}'.format(Bord))


################################# Brute_force2 #################################


def brute_force2(pattern: str, text: str) -> bool:
    """

    The algorithm tells us if a `pattern` exists in a `text`.
    The way that we do that is by checking equality of consecutive
    characters of both text and pattern by scanning them from right
    to left in contrast of brute_force1.

    :param pattern: The pattern that we want to find in text.
    :param text: The text in which we check if the pattern exists.
    :return: True if the `pattern` exists in `text`.False otherwise.

    """

    i = 0
    n = len(text)
    m = len(pattern)
    while i < n - m:
        j = m
        while j > 0 and pattern[j - 1] == text[i + j - 1]:
            j -= 1
        if j == 0:
            # print('Pattern {0} was found at position {1} in text {2}.'.
            #     format(pattern, i, text))
            return True
        i += 1
    return False


########################### Boyer_Moore_bad_character ##########################


NO_OF_CHARS = 256  # global variable for unicode chars


def badcharpreprocess(pattern: str, m: int) -> list:
    """
    Creates a list by preprocessing the pattern.

    The list contains the index of the last occurrence of each
    character in pattern.

    :param pattern: A `string`.
    :param m: The length of `string`.
    :return: The preprocessed list.
    """

    # Initialize all occurrence of list as -1
    badchar = [-1] * NO_OF_CHARS

    # Fill the value of last occurrence of each
    # character in our pattern
    # ord() --> returns an integer representing the
    # Unicode character for input string
    for i in range(m):
        badchar[ord(pattern[i])] = i

    return badchar


def boyermoorebadcharsearch(text: str, pattern: str) -> None:
    """
     A string-matching function that uses the preprocessed list of pattern
     in order to find a match between pattern and text.

    :param text: A given `string` in which we search for the pattern in it.
    :param pattern: The `string` that we search for in `text`.
    """

    m = len(pattern)
    n = len(text)

    # create the bad character list of our pattern
    badchar = badcharpreprocess(pattern, m)

    # s is shift of the pattern. we set it as 0 at the
    # beginning meaning that we check the first m chars
    # of pattern with the first m chars of text from right
    # to left
    s = 0
    while s <= n-m:
        j = m-1

        # Keep reducing index j of pattern while
        # characters of pattern and text are matching
        # at this shift s
        while j >= 0 and pattern[j] == text[s+j]:
            j -= 1

        # If the pattern is present at current shift,
        # then index j will become -1 after the above loop
        if j < 0:
            print("Pattern occur at shift = {}".format(s))

            '''   
                Shift the pattern so that the next character in text
                      aligns with the last occurrence of it in pattern.
                The condition s+m < n is necessary for the case when
                   pattern occurs at the end of text
               '''
            s += (m-badchar[ord(text[s+m])] if s+m < n else 1)
        else:
            '''
               Shift the pattern so that the bad character in text
               aligns with the last occurrence of it in pattern. The
               max function is used to make sure that we get a positive
               shift. We may get a negative shift if the last occurrence
               of bad character in pattern is on the right side of the
               current character.
            '''
            s += max(1, j-badchar[ord(text[s+j])])


########################## Boyer_Moore_good_suffix #############################


def preprocess_strong_suffix(shift: list, border: list, pat: str, m: int) -> None:
    """A function that preprocesses the pattern
    in order to find the border list of the pattern.

    :param shift: A list that tells us how many characters of text
    we need to shift in case of a missmatch before we continue our
    pattern-text character by character comparisons.
    :param border: A list that contains the starting index of border
    for each suffix of pattern.
    :param pat: A given string.
    :param m: The length of string `pat`.
    """

    # m is the length of pattern
    i = m
    j = m + 1
    border[i] = j

    while i > 0:

        '''if character at position i-1 is 
        not equivalent to character at j-1, 
        then continue searching to right 
        of the pattern for border '''
        while j <= m and pat[i - 1] != pat[j - 1]:

            ''' the character preceding the occurrence 
            of t in pattern P is different than the 
            mismatching character in P, we stop skipping
            the occurrences and shift the pattern 
            from i to j '''
            if shift[j] == 0:
                shift[j] = j - i
            # Update the position of next border
            j = border[j]

        ''' p[i-1] matched with p[j-1], border is found. 
        store the beginning position of border '''
        i -= 1
        j -= 1
        border[i] = j


# Preprocessing for case 2
def preprocess_case2(shift: list, border: list, pat: str, m: int) -> None:
    j = border[0]
    for i in range(m + 1):

        ''' set the border position of the first character 
        of the pattern to all indices in array shift
        having shift[i] = 0 '''
        if shift[i] == 0:
            shift[i] = j
        ''' suffix becomes shorter than border[0], 
        use the position of next widest border
        as value of j '''
        if i == j:
            j = border[j]


def search(text: str, pat: str) -> None:
    """

    The boyer-moore algorithm that searches for occurrences
    of the pattern in text.We take advantage of the preprocessed lists
    border, shift in order to avoid the unnecessary character by character
    comparisons of brute force algorithm.

    :param text: A given text string.
    :param pat: The `pattern` that we want to search if it exists in `text`.

    """

    # s is shift of the pattern with respect to text
    s = 0
    m = len(pat)
    n = len(text)

    border = [0] * (m + 1)

    # initialize all occurrence of shift to 0
    shift = [0] * (m + 1)

    # do preprocessing
    preprocess_strong_suffix(shift, border, pat, m)
    preprocess_case2(shift, border, pat, m)

    print('The shift list is : {0}\nand the border list is: {1}'
          .format(shift, border))

    while s <= n - m:
        j = m - 1

        ''' Keep reducing index j of pattern while characters of 
            pattern and text are matching at this shift s'''
        while j >= 0 and pat[j] == text[s + j]:
            j -= 1

        ''' If the pattern is present at the current shift, 
            then index j will become -1 after the above loop '''
        if j < 0:
            print("pattern occurs at shift = {}".format(s))
            s += shift[0]
        else:

            '''pat[i] != pat[s+j] so shift the pattern 
            shift[j+1] times '''
            s += shift[j + 1]


################################ Z_naive #######################################


def z_naive(string: str, z: list) -> list:
    """

    A function that calculates the z array for the concatenated string
    pattern + $ + text.

    :param string: A concatenated string of `pattern` and `text` alongside $.
    :param z: z array.
    :return: z array.

    """

    for k in range(1, len(string)):
        n = 0
        while n + k < len(string) and string[n] == string[n + k]:
            n += 1
        z[k] = n
    return z


def search1(text: str, pattern: str) -> None:
    """

    A function that searches for occurrences of a pattern
    in text with the help of z array in O(n^2) time, where n
    is the length of text.

    :param text: A given `text`.
    :param pattern: A given `pattern`

    """

    # Create concatenated string "P$T"
    concat = pattern + "$" + text
    l = len(concat)
    z = [0] * l
    # Initialize z array as 0 for all indexes of pattern
    z_naive(concat, z)  # construction of z array
    print(z)

    t = 0
    # now looping through Z array for matching condition
    for i in range(l):

        # if Z[i] (matched region) is equal to pattern
        # length we got the pattern
        if z[i] == len(pattern):
            print("Pattern {} was found at text {} at index {}".
                  format(pattern, text, i - len(pattern)-1))
            t += 1
    if t == 0:
        print("Pattern {} was not found in text {}".format(pattern, text))


################################### Z_algorithm ################################


def zarrayconstruction(string: str, z: list) -> list:
    """

    A function that calculates the z array for the concatenated `pattern`, $, `text`
    with respect to a window [L,R].

    :param string: A string that contains pattern, $, text concatenated.
    :param z: The array z.
    :return: z array.

    """

    n = len(string)

    # [L,R] make a window which matches
    # with prefix of s
    l, r, k = 0, 0, 0  # l is the left bound of window,
    # r is the right bound of window and
    # k is the current index
    for i in range(1, n):

        # if i>R nothing matches so we will calculate.
        # Z[i] using naive way.
        if i > r:
            l, r = i, i

            # R-L = 0 in starting, so it will start
            # checking from 0'th index. For example,
            # for "ababab" and i = 1, the value of R
            # remains 0 and Z[i] becomes 0. For string
            # "aaaaaa" and i = 1, Z[i] and R become 5
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:

            # k = i-L so k corresponds to number which
            # matches in [L,R] interval.
            k = i - l

            # if Z[k] is less than remaining interval
            # then Z[i] will be equal to Z[k].
            # For example, str = "ababab", i = 3, R = 5
            # and L = 2
            if z[k] < r - i + 1:
                z[i] = z[k]

            # For example str = "aaaaaa" and i = 2,
            # R is 5, L is 0
            else:

                # else start from R and check manually
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z



def search2(text: str, pattern: str) -> None:
    """

    A function that searches for occurrences of a pattern
    in text with the help of z array in O(n + m) time, where n, m
    is the length of text and pattern.

    :param text: A given `text`.
    :param pattern: A given `pattern`

    """

    # Create concatenated string "P$T"
    concat = pattern + "$" + text
    l = len(concat)

    # Initialize z array as 0 for all indexes of pattern
    z = [0] * l
    zarrayconstruction(concat, z)  # construction of z array

    t = 0
    # now looping through Z array for matching condition
    for i in range(l):

        # if Z[i] (matched region) is equal to pattern
        # length we got the pattern
        if z[i] == len(pattern):
            print("Pattern {} was found at text {} at index {}".
                  format(pattern, text, i - len(pattern)-1))
            t += 1
    if t == 0:
        print("Pattern {} was not found in text {}".format(pattern, text))


############################### KMR ############################################


def factors_of_current_length(length_of_factor: int, pattern: str, m: int):
    """
    A function that finds the factors of a pattern taking into consideration
    the length of factors that we want to find.

    :param length_of_factor: An `int` that defines what is the length of the
    factors that we search.
    :param pattern: A given `string`.
    :param m: Length of `pattern`.
    :return: A `list` that contains all the factors of given length alongside with its length.

    """

    factors = []
    for i in range(m):
        if len(pattern[i:i+length_of_factor]) == length_of_factor:
            factors.append(pattern[i:i+length_of_factor])
    n = len(factors)
    print("The factors of current length {} are {}".format(length_of_factor, factors))
    return factors, n


def factor_occurrences(characteristic_number: int, length_of_factor: int, factors: list, dic: dict, factor_count: dict,
                       pattern: str, n: int):
    """
     A function that first sorts the list factors in order to give a characteristic value to each factor and then
    store it in a dictionary.

    Also find the occurrences of each factor and store it in a dictionary as key-value pairs.

    :param characteristic_number: The unique number that characterize each factor.
    :param length_of_factor:An `int` that defines what is the length of the
    factors that we search.
    :param factors: A `list` that contains the factors of pattern.
    :param dic: A `dictionary` of factors with their unique values.
    :param factor_count: A `dictionary` of factors with their number of occurrences.
    :param pattern: A given `string`.
    :param n: Length of list factors.
    :return: The `list` factors, the `dictionaries` dic and factor_count and also the
    `int` characteristic number.

    """

    m = len(pattern)
    factors.sort()
    for i in range(n):
        if factors[i] not in dic.keys():
            dic[factors[i]] = characteristic_number
            factor_count[factors[i]] = 1
            characteristic_number += 1
        else:
            factor_count[factors[i]] += 1
    factors = []
    for i in range(m):
        if len(pattern[i:i+length_of_factor]) == length_of_factor:
            factors.append(dic[pattern[i:i+length_of_factor]])
    return factors, characteristic_number, dic, factor_count


def find_factors(pattern: str) -> None:
    """

    A function to display the factors of a given pattern alongside with their characteristic value
    and number of occurrences.

    :param pattern : A given `string`.

    """

    characteristic_number = 1
    length_of_factor = 1
    # defined as 1 because for each pattern we are sure
    # that we need to find his factor of length 1
    dic = {}
    # a dictionary that stores key-value pairs of
    # factors-characteristic number for each one
    factor_count = {}
    # a dictionary that stores key-value pairs of
    # factors - number of occurrences for each factor
    m = len(pattern)  # length of a given pattern
    table = []
    # a list that contains all the factors of pattern
    while length_of_factor <= m:
        factors, n = factors_of_current_length(length_of_factor, pattern, m)
        num, characteristic_number, dic, factor_count = factor_occurrences(characteristic_number, length_of_factor,
                                                                           factors, dic, factor_count, pattern, n)
        table.append(num)
        length_of_factor = 2 * length_of_factor
        # we increase length_of_factor by
        # multiplying with 2 so that we can find all factors of text with respect to
        # its length
    print("All factors of pattern as their unique values are: {}\n". format(table))
    print("Factors of pattern '{}' and number of occurrences: {}".format(pattern, factor_count))


########################### Longest_palindrome_substring #######################


def longest_palindrome_substring(text: str):
    """

    A function that finds the biggest palindrome that occurrence
    in a text and prints it out alongside with her length.

    :param text: A given `string`.

    """

    n = len(text)  # length of string
    # if string is empty ' ' then size will be 0.
    #  if n==1 then, answer will be 1(single
    # character will always be a palindrome of itself)
    # so we need to cover those cases too.
    if n == 0:
        print("Longest palindrome substring is the empty string")
        print("Length of longest palindrome is:{}".format(n+1))
    elif n == 1:
        print("Longest palindrome substring is:{}".format(text[0]))
        print("Length of longest palindrome is:{}".format(n))
    else:

        # We take into consideration that the first palindrome is
        # the character that start at index 0.
        start = 0

        # and the length of palindrome is 1
        max_length = 1

        # The for loop indicate the current center that we keep
        # expanding left and right
        for i in range(n):
            low = i - 1
            high = i + 1
            while high < n and text[high] == text[i]:
                high = high + 1

            while low >= 0 and text[low] == text[i]:
                low = low - 1

            # we keep expanding left and right until we have a
            # missmatch between text[low] and text[high]
            while low >= 0 and high < n and text[low] == text[high]:
                low = low - 1
                high = high + 1

            # calculating the length of current palindrome
            length = high - low - 1

            # if it's bigger than max_length then we have a found a
            # longest palindrome that begins at index start.
            if max_length < length:
                max_length = length
                start = low + 1

        print("Longest palindrome substring is:", end=" ")
        print(text[start: start + max_length])
        print("Length of longest palindrome is {}".format(max_length))


############################## Manachers #######################################


def manachers(text: str) -> None:
    """

    A function that find the longest palindrome substring of a given text
    using the Manacher's improvements so that we don't have to check each
    character as center.With those improvements we can find the longest
    palindrome substring in linear time O(n).
    There are 4 cases that we check.

    Case 1:
    longest_palindrome_substring[currentRightPosition] = longest_palindrome_substring[i_mirror]
    when
    1)i-left palindrome contained inside the center palindrome,
    2)i-left palindrome is not a prefix of center palindrome.
    That happens when longest_palindrome_substring[i_mirror] < centerRightPosition - currentRightPosition

    Case 2:
    longest_palindrome_substring[currentRightPosition] = longest_palindrome_substring[i_mirror]
    when
    1)i-left palindrome is prefix of center palindrome,
    2)center palindrome is suffix of input text.
    That happen when longest_palindrome_substring[currentLeftPosition] = centerRightPosition - currentRightPosition

    Case 3:
    longest_palindrome_substring[currentRightPosition] >= longest_palindrome_substring[i_mirror]
    when
    1)i-left palindrome is prefix of center palindrome,
    2)center palindrome is not a suffix of input text.
    That happens when L[i_mirror] = centerRightPosition – currentRightPosition (For 1st condition) AND
    centerRightPosition < 2 * n where n is input string length n (For 2nd condition).
    In that case there is a possibility for expansion of i-right palindrome and the length of i-right palindrome
    will be at least equal or bigger than length of i-left palindrome.

    Case 4:
    longest_palindrome_substring[currentRightPosition] >= longest_palindrome_substring[i_mirror]
    when
    i-left palindrome is not contained whole in center palindrome.
    That happens when L[i_mirror] > centerRightPosition – currentRightPosition.

    We change centerPosition into currentRightPosition if palindrome centered in currentRightPosition
    expands beyond centerRightPosition.
    In this case, length of i-right palindrome is at least as long (centerRightPosition – currentRightPosition) and
    there is a possibility of i-right palindrome expansion.

    :param text: A given `string`.

    """

    n = len(text)
    if n == 0:
        return

    # We put a '$' before and after each character,so
    # we have to change the length of our input.
    n = 2 * n + 1
    # Initialize our list to 0
    longest_palindrome_substring = [0] * n
    longest_palindrome_substring[0] = 0
    longest_palindrome_substring[1] = 1
    center = 1     # centerPosition
    right_center_position = 2     # centerRightPosition
    current_right_position = 0    # currentRightPosition
    i_mirror = 0     # currentLeftPosition
    max_lps_length = 0
    max_lps_center_position = 0
    start = -1
    end = -1
    diff = -1

    for i in range(2, n):

        # get currentLeftPosition i_mirror for currentRightPosition i
        i_mirror = 2 * center - i
        longest_palindrome_substring[i] = 0
        # we calculate the difference between right_center_position - current_right_position
        # in order to find which case apply
        difference = right_center_position - i
        # If currentRightPosition i is within centerRightPosition R
        if difference > 0:
            longest_palindrome_substring[i] = min(longest_palindrome_substring[i_mirror], diff)

        # Attempt to expand palindrome centered at currentRightPosition i
        # Here for odd positions, we compare characters and
        # if match then increment LPS Length by ONE
        # If even position, we just increment LPS by ONE without
        # any character comparison
        try:
            while ((i + longest_palindrome_substring[i]) < n and (i - longest_palindrome_substring[i]) > 0) and \
                    (((i+longest_palindrome_substring[i]+1) % 2 == 0) or
                     (text[(i+longest_palindrome_substring[i]+1)//2] == text[(i-longest_palindrome_substring[i] - 1)//2])):
                longest_palindrome_substring[i] += 1
        except Exception as e:
            pass

        if longest_palindrome_substring[i] > max_lps_length:        # Find maxLPSLength
            max_lps_length = longest_palindrome_substring[i]
            max_lps_center_position = i

        # If palindrome centered at currentRightPosition i
        # expand beyond centerRightPosition R,
        # adjust centerPosition C based on expanded palindrome.
        if i + longest_palindrome_substring[i] > right_center_position:
            center = i
            right_center_position = i + longest_palindrome_substring[i]

    start = (max_lps_center_position - max_lps_length) // 2
    end = start + max_lps_length - 1
    print("LPS of string '{}' is: '{}'.".format(text, text[start:end + 1]))
    #print(longest_palindrome_substring)



################################# Perfect_square ###############################


def perfectSquare(text: str) -> bool:
    """

    A function that check if a string is a perfect square.

    :param pattern: A given `string` that we want to check.
    :return: If it is a perfect square return `True` otherwise return `False`

    """

    m = len(text)
    l = m // 2  # split pattern into two equal segments
    i = 0
    j = 0
    while j < l:
        if text[j] == text[l + j]:  # checking if characters of segment 1 are equals with characters of segment 2
            i += 1
        j += 1
    if i == l:
        print("The string {} is a perfect square.".format(text))
        return True
    else:
        print("The string {} is not a perfect square.".format(text))
        return False


############################### Square #########################################


def SquareAlgorithm(word: str) -> bool:
    """

    A function that splits the string in half and then continue splitting
    the segments until they are segments of one character.

    Then he tries to find if there is a square in string by comparing the
    least created characters.

    :param word: A given `string`.
    :return: `True` if there is a square in string otherwise `False`

    """

    length = len(word)
    half_length = int(length / 2)
    if length > 1:  # we keep splitting the word until there are only segments of one character
        if SquareAlgorithm(word[0:half_length]):  # splitting the first half
            return True
        if SquareAlgorithm(word[half_length:length]):  # splitting the second half
            return True
        if test(word[0:half_length], word[half_length:length]):
            return True
    return False


def test(x: str, y: str) -> bool:
    """

    A function that finds if there is a square that has its center in y
    but start in x.

    :param x: A substring of the word in which we search for a square.
    :param y: A substring of the word in which we search for a square.
    :return: `True` if there is a square that fulfill the principle that we
    defined , `False` otherwise.

    """

    i = len(y)
    center = i + 1  # center of possible square
    while i >= 1:
        j = i
        # traversing right-to-left
        while (j >= 1) and (len(x) - i + j >= 1) and (x[len(x) - i + j - 1] == y[j - 1]):
            j = j - 1
        if j == 0:  # The length of word is even and there is a square in it
            return True
        k = i + j
        if k < center:
            center = k
            # traversing right-to-left
            while center > i and y[center-1] == y[j - k + center - 1]:
                center = center - 1
            if center == i:
                return True

        i = max(j, int(i/2))-1
    return False  # no square centered in y


################################ Huffman #######################################


class Nodes:
    def __init__(self, frequency, character, left=None, right=None):
        # frequency of the character
        self.frequency = frequency

        # character
        self.character = character

        # left node
        self.left = left

        # right node
        self.right = right

        # tree direction (0 or 1)
        self.code = ''


def compute_frequency(text: str) -> dict:
    """

    A function that calculates the frequency for each unique character.

    :param text: A `text` that the user defines.
    :return: A `dictionary` of the characters found in text alongside
             with their frequency in text as (key: value) pairs.

    """

    unique_characters = dict()
    for character in text:
        # if the character is not already in dictionary
        # we initialise its value to 1 else we increment
        # its value by 1.
        if unique_characters.get(character) is None:
            unique_characters[character] = 1
        else:
            unique_characters[character] += 1
    return unique_characters


codes_of_characters = dict()


def compute_code(node, value='') -> dict:
    """

    A function that calculates the unique code for each character.

    :return: A dictionary that contains the unique code for each character
             as (key: value) pairs.

    """

    # a huffman code for current node
    new_value = value + str(node.code)

    if node.left:
        compute_code(node.left, new_value)
    if node.right:
        compute_code(node.right, new_value)

    if not node.left and not node.right:
        codes_of_characters[node.character] = new_value

    return codes_of_characters


def encoding_output(text: str, coding: dict) -> str:
    """

    A function that assigns each character of the text to its corresponding unique code.

    :param text: A `text` that the user defines.
    :param coding: A `dictionary` that contains the unique code for each character.
    :return: A `string` that represents the same text but in its encoding form.

    """

    output = []
    for character in text:
        output.append(coding[character])

    encoding_text = ''.join([str(item) for item in output])
    return encoding_text


def difference(text: str, coding: dict) -> tuple:
    """

    A function that calculates how many bits we need to represent the text before
    and after compression.

    :param text: A `text` that the user defines.
    :param coding:A `dictionary` that contains the unique code for each character.
    :return: The number of bits needed to represent the same information before and after compression.

    """

    bits_before_compression = len(text) * 8
    bits_after_compression = 0
    characters = coding.keys()
    for character in characters:
        # calculating how many times each character appears in text.
        text_count = text.count(character)
        # calculating how many bits is required for that character in total.
        bits_after_compression += text_count * len(coding[character])
    return bits_before_compression, bits_after_compression


def huffman(text: str) -> None:
    """

    A function that compresses the text into a smaller binary form.

    :param text: A `text` that the user defines.
    :return: None.

    """

    character_with_frequency = compute_frequency(text)
    characters = character_with_frequency.keys()
    frequencies = character_with_frequency.values()
    print("Characters: {} ".format(characters))
    print("Frequencies: {} ".format(frequencies))

    nodes = []

    # converting characters and frequencies into huffman tree nodes
    for character in characters:
        nodes.append(Nodes(character_with_frequency.get(character), character))

    while len(nodes) > 1:
        # sorting all the nodes in ascending order based on their frequency
        nodes = sorted(nodes, key=lambda x: x.frequency)
        # for node in nodes:
        #     print(node.character, node.frequency)

        # picking two smallest nodes
        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        new_node = Nodes(left.frequency + right.frequency, left.character + right.character, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    huffman_encoding = compute_code(nodes[0])
    print("Characters with codes: ", huffman_encoding)
    encoded_output = encoding_output(text, huffman_encoding)
    bits_before, bits_after = difference(text, huffman_encoding)
    print("Number of bits that we needed before compression: {}.".format(bits_before))
    print("Number of bits that we needed after compression: {}.".format(bits_after))
    print("Encoded output: {}".format(encoded_output))
    print("Decoded Output: {}".format(decoding(encoded_output, nodes[0])))
    print("With huffman coding we need {} less bits to represent the same information."
          .format(bits_before - bits_after))


def decoding(encoded_text: str, huffman_tree) -> str:
    """

    A function that transform the compressed text to its initial form.

    :param encoded_text: The binary form of text after the compression.
    :param huffman_tree: The `huffman` tree.
    :return: The initial text.

    """
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_text:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.character is None and huffman_tree.right.character is None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.character)
            huffman_tree = tree_head
    print(decoded_output)
    text = ''.join([str(item) for item in decoded_output])
    return text


################################ Lempel_Ziv_Welch ##############################


def text_compress(text: str) -> list:
    """

    Compress a text to a list of unique codes.We do that by checking
    if a single character is in the dictionary.If yes then we expand
    for 1 character and check again if the substring is in the dictionary.
    If not we insert it and give it the next available number with respect to
    dictionary size.Then we store in the list the code of the substring that we
    take if we remove the last character from the substring that we check if is
    in dictionary.Then we take the last character of the substring that we check
    and repeating the same procedure until we reach the end of the text.

    :param text: A `text` that the user defines.
    :return: A list of unique codes that represent the text in a compressed form.

    """

    # We initialize dictionary with 256 default ASCII characters.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))

    substring = ""  # we initialize first substring as the empty string.
    result = []  # the list that will contain the unique codes
    for character in text:
        new_substring = substring + character
        if new_substring in dictionary:
            substring = new_substring
        else:
            result.append(dictionary[substring])
            # Add new_substring to the dictionary.
            dictionary[new_substring] = dict_size
            dict_size += 1
            substring = character

    # Output the code for substring.
    if substring:
        result.append(dictionary[substring])
    return result


def text_decompress(list_of_codes: list) -> str:
    """

    Decompress the list of unique codes into the text.

    :param list_of_codes: The codes for the text that we created
                          in text_compress function.
    :return: The given 'text' in its uncompressed form.

    """

    from io import StringIO

    # We initialize dictionary with the 256 default ASCII characters.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    substring = chr(list_of_codes.pop(0))
    result.write(substring)
    for code in compressed:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = substring + substring[0]
        else:
            raise ValueError('Bad compressed code: %s' % code)
        result.write(entry)

        # Add substring + entry[0] to the dictionary.
        dictionary[dict_size] = substring + entry[0]
        dict_size += 1

        substring = entry
    return result.getvalue()


compressed = text_compress('TOBEORNOTTOBEORTOBEORNOT')

############################### Edit_distance ##################################


def edit_distance(str1: str, str2: str) -> None:
    """
    A function that computes how many operations we need in order to
    convert `str1` into `str2`.
    ----------------------------------------------------------------
                            Operations:

    -> Insert: Insert a character into `str2`.

    -> Delete: Delete a character from `str2`.

    -> Replace:Replace a character from `str2` with a character
    from `str1`.

    ----------------------------------------------------------------

    :param str1: A `string` that the user defines.
    :param str2: The 'string' that we want to produce by making operations
                 on `str1`.
    """

    m = len(str1)
    n = len(str2)

    # We initialize the two-dimensional table with 0 for each element.
    levenshtein_table = [[0 for i in range(n + 1)] for j in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                levenshtein_table[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                levenshtein_table[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                levenshtein_table[i][j] = levenshtein_table[i-1][j-1]

            # If last character are different, consider all
            # operations and find minimum.
            else:
                levenshtein_table[i][j] = 1 + min(levenshtein_table[i][j-1],  # Insert
                                                  levenshtein_table[i-1][j],        # Remove
                                                  levenshtein_table[i-1][j-1])    # Replace

    print('The Levenshtein table for {} and {} is: '.format(str1, str2))
    for i in range(m + 1):
        for j in range(n + 1):
            if j == n:
                print(levenshtein_table[i][j])
            else:
                print(levenshtein_table[i][j], '\t', end='|')
    print('The last element of Levenshtein table defines the minimum operations that we need to do,')
    print('so in order to produce {} from {} we need {} operations.'.format(str2, str1, levenshtein_table[m][n]))


########################### Longest_common_subsequence #########################


def calculate_longest_common_subsequence(str1: str, str2: str) -> None:
    """

    A function that calculates the longest common subsequence table for
    two strings.The value of the last cell defines the length of the longest
    common subsequence between the two strings and acts as a guide in order to
    find it.
    We create the lcs_table by using dynamic programming meaning that we can
    find the next value of a cell by using already calculated cell values.

    :param str1: A `string` that the user defines.
    :param str2: A `string` that the user defines.

    """

    m = len(str1)
    n = len(str2)

    # We create a table of dimensions (m+1) * (n+1) and we initialize
    # its values as zeros.
    lcs_table = [[0 for i in range(n+1)] for j in range(m+1)]

    # lcs_table[i][j] contains length of longest_common_subsequence of
    # str1[0..i-1] and str2[0..j-1].

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:  # We store zeros as the values of the first row and the first column of table.
                lcs_table[i][j] = 0
            elif str1[i-1] == str2[j-1]:
                lcs_table[i][j] = lcs_table[i-1][j-1] + 1
            else:
                lcs_table[i][j] = max(lcs_table[i-1][j], lcs_table[i][j-1])

    # Create a string variable to store the lcs string
    longest_common_subsequence = ""

    # Starting from the right bottom corner
    # we store characters of longest_common_subsequence
    # in string lcs.
    i = m
    j = n
    while i > 0 and j > 0:

        # If current character in str1 and str2 are same, then
        # current character is part of LCS and we continue moving up
        # diagonally.
        if str1[i-1] == str2[j-1]:
            longest_common_subsequence += str1[i-1]
            i -= 1
            j -= 1

        # If not same, then find the larger of two and
        # go in the direction of larger value.
        elif lcs_table[i-1][j] > lcs_table[i][j-1]:  # We move up from the current cell.
            i -= 1
        else:  # We move left from the current cell.
            j -= 1

    # We need to reverse the lcs because we calculated it from
    # the bottom and not from the start.
    print("The Longest common subsequence table for string {} and string {} is:".format(str1, str2))
    for i in range(m + 1):
        for j in range(n + 1):
            if j == n:
                print(lcs_table[i][j])
            else:
                print(lcs_table[i][j], '\t', end='|')
    lcs_reversed = reverse_string(longest_common_subsequence)
    print("Longest common subsequence of string {} and string {} is {} with a length of {}.".format(str1, str2,
                                                                                                    lcs_reversed,
                                                                                                    lcs_table[m][n]))


def reverse_string(lcs: str) -> str:
    """

    A function that reverse a string.

    :param lcs: The longest common subsequence found from the bottom to the top.
    :return: The longest common subsequence with the right order, that is from top
             to bottom.

    """
    lcs_reversed = lcs[::-1]
    return lcs_reversed


################################### Rabin_Karp #################################


def rabin_karp(text: str, pattern: str, d=256, q=101) -> None:
    """

    A function that operating `string-matching` between a pattern
    and a text. In order to do that we are using hashing alongside with
    the sliding window technique.

    We calculate the hash value of pattern and each window.If we find
    match between those two we continue by performing character by
    character comparisons between those two in order to confirm that
    we found pattern in text. We repeat that until we reach at the final
    window of text.

    :param text: A `text` that the user defines.
    :param pattern: A 'pattern' that the user defines and we need to
                     check if exists in `text`.
    :param d: The different characters from which the `pattern` and
               `text` can be created. We set as default value the 256 ASCII
               characters.
    :param q: A prime number. We set as default value the number 101.
    :return: None.

    """

    n = len(text)
    m = len(pattern)

    h = pow(d, m-1) % q
    # We initialize hash value of pattern and hash value of
    # m first characters of text as 0.
    hash_p = 0
    hash_s = 0
    # We create a list that stores the indexes of text in which
    # we found the pattern.
    output = []

    # We calculate hash of pattern and hash of m first characters
    # of text.
    for i in range(m):
        hash_p = (d * hash_p + ord(pattern[i])) % q
        hash_s = (d * hash_s + ord(text[i])) % q

    for i in range(n - m + 1):
        # We check if hash of pattern and hash of current window
        # matches.If yes we do a character-character comparison
        # between pattern and current window. If we have match we
        # add the starting position i of current window in output.
        if hash_s == hash_p:
            if text[i:i + m] == pattern:
                output.append(i)
        # if hash of pattern and hash of current window don't match
        # and we are also before the last window we calculate the hash
        # value of the next window.
        if i < n-m:
            hash_s = (d * (hash_s-ord(text[i]) * h) + ord(text[i+m])) % q
    k = len(output)
    if k == 0:
        print("The pattern '{}' doesn't exist in text '{}'.".format(pattern, text))
    else:
        for i in range(k):
            print("The pattern '{}' was found in text '{}' at position {}.".format(pattern, text, output[i]))


###################### Longest_no_repeating_substring ##########################


def longest_sub_no_repeating(text: str) -> None:
    """

    A function that calculates the longest substring without repeating
    characters using the sliding window technique alongside with a hash
    table.

    :param text: A `string` that the user defines.
    :return: None

    """

    n = len(text)

    # starting point of current substring.
    st = 0

    # maximum length substring without
    # repeating characters.
    max_length = 0

    # starting index of maximum
    # length substring.
    start = 0

    # Hash Map to store last occurrence
    # of each already visited character.
    pos = {}

    # Last occurrence of first
    # character is index 0
    pos[text[0]] = 0

    for i in range(1, n):

        # If this character is not present in hash,
        # then this is the first occurrence of this
        # character and we store it in hash.
        if text[i] not in pos:
            pos[text[i]] = i

        else:
            # If this character is present in hash then
            # this character has previous occurrence.
            # Then we check if that occurrence is before
            # or after starting point of current substring.
            if pos[text[i]] >= st:

                # find length of current substring and
                # update max_length and start accordingly.
                current_length = i - st
                if max_length < current_length:
                    max_length = current_length
                    start = st

                # Next substring will start after the last
                # occurrence of current character to avoid
                # its repetition.
                st = pos[text[i]] + 1

            # Update last occurrence of
            # current character.
            pos[text[i]] = i
    # Compare length of last substring with max_length
    # and update max_len and start accordingly.
    if max_length < i - st:
        max_length = i - st
        start = st

    print("The longest substring without repeating characters for '{}' is '{}' with a length of {}."
          .format(text, text[start: start + max_length], max_length))


############################### Lyndon_words ###################################


def lyndon_words(s: list, n: int) -> None:
    """

    A function that generates Lyndon words of a specified
    length and a specified alphabet that the user defines.

    A Lyndon word is a non-empty string that is strictly
    smaller in lexicographic order than all of its rotation.

    e.g. 'abc' is a Lyndon word because it's less than its
    rotation 'bca' and 'cab'.

    :param s: The alphabet that we use to produce Lyndon words.
    :param n: The length of the Lyndon words that we want to produce.

    """

    # First we sort the list.
    s.sort()
    # We use a second list that gives indexes
    # to each character of the s list.
    result = [-1]
    k = len(s)
    # Count how many Lyndon words
    # of length n we can produce.
    total = 0
    print("The Lyndon words of length {} that we can produce are:".format(n))
    while result:
        # We increment the last value of result
        result[-1] += 1
        m = len(result)
        if m == n:
            print(''.join(s[i] for i in result))
            total += 1

        # Repeating result to get a
        # n-length string.
        while len(result) < n:
            result.append(result[-m])
        # Removing the last character as long
        # it is equal to the largest character
        # in s
        while result and result[-1] == k-1:
            result.pop()

    print("So we generated {} Lyndon words of length {} from the alphabet {}."
          .format(total, n, s))


############################## Suffix_tree_construction ########################


import os


def get_suffixes(string: str) -> list:
    """

    A function that returns all the suffixes of a given `string`.

    :param string: A 'string' that the user defines.
    :return: A `list` with the suffixes of the given `string`.

    """

    return [string[i:] + "$" for i in range(len(string) + 1)]


def shared_prefix(strings: list) -> str:
    """

    A function that find the common prefix between strings.

    :param strings: A `list` of strings.
    :return: The prefix between string_a and string_b.If there is no
             prefix returns "".

    """

    return os.path.commonprefix([strings[i] for i in range(len(strings))])


def construct_suffix_tree(string: str) -> dict:
    """

    A function that construct the suffix tree of a given `string`.

    :param string: A given `string`.
    :return:The suffix tree in a form of a `dictionary`.

    """

    tree = {}
    for i in range(len(string) + 1):
        suffix = string[i:] + '$'
        insert_suffix(suffix, tree)
    print("The suffixes of the given string '{}' alongside with the unique '$' character in the end are: "
          .format(string))
    print(get_suffixes(string))
    print("and the suffix tree represented as a dictionary is: ")
    return tree


def insert_suffix(string: str, suffix_tree: dict) -> dict:
    """

    A function that insert each suffix of the given string into the
    suffix tree in a `dictionary` form.

    :param string: The current suffix of string.
    :param suffix_tree:The suffix tree so far.
    :return: The suffix tree after we insert the current suffix in it.

    """
    strings = []
    if len(suffix_tree) == 0:
        suffix_tree[string] = []
        return suffix_tree

    found_match = False
    for key in list(suffix_tree):
        strings.append(key)
        strings.append(string)
        prefix = shared_prefix(strings)
        strings = []
        n = len(prefix)
        if n > 0:
            if len(suffix_tree[key]) < 2:
                found_match = True
                key_suffix = key[n:]
                string_suffix = string[n:]
                del suffix_tree[key]
                suffix_tree[prefix] = [key_suffix, string_suffix]
            elif len(suffix_tree[key]) >= 2:
                found_match = True
                strings.append(string)
                for i in range(len(suffix_tree[key])):
                    string1 = prefix + suffix_tree[key][i]
                    strings.append(string1)
                prefix = shared_prefix(strings)
                m = len(prefix)
                if m > 0:
                    suffix_tree[prefix] = [strings[i][m:] for i in range(len(strings))]

    if not found_match:
        suffix_tree[string] = []
    return suffix_tree


################################## Ukkonen #####################################


class Node:

    __num__ = -1

    def __init__(self, parent_key, out_edges, suffix_link=None):
        self.parent_key = parent_key
        self.out_edges = out_edges
        self.suffix_link = suffix_link
        Node.__num__ += 1
        self.id = Node.__num__

    def get_out_edges(self):
        return self.out_edges

    def set_out_edge(self, key, multi_args):
        anode, label_start_index, label_end_index, b_node = multi_args
        if self.out_edges is None:  # edge is not root
            self.out_edges = {}
        self.out_edges[key] = (anode, label_start_index, label_end_index, b_node)

    def get_out_edge(self, key):
        if key in self.out_edges:
            return self.get_out_edges()[key]
        else:
            return None

    def get_paren_key(self):
        return self.parent_key

    def set_parent_key(self, parent_key):
        self.parent_key = parent_key

    def get_suffix_link(self):
        return self.suffix_link

    def set_suffix_link(self, node):
        self.suffix_link = node

    def get_id(self):
        return self.id

    @staticmethod
    def __draw__(rnode, chars, v, ed='#'):
        l = len(chars)
        edges = rnode.get_out_edges().items()
        nogc = []
        hasgc = []
        gc = []
        max_len = len(chars) + 12
        for edg in edges:
            if v == 0:
                if edg[1][3].get_out_edges() is None:
                    nogc.append(edg)
                else:
                    hasgc.append(edg)
            else:
                if edg[1][3].get_out_edges() is None:
                    hasgc.append(edg)
                else:
                    nogc.append(edg)
        gc.extend(hasgc)
        gc.extend(nogc)
        for k, (parent, s, t, node) in gc:
            if ed == '#':
                if t == '#':
                    t = l
            else:
                if t == '#':
                    t = ed
            link_id = ''
            if node.get_suffix_link() is not None:
                link_id = '->' + str(node.get_suffix_link().get_id()) + '     (Suffix link)'

            if v == 0:
                print(" " * max_len * v + '|')
                print(" " * max_len * v + '|' + ' ' * 3 + chars[s:t + 1]+'  [' + str(s) + ' , ' + str(t) + ']')
                print('+' + " " * max_len * v + '-' + '-' * (max_len - 1) + '● ' + '( edge id : ' + str(node.get_id())
                      + link_id + ')')
            else:
                print('|' + " " * max_len * v + '|')
                print('|' + " " * max_len * v + '|' + ' ' * 3 + chars[s:t + 1]+'  [' + str(s) + ' , ' + str(t) + ']')
                print('|' + " " * max_len * v + '+' + '-' * (max_len - 1) + '● ' + '( edge id : ' + str(node.get_id())
                      + link_id + ')')
            if node.get_out_edges() is not None:
                Node.__draw__(node, chars, v + 1, ed)

    @staticmethod
    def draw(root, chars, ed='#'):
        print('\n', chars, '\n● (0)')
        v = 0
        Node.__draw__(root, chars, v, ed)


def build(chars: str, regularize=False):

    """

    A function that creates the suffix tree for a given string following
    Ukkonen implementation.

    :param chars: A `string` that the user defines.
    :param regularize: A boolean value that we set as `False`.
    :return: Returns the root  of `string` and the `string` itself.

    """

    root = Node(None, None, None)  # we initialize root
    act_node = root  # the node that we are
    act_key = ''  # the start of the edge that we need to follow
    act_len = 0   # how many characters we need to insert following the edge
    # the variables act_node,act_key, act_len defines the active point
    # that is the point that we are
    remainder = 0  # used for splitting and also means how many suffixes
    # we have yet to insert at current stage
    ind = 0  # starting position of string
    while ind < len(chars):  # We continue with our operations as long as we have not reached the end of our string
        ch = chars[ind]  # we get the character in current index
        if remainder == 0:  # We don't have a suffix to insert
            if act_node.get_out_edges() is not None and ch in act_node.get_out_edges():
                # We update our active point
                act_key = ch  # We set as edge the current character
                act_len = 1  # We increment the length by 1 meaning that we need to insert one more character
                # after the act_key
                remainder = 1  # We need to insert one more suffix
                anode, start, end, b_node = act_node.get_out_edge(act_key)
                if end == '#':  # check if end == #
                    end = ind  # we set end as the current index
                if end - start + 1 == act_len:  # else we update our
                    # active point
                    act_node = act_node.get_out_edge(act_key)[3]
                    act_key = ''
                    act_len = 0
            else:  # if active edge is null we continue from root
                aleaf = Node(None, None, None)
                aedge = (act_node, ind, '#', aleaf)
                aleaf.set_parent_key((act_node, chars[ind]))
                act_node.set_out_edge(chars[ind], aedge)
        else:
            if act_key == '' and act_len == 0:  # compare on node
                if ch in act_node.get_out_edges():  # if character exists
                    # in path of our edge
                    act_key = ch  # update the start of edge into this
                    # character
                    act_len = 1  # increment how many characters we need
                    # to insert by 1
                    remainder += 1  # increment how many suffixes we
                    # have yet to insert by 1
                else:  # if character don't exist in our path
                    remainder += 1  # increment how many suffixes we
                    # have yet to insert by 1
                    remainder, act_node, act_key, act_len = unfold(root, chars, ind, remainder, act_node, act_key,
                                                                   act_len)
                    # we create an internal node
            else:  # compare on edge
                anode, start, end, b_node = act_node.get_out_edge(act_key)
                if end == '#':
                    end = ind
                compareposition = start + act_len  # the number of
                # characters within the path that we follow
                if chars[compareposition] != ch:  # character at
                    # compareposition different than current character
                    remainder += 1  # increment remainder
                    remainder, act_node, act_key, act_len = unfold(root, chars, ind, remainder, act_node, act_key,
                                                                   act_len)
                    # create an internal node
                else:  # current character equals with character at
                    # compare position
                    if compareposition < end:  # on edge
                        # update active point
                        act_len += 1
                        remainder += 1
                    else:  # on node
                        # update active point
                        remainder += 1
                        act_node = act_node.get_out_edge(act_key)[3]
                        if compareposition == end:  # if we reached the
                            # end we go back to root
                            act_len = 0
                            act_key = ''
                        else:
                            # update active point
                            act_len = 1
                            act_key = ch
        ind += 1  # increment ind by 1 to get the next character
        # of string
        if ind == len(chars) and remainder > 0:  # we reached the end
            # of our string and we have yet to insert a suffix
            if regularize:
                chars = chars + '$'  # add the unique character '$' so
                # that we get a non implicit suffix tree
    return root, chars


def unfold(root, chars, ind, remainder, act_node, act_key, act_len):

    """

    A function that is used when one of the two rules applies,
    in order to create an internal node.

    Rule1:

    When we insert a character from the root:
      ->root remains as active node

      ->active edge is the first character of the new suffix that we
      need to insert

      ->active length decrements by 1

    Rule2:

     when we split a path from an active node that is not root
     we follow the suffix link that this node indicates if it exists and
     set the node to whom it shows as active node. If there is no suffix
     link we set as active node the root and we keep active edge and
     active length unchanged


    :param root: The start of our tree.
    :param chars: The characters that we have yet to insert.
    :param ind: The index of current character.
    :param remainder: How many suffixes we need to insert.
    :param act_node: The current node.
    :param act_key: The start of the edge that we need to follow.
    :param act_len: How many characters we need to insert following
                    the edge.

    """

    pre_node = None  # we don't have an internal node yet.
    while remainder > 0:
        remains = chars[ind - remainder + 1:ind + 1]
        act_len_re = len(remains) - 1 - act_len
        act_node, act_key, act_len, act_len_re = hop(ind, act_node, act_key, act_len, remains, act_len_re)
        lost, act_node, act_key, act_len, act_len_re = step(chars, ind, act_node, act_key, act_len, remains, act_len_re)
        if lost:
            if act_len == 1 and pre_node is not None and act_node is not root:
                pre_node.set_suffix_link(act_node)
            return remainder, act_node, act_key, act_len
        if act_len == 0:  # we have no more characters to insert
            if remains[act_len_re] not in act_node.get_out_edges():
                aleaf = Node(None, None, None)
                aedge = (act_node, ind, '#', aleaf)
                aleaf.set_parent_key((act_node, chars[ind]))
                act_node.set_out_edge(chars[ind], aedge)
        else:  # on edge
            anode, start, end, b_node = act_node.get_out_edge(act_key)
            if remains[act_len_re + act_len] != chars[start + act_len]:
                # split
                anode, start, end, b_node = act_node.get_out_edge(act_key)
                new_node = Node(None, None, None)
                half_edge1 = (act_node, start, start + act_len - 1, new_node)
                half_edge2 = (new_node, start + act_len, end, b_node)
                act_node.set_out_edge(act_key, half_edge1)
                new_node.set_parent_key((act_node, act_key))
                new_node.set_out_edge(chars[start + act_len], half_edge2)
                aleaf = Node(None, None, None)
                aedge = (new_node, ind, '#', aleaf)
                aleaf.set_parent_key((new_node, chars[ind]))
                new_node.set_out_edge(chars[ind], aedge)
            else:
                return remainder, act_node, act_key, act_len
        if pre_node is not None and 'aleaf' in locals() and aleaf.get_paren_key()[0] is not root:
            pre_node.set_suffix_link(aleaf.get_paren_key()[0])
        if 'aleaf' in locals() and aleaf.get_paren_key()[0] is not root:
            pre_node = aleaf.get_paren_key()[0]
        if act_node == root and remainder > 1:
            act_key = remains[1]
            act_len -= 1
        if act_node.get_suffix_link() is not None:  # Rule1
            act_node = act_node.get_suffix_link()
        else:  # Rule2
            act_node = root
        remainder -= 1
    return remainder, act_node, act_key, act_len


def step(chars, ind, act_node, act_key, act_len, remains, ind_remainder):

    """

    A function that is used when the active node is right, but the next operation
    should be imposed in the middle of the edge so we need to move char-by-char on
    the edge to the right position.

    :param chars: The characters that we have yet to insert.
    :param ind: The index of current character.
    :param act_node: The current node.
    :param act_key: The start of the edge that we need to follow.
    :param act_len: How many characters we need to insert following
                    the edge.
    :param remains: Suffixes we have yet to insert.
    :param ind_remainder: How many suffixes we have yet to insert.

    """

    rem_label = remains[ind_remainder:]
    if act_len > 0:
        anode, start, end, b_node = act_node.get_out_edge(act_key)
        if end == '#':
            end = ind
        edge_label = chars[start:end + 1]
        if edge_label.startswith(rem_label):
            act_len = len(rem_label)
            act_key = rem_label[0]
            return True, act_node, act_key, act_len, ind_remainder
    else:
        # on node
        if ind_remainder < len(remains) and remains[ind_remainder] in act_node.get_out_edges():
            anode, start, end, b_node = act_node.get_out_edge(remains[ind_remainder])
            if end == '#':
                end = ind
            edge_label = chars[start:end + 1]
            if edge_label.startswith(rem_label):
                act_len = len(rem_label)
                act_key = rem_label[0]
                return True, act_node, act_key, act_len, ind_remainder
    return False, act_node, act_key, act_len, ind_remainder


def hop(ind, act_node, act_key, act_len, remains, ind_remainder):
    """

    A function that is used when we have to hop node-by-node until we reach
    the actual node to do the next operation.

    :param ind:  The index of current character.
    :param act_node:  The current node.
    :param act_key: The start of the edge that we need to follow.
    :param act_len: How many characters we need to insert following
                    the edge.
    :param remains: Suffixes we have yet to insert.
    :param ind_remainder: How many suffixes we have yet to insert.

    """

    if act_len == 0 or act_key == '':
        return act_node, act_key, act_len, ind_remainder
    anode, start, end, b_node = act_node.get_out_edge(act_key)
    if end == '#':
        end = ind
    edge_length = end - start + 1
    while act_len > edge_length:
        # update active point
        act_node = act_node.get_out_edge(act_key)[3]
        ind_remainder += edge_length
        act_key = remains[ind_remainder]
        act_len -= edge_length
        anode, start, end, b_node = act_node.get_out_edge(act_key)
        if end == '#':
            end = ind
        edge_length = end - start + 1
    if act_len == edge_length:
        #  update active point
        act_node = act_node.get_out_edge(act_key)[3]
        act_key = ''
        act_len = 0
        ind_remainder += edge_length
    return act_node, act_key, act_len, ind_remainder


############################### McCreight ######################################


import itertools


class SuffixNode(object):

    def __init__(self, text: str):  # the text is the string for which
        # we want to create the tree and is defined from the user.
        self.children = {}  # children node
        self.parent = None  # we define parent node as None
        self.suffix_link = None  # we define suffix link as None
        self.i_from = 0  # we initialize i_from to 0
        self.i_to = 0  # we initialize i_to to 0
        self.text = text  # we get the text

    @property
    def length(self):
        return self.i_to - self.i_from  # the length from i_to character
        # to i_from character

    def add(self, i_from, i_to):
        child = SuffixNode(self.text)  # The child is the SuffixNode
        # from text[i_from to i_to]
        child.i_from = i_from  # i_from of child = i_from
        child.i_to = i_to  # i_to of child = i_to
        child.parent = self  # parent of child
        self[self.text[i_from]] = child
        return child

    def split(self, i_split):
        i_from = self.i_from  # the position of first character
        i_to = self.i_to  # the position of final character
        assert i_split > i_from  # check
        assert i_split < i_to  # check
        self.i_to = i_split  # we set i_to to i_split
        child = SuffixNode(self.text)  # SuffixNode from
        # text[i_from to i_to] is the child
        child.i_from = i_split
        child.i_to = i_to
        child.parent = self
        child.children = self.children
        self.children = {}  # create the next empty children node
        self[self.text[i_from]] = child  # we set text to
        # SuffixNode(text[i_split to i_to])

    @property
    def label(self):
        return repr(self.text[self.i_from: self.i_to])  # label of the
        # substring [i_from, i_to]

    def __getitem__(self, ident):
        return self.children[ident]  # children ident node

    def __setitem__(self, ident, child):
        self.children[ident] = child  # set children[ident] node
        # to child

    def __str__(self, indent=0):
        # we create the string and all of its substrings
        return '%s%s\n%s' % (
            indent * '  ',
            self.label,
            ''.join(
                child.__str__(indent + 1)
                for key, child in sorted(self.children.items())
            )
        )


def mc_creight(text):

    print("The tree for text '{}' is : \n".format(text))

    def fast_scan(node, i_from, i_to):

        """

        This function helps us jump from node to node in case we know
        that `y` string is substring of text[i_from,i_to]

        """

        assert node is not None  # check if node exists
        length = i_to - i_from  # set length of substring to
        # [i_to - i_from]
        assert length >= 0  # checking if length is positive
        if length == 0:  # in this case we have no node so we return
            # the node alongside its number
            return node, node.i_from
        node = node[text[i_from]]  # we set our node to node[text[i_from]]
        # which indicates the next node
        while length > node.length:  # traverse through the path until
            # we reach the end
            i_from += node.length  # move to the next character
            length -= node.length  # we decrement node.length by one in
            # order to reach the end
            node = node[text[i_from]]  # we define our next node
        return node, node.i_from + length

    def slow_scan(node, i_from, i_to):

        """

        This function tells us that we have to search character by
        character in case that we don't know if `y` string is substring
        of text[i_from,i_to]

        """

        assert node is not None  # check if node exists
        assert i_from <= i_to  # check if we haven't reached the end
        delta = 0  # we use this variable to increase the number in
        # order to show to the next character
        loop = True  # meaning that we haven't reached the end
        try:
            node = node[text[i_from]]
            while i_from < i_to and loop:  # searching character by
                # character
                if node.i_from + delta < node.i_to:  # still haven't
                    # reached the end
                    # current character equals next character
                    if text[i_from] == text[node.i_from + delta]:
                        delta += 1
                        i_from += 1  # we move to the next character
                    else:
                        break
                else:  # we reached the end
                    delta = 0
                    node = node[text[i_from + delta]]  # set node
                    # to node[text[i_from + delta]]
        except KeyError:
            pass
        if delta > 0:
            node.split(node.i_from + delta)  # split the string node
        leaf = node.add(i_from, i_to)  # and we take a leaf[i_from, i_to]
        return node, leaf

    text_len = len(text)  # length of text
    root = SuffixNode(text)
    head = root  # set head as root
    leaf = root.add(0, text_len)  # create a leaf from root to text
    # length indicating the suffix of text equals to its length.
    for j in range(1, text_len):  # we traverse character by character
        if head == root:  # if head equals root then we use slow_scan
            # function
            head, leaf = slow_scan(root, leaf.i_from + 1, leaf.i_to)
            continue
        parent = head.parent  # set new parent node
        if parent == root:  # if parent is root
            # we use fast_scan function from root+1 node[head(i_from+1)]
            # to head(i_to)] node
            head_sl, i = fast_scan(parent, head.i_from + 1, head.i_to)
        else:
            # we use fast_scan method from parent.suffix_link node[head
            # (i_from) to head(i_to)] node
            head_sl, i = fast_scan(parent.suffix_link, head.i_from, head.i_to)
        if i < head_sl.i_to:
            # s(head) is in the middle of an edge
            head_sl.split(i)  # we split the string
            new_head = head_sl  # we get new head and add a leaf
            leaf = new_head.add(leaf.i_from, leaf.i_to)
        else:
            # s(head) is a node and search character by character with
            # slow scan function
            new_head, leaf = slow_scan(head_sl, leaf.i_from, leaf.i_to)
        head.suffix_link = head_sl  # new node_suffix link is head_sl
        head = new_head  # we set as our head the head that slow scan
        # function returns

    return root


########################### String_matching_finite_automata ####################


def next_state(pattern: str, m: int, state: int, ascii_value: int) -> int:

    """

    A function that help us calculate the next state we get after the
    addition of each one of the different characters of pattern.Given
    a character x and a state k, we can get the next state by
    considering the string “pat[0..k-1]x” which is basically
    concatenation of pattern characters pat[0], pat[1] ... pat[k-1]
    and the character x.

    :param pattern: A `string` that the user defines.
    :param m: The length of pattern.
    :param state: Current state.
    :param ascii_value: The ASCII value for each one of the different
                        characters of pattern.
    :return: Next state we get after the addition of one of the
             different characters of pattern.

    """

    # If the character x is same as next character
    # in pattern, then simply increment state

    if state < m and ascii_value == ord(pattern[state]):
        return state + 1

    i = 0

    # ns tells us which is the next state

    # ns contains the longest prefix
    # which is also suffix in "pat[0..state-1]x"

    # Start from the largest possible value and
    # stop when you find a prefix which is also suffix
    for ns in range(state, 0, -1):
        if ord(pattern[ns - 1]) == ascii_value:
            while i < ns - 1:
                if pattern[i] != pattern[state - ns + 1 + i]:
                    break
                i += 1
            if i == ns - 1:
                return ns
    return 0


def compute_finite_automata_table(pattern: str, m: int, different_characters: list) -> list:

    """

    A function that calculates the finite automata table for the pattern.

    :param pattern: A `string` that the user defines.
    :param m: The length of pattern.
    :param different_characters: A list containing the different characters
                                 of pattern.
    :return: A 2D list representing the finite automata of pattern.

    """

    # we initialize our table with 0 at the beginning
    finite_automata_table = [[0 for i in range(len(different_characters))] for j in range(m+1)]

    for state in range(m+1):
        for x in range(len(different_characters)):
            # we get the ASCII values for the characters of pattern.
            ascii_value = ord(different_characters[x])
            # we calculate which state we get with the addition of each one of the
            # different characters of pattern
            z = next_state(pattern, m, state, ascii_value)
            # we store next state in our finite automata
            finite_automata_table[state][x] = z

    # print our finite automata
    print("Finite automata table: ")
    print("       ", end=" ")
    for k in range(len(different_characters)):
        print(different_characters[k], end=" ")
    for i in range(m+1):
        print("\nstate{}:".format(i), end=" ")
        for j in range(len(different_characters)):
            print(finite_automata_table[i][j], end=" ")
        if i == m:
            print("\n")

    return finite_automata_table


def finite_automata_pattern_search(pattern: str, text: str) -> None:

    """

    A function that searches for occurrences of pattern inside a text
    with the help of finite automatas. First we construct the finite
    automata for the pattern and then we check character-by-character
    what state we get with the addition of each character of text.If
    we reach the final state which is equal with the length of
    pattern + 1 then the pattern was found inside text.

    :param pattern: A `string` that the user defines.
    :param text: A `string` that the user defines.

    """

    m = len(pattern)
    n = len(text)
    # a dictionary in which we store key value pairs for the different characters
    # of pattern
    characters = {}
    # a list that stores the different characters of pattern
    different_characters = []
    k = 0
    # fill the dictionary
    for i in range(m):
        # if the current character of pattern not in dictionary then store it
        if pattern[i] not in characters:
            characters[pattern[i]] = k
            k += 1
    # fill the list
    for key in characters:
        different_characters.append(key)

    # construction of finite automata for pattern
    finite_automata = compute_finite_automata_table(pattern, m, different_characters)

    # Search in text for pattern

    pattern_occurrences = []  # a list that stores the index on text in which pattern was found
    state = 0  # first state
    y = - 100
    for i in range(n):
        # if current character of text not exist in pattern we always return to state 0
        if text[i] not in different_characters:
            state = 0
        else:
            # we check with the help of the finite automata in which state
            # we go with current character of text
            for key, value in characters.items():
                if text[i] == key:
                    y = value
            state = finite_automata[state][y]
        # we reached final state so pattern was found
        if state == m:
            pattern_occurrences.append(i - m + 1)

    # print the results

    if len(pattern_occurrences) == 0:
        print("The pattern '{}' was not found in text '{}'.".format(pattern, text))
    else:
        if len(pattern_occurrences) == 1:
            print("The pattern '{}' was found in '{}' {} time and specifically at position {}.".
                  format(pattern, text, len(pattern_occurrences), pattern_occurrences[0]))
        else:
            print("The pattern '{}' was found in '{}' {} times and specifically at positions {}.".
                  format(pattern, text, len(pattern_occurrences), pattern_occurrences))


############################## Aho_corasick ####################################


# defaultdict is used only for storing the final output
# We will return a dictionary where key is the matched word
# and value is the list of indexes of matched word
from collections import defaultdict


# For simplicity, Arrays and Queues have been implemented using lists.
class AhoCorasick:
    def __init__(self, words):

        # Max number of states in the matching machine.
        # Should be equal to the sum of the length of all keywords.
        self.max_states = sum([len(word) for word in words])

        # Maximum number of characters.
        self.max_characters = 26

        # OUTPUT FUNCTION IS IMPLEMENTED USING out []
        # Bit i in this mask is 1 if the word with
        # index i appears when the machine enters this state.
        # Lets say, a state outputs two words "he" and "she" and
        # in our provided words list, he has index 0 and she has index 3
        # so value of out[state] for this state will be 1001
        # It has been initialized to all 0.
        # We have taken one extra state for the root.
        self.out = [0]*(self.max_states+1)

        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        # There is one value for each state + 1 for the root
        # It has been initialized to all -1
        # This will contain the fail state value for each state
        self.fail = [-1]*(self.max_states+1)

        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        # Number of rows = max_states + 1
        # Number of columns = max_characters
        # It has been initialized to all -1.
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]

        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
            words[i] = words[i].lower()

        # All the words in dictionary which will be used to create Trie
        # The index of each keyword is important:
        # "out[state] & (1 << i)" is > 0 if we just found word[i]
        # in the text.
        self.words = words

        # Once the Trie has been built, it will contain the number
        # of nodes in Trie which is total number of states required <= max_states
        self.states_count = self.__build_matching_machine()


    # Builds the String matching machine.
    # Returns the number of states that the built machine has.
    # States are numbered 0 up to the return value - 1, inclusive.
    def __build_matching_machine(self):
        k = len(self.words)

        # Initially, we just have the 0 state
        states = 1

        # Convalues for goto function, i.e., fill goto
        # This is same as building a Trie for words[]
        for i in range(k):
            word = self.words[i]
            current_state = 0

            # Process all the characters of the current word
            for character in word:
                ch = ord(character) - 97  # Ascii value of 'a' = 97

                # Allocate a new node (create a new state)
                # if a node for ch doesn't exist.
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1

                current_state = self.goto[current_state][ch]

            # Add current word in output function
            self.out[current_state] |= (1 << i)

        # For all characters which don't have
        # an edge from root (or state 0) in Trie,
        # add a goto edge to state 0 itself
        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0

        # Failure function is computed in
        # breadth first order using a queue
        queue = []

        # Iterate over every possible input
        for ch in range(self.max_characters):

            # All nodes of depth 1 have failure
            # function value as 0. For example,
            # in above diagram we move to 0
            # from states 1 and 3.
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        # Now queue has states 1 and 3
        while queue:

            # Remove the front state from queue
            state = queue.pop(0)

            # For the removed state, find failure
            # function for all those characters
            # for which goto function is not defined.
            for ch in range(self.max_characters):

                # If goto function is defined for
                # character 'ch' and 'state'
                if self.goto[state][ch] != -1:

                    # Find failure state of removed state
                    failure = self.fail[state]

                    # Find the deepest node labeled by proper
                    # suffix of String from root to current state.
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]

                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure

                    # Merge output values
                    self.out[self.goto[state][ch]] |= self.out[failure]

                    # Insert the next level node (of Trie) in Queue
                    queue.append(self.goto[state][ch])

        return states


    # Returns the next state the machine will transition to using goto
    # and failure functions.
    # current_state - The current state of the machine. Must be between
    #             0 and the number of states - 1, inclusive.
    # next_input - The next character that enters into the machine.


    def __find_next_state(self, current_state, next_input):
        answer = current_state
        ch = ord(next_input) - 97  # Ascii value of 'a' is 97

        # If goto is not defined, use
        # failure function
        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]

        return self.goto[answer][ch]


    # This function finds all occurrences of all words in text.
    def search_words(self, text: str):
        # Convert the text to lowercase to make search case insensitive
        text = text.lower()

        # Initialize current_state to 0
        current_state = 0

        # A dictionary to store the result.
        # Key here is the found word
        # Value is a list of all occurrences start index
        result = defaultdict(list)

        # Traverse the text through the built machine
        # to find all occurrences of words
        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])

            # If match not found, move to next state
            if self.out[current_state] == 0: continue

            # Match found, store the word in result dictionary
            for j in range(len(self.words)):
                if (self.out[current_state] & (1<<j)) > 0:
                    word = self.words[j]

                    # Start index of word is (i-len(word)+1)
                    result[word].append(i-len(word)+1)

        # Return the final result dictionary
        return result


def results(words: list, text: str) -> None:
    """

    A function to print out the results.

    :param words: A list of words that the user defines.
    :param text: The `string` in which we have to check if the words
                 appearing. The user defines it too.

    """

    # Create an Object to initialize the Trie
    aho_chorasick = AhoCorasick(words)

    # Get the result
    result = aho_chorasick.search_words(text)


    # Print the result
    for word in result:
        for i in result[word]:
            print("Word '{}' appears in text '{}' starting from index"
                  " {} to {}.".format(word, text, i, i+len(word)-1))
