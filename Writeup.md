# Homework 5

1. Laplace smoothing works by having unknown characters or letters (things that don't show up in the training data) have a small amount of probability. We would need to have this for prob method to work because if we're doing the log probability, then we'll need to take logs but if a prob is 0, then log of that would be undefined and break our code.

2. The command line interface for EditDistance.py requires you to write a store source which is where we'll put our probabilities. Then we have an optional input for source. If we put in a source, then we'll be training on that file. If we don't put a source, we'll use no training data and we'll just assign equal probabilities (due to our Laplace Smoothing) for every insert, delete, and substitution. To run the desired script, we will use: python3 EditDistance.py --store ed.pkl --source /data/spelling/wikipedia_misspellings.txt

3. Looking at LanguageModel.py, it supports bigram and monogram models.

4. The class deals with 0-counts by adding an alpha value to all the words probabilities.

5. The "__contains__" method checks if the word is in the vocabulary or not. This allows us to do things like "if word in self" to check instead of "if word in self.vocab"

6. We're limiting the amount of text we're processing by breaking things down into chunks with the get_chunks method that is defaulted to 100,000 words.

7. python3 LanguageModel.py --store lm.pkl ../data/gutenberg/*.txt

6. I couldn't figure out how diff worked. But just from looking at the first few examples, I feel like our spell checker did not work nearly as well as the ispell spellchecker

7. ispell seemed to work well with things that were one edit distance away (one sub, one del, one transposition). Our spell checker only seemed to do well on the examples that were in our training data

8. I probably did it the assignment wrong, but the spell checker was waaaaay off on a lot of things.

9. I didn't have time to implement one, but if I did, I would do transpositions. I would probably have to modify EditDistance.py in order to account for the difference in cost. Afterwards, I would have to modify the SpellChecker.py to include transpositions as something that was one edit away.

10. N/A

11. N/A