# Homework 5

1. Laplace smoothing works by having unknown characters or letters (things that don't show up in the training data) have a small amount of probability. We would need to have this for prob method to work because if we're doing the log probability, then we'll need to take logs but if a prob is 0, then log of that would be undefined and break our code.

2. The command line interface for EditDistance.py requires you to write a store source which is where we'll put our probabilities. Then we have an optional input for source. If we put in a source, then we'll be training on that file. If we don't put a source, we'll use no training data and we'll just assign equal probabilities (due to our Laplace Smoothing) for every insert, delete, and substitution

3. 

4. 

5.