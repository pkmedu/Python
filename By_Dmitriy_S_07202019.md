

```python

```

[Class code for Aviation - July 20, 2019 by Dimitriy Synkrov](https://github.com/dcpylab/classes/tree/master/2019-07/20)


```python
""" Get alphabet from -> https://en.wikipedia.org/wiki/NATO_phonetic_alphabet """

source = "Alfa, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India, Juliett, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, X-ray, Yankee, Zulu"

""" First, clean up our source material """

words = source.split(",")

# Using list comprehension
clean_words = [word.lower().strip() for word in words]
clean_words
```




    ['alfa',
     'bravo',
     'charlie',
     'delta',
     'echo',
     'foxtrot',
     'golf',
     'hotel',
     'india',
     'juliett',
     'kilo',
     'lima',
     'mike',
     'november',
     'oscar',
     'papa',
     'quebec',
     'romeo',
     'sierra',
     'tango',
     'uniform',
     'victor',
     'whiskey',
     'x-ray',
     'yankee',
     'zulu']




```python
# Using for loop
clean_words = []
for word in words:
    clean_words.append(word.lower().strip())
    print(clean_words)
```

    ['alfa']
    ['alfa', 'bravo']
    ['alfa', 'bravo', 'charlie']
    ['alfa', 'bravo', 'charlie', 'delta']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'x-ray']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'x-ray', 'yankee']
    ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'x-ray', 'yankee', 'zulu']
    


```python
# Using map and lambda combo
clean_words = list(map(lambda w: w.lower().strip(), words))

""" Then get the letters of the alphabet in a separate list """

# Using list comprehension
letters = [word[0] for word in clean_words]
letters
```




    ['a',
     'b',
     'c',
     'd',
     'e',
     'f',
     'g',
     'h',
     'i',
     'j',
     'k',
     'l',
     'm',
     'n',
     'o',
     'p',
     'q',
     'r',
     's',
     't',
     'u',
     'v',
     'w',
     'x',
     'y',
     'z']




```python

```


```python
# Alternatively, using `string` library
import string
letters = list(string.ascii_lowercase)
letters
```




    ['a',
     'b',
     'c',
     'd',
     'e',
     'f',
     'g',
     'h',
     'i',
     'j',
     'k',
     'l',
     'm',
     'n',
     'o',
     'p',
     'q',
     'r',
     's',
     't',
     'u',
     'v',
     'w',
     'x',
     'y',
     'z']




```python
""" Zip the two list together to create a dictionary """
nato = dict(zip(letters, clean_words))
nato
```




    {'a': 'alfa',
     'b': 'bravo',
     'c': 'charlie',
     'd': 'delta',
     'e': 'echo',
     'f': 'foxtrot',
     'g': 'golf',
     'h': 'hotel',
     'i': 'india',
     'j': 'juliett',
     'k': 'kilo',
     'l': 'lima',
     'm': 'mike',
     'n': 'november',
     'o': 'oscar',
     'p': 'papa',
     'q': 'quebec',
     'r': 'romeo',
     's': 'sierra',
     't': 'tango',
     'u': 'uniform',
     'v': 'victor',
     'w': 'whiskey',
     'x': 'x-ray',
     'y': 'yankee',
     'z': 'zulu'}




```python


def get_phonetic_simple(word):
    """ 
    Translates string into phonetic alphabet.
    """

    translation = [nato[letter].title() for letter in word]
    return ' '.join(translation)

```


```python
word = input("Select a word that you would like to translate: ")
translation = get_phonetic_simple(word)
print("The phonetic spelling of '%s' is: '%s'." % (word, translation))

```

    Select a word that you would like to translate:  Python
    


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-19-8446f816ede4> in <module>
          1 word = input("Select a word that you would like to translate: ")
    ----> 2 translation = get_phonetic_simple(word)
          3 print("The phonetic spelling of '%s' is: '%s'." % (word, translation))
    

    <ipython-input-18-fd524af784d0> in get_phonetic_simple(word)
          6     """
          7 
    ----> 8     translation = [nato[letter].title() for letter in word]
          9     return ' '.join(translation)
    

    <ipython-input-18-fd524af784d0> in <listcomp>(.0)
          6     """
          7 
    ----> 8     translation = [nato[letter].title() for letter in word]
          9     return ' '.join(translation)
    

    KeyError: 'P'



```python
word_with_spaces = input("Now, select a word with spaces: ")
translation_with_spaces = get_phonetic_complete(word_with_spaces)
print("The phonetic spelling of '%s' is: '%s'." % (
    word_with_spaces, 
    translation_with_spaces
))
```

    Now, select a word with spaces:  DC Python
    


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-20-3da6be464f72> in <module>
          1 word_with_spaces = input("Now, select a word with spaces: ")
    ----> 2 translation_with_spaces = get_phonetic_complete(word_with_spaces)
          3 print("The phonetic spelling of '%s' is: '%s'." % (
          4     word_with_spaces,
          5     translation_with_spaces
    

    NameError: name 'get_phonetic_complete' is not defined



```python
word_with_digits = input("Now, select phrase with digits: ")
# This part will throw a TypeError because we cannot transate digits
translation_with_digits = get_phonetic_complete(word_with_digits)
```

    Now, select phrase with digits:  Python101
    


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-21-3be4ed9019ba> in <module>
          1 word_with_digits = input("Now, select phrase with digits: ")
          2 # This part will throw a TypeError because we cannot transate digits
    ----> 3 translation_with_digits = get_phonetic_complete(word_with_digits)
    

    NameError: name 'get_phonetic_complete' is not defined


# 
