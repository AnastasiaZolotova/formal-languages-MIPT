# formal-languages

## Practical task No. 1. Regular expressions
In the task, it is necessary to implement some algorithm for processing regular expressions.
Further, it is assumed that the first component of the input is the regular expression α in the reverse Polish notation, specifying the language L. The alphabet for all tasks is {a, b, c}

### Problem condition: 
α and the word u {a, b, c} are given. Find the length of the longest subword u, which is also a subword of some word in L.

## Proof of the algorithm's operability.
Note that any subword of the word u is a prefix of some suffix u. The algorithm is that we iterate through all possible suffixes, get into all states and run this suffix through the automaton. Due to the fact that we start not only from the starting state, but from any one, we can get the maximum prefix as a subword of a word of L.
