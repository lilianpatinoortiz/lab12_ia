# TC2011 - Bayes Network Lab

## Setup

Before you begin, perform the following two steps:

- [Install autograder](https://github.com/rhomeister/autograder#for-students)
- [Setup your git repository](https://github.com/rhomeister/autograder#installation)


## Querying a Bayes Network

For this lab, you have to write a program to Query a Bayes Network

### Objective 

Your assignment is to build a program that reads the structure and probability
tables of a Bayes Network, and then query it. Querying a Bayes network means to
compute the probability of the query variables being true, given certain
evidence.

### Input/Output
Your program must read from `stdin` and output to `stdout`. See
[here](https://github.com/rhomeister/autograder#the-required-structure-of-a-project)
for instructions how to do this.

Basically, your program will be called by executing `run < [problem_file]`,
where `problem_file` is a file describing the problem (see below). Your program
should output the solution as text to the terminal.

#### Input

The input consists of three sections:

1. **Nodes**: a list of variable nodes in the Bayes Network, separated by a
   comma.
2. **Probabilities**: the probability tables associated variable nodes. Entries
   of a probability table have the following format:

   `VariableAssignment [| [VariableAssigment]*]? = Probability`

   This encodes the probability of a variable being true, given its parent nodes
   in the Bayes Network having a certain value.

   A VariableAssignment is formatted as `[+-]VariableName`. When preceded by a 
   +, it means that the variable is true. A minus (-) indicates the variable is
   false.
3. **Queries**: one or more queries. A query has the following format

   `[QueryAssignment]* [| [EvidenceAssigment]*]?`

   Both QueryAssignment and EvidenceAssigment are VariableAssigments.

   A query basically requests your program to compute the probability of the 
   query variables having a certain value, given the evidence variables having a
   certain value.

#### Output

Output consists multiple lines, one per query. For each query, output the
probability, rounded to 7 digits.

### Example

The following example encodes a Bayes network for a simple diagnostics test to
determine whether a patient is ill.

The network consists of two nodes: "Ill" and "Test". There is one edge from
"Ill" to "Test".

There are 3 queries defined.

Input:
```
[Nodes]
Test, Ill

[Probabilities]
+Ill = 0.001
+Test|+Ill=0.9
+Test|-Ill=0.05

[Queries]
+Ill
-Ill|+Test
+Test|+Ill
```

Output:
```
0.001
0.9823009
0.9
```

More examples can be found in the `testcases` directory
