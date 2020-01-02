# The Allocator


    ████████╗██╗  ██╗███████╗
    ╚══██╔══╝██║  ██║██╔════╝
       ██║   ███████║█████╗
       ██║   ██╔══██║██╔══╝
       ██║   ██║  ██║███████╗
       ╚═╝   ╚═╝  ╚═╝╚══════╝              -v1.0 by @amirootyet

     █████╗ ██╗     ██╗      ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗
    ██╔══██╗██║     ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    ███████║██║     ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
    ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
    ██║  ██║███████╗███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═

```sh
usage: allocator.py [-h] [-a] [-b] -f FILENAME [-c]
```



This command-line utility was written to tackle the problem of assigning TAs to CSE 231 lab sections at Michigan State University according to preferences. The Allocator expects a CSV with TA preferences as input and produces lab assignments as output.

## Description

This is a linear sum assignment problem that can be interpreted as minimum weight matching in a bipartite graph where <em> N </em> workers need to be assigned <em> M </em> jobs while minimizing cost. The objective function is, hence, a cost function that needs to be minimized while completing a one-to-one assignment of each TA to a lab section. The cost associated with assigning a TA a lab section depends on the TA's preferences indicated in the CSV file. For instance, a high cost is incurred while assigning a TA a lab section that they have marked as as 'conflict.'

The problem instance is thus formulated as a cost matrix C, such that each element $C[x,y]$ in the cost matrix represents the cost of assigning TA <em> x </em> ('worker') a lab section <em> y </em> ('job'). The optimal assignment to this problem has the minimal cost denoted by:

![preferences](/screenshots/function.png?raw=true)


A naive way of solving this problem would be to bruteforce all possible combinations of assignments of TAs to lab sections / time slots and then calculating and comparing the associated costs. For an <em> n x n </em> assignment, there are <em> n </em> choices for the first assignment, <em> n-1 </em> for the next, resulting in an exponential complexity! The Hungarian algorithm allows us to solve this problem in polynomial time.


## Features
	- minimum cost assignment in polynomial time.
	- one-to-one mapping of labs / sections to TAs.
	- abililty to handle rectangular matrices, N x M
	- finds "busy bees" or TAs with 'conflicts' marked
		for more half of the total time slots.

## Installation

```sh
git clone https://github.com/amirootyet/the_allocator.git
```

## Usage

```sh
usage: allocator.py [-h] [-a] [-b] -f FILENAME [-c]

A utility to manage CSE 231 TA assignment with the Munkres algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -a, --assign          Read the preferences CSV and create assignments.
  -b, --busybees        Find TAs that have a conflict for more than halfof the total work slots.
  -f FILENAME, --filename FILENAME
                        CSV file containing TA preferences.
  -c, --costmatrix      Build and display the TA cost matrix.
```

Cost are hard-coded in `allocator.py` and can be modified:

```sh
COSTS = {
    'Preferred': 1,
    'Available but not preferred': 5,
    'Conflict': 100
}
```

TAs can be assigned two lab sections instead of one by modifying (uncomment and add TAs) the following set:

```sh
TAs_WITH_TWO_LABS = (
#        'TA1',
#        'TAs',
)
```

The allocator will then automatically create clones of these TAs and assign them sections. The clones are marked by asterisk (\*).

## Examples

```sh
python allocator.py -f preferences.csv
```

![preferences](/screenshots/nothing_to_do.jpg?raw=true)

```sh
python allocator.py -f preferences.csv --busybees
```

![preferences](/screenshots/busy_bees.jpg?raw=true)

```sh
python allocator.py -f preferences.csv --costmatrix
```

![preferences](/screenshots/cost_matrix.jpg?raw=true)

```sh
python allocator.py -f preferences.csv --assign
```

![preferences](/screenshots/ta_assignment.jpg?raw=true)


## References

	- https://en.wikipedia.org/wiki/Hungarian_algorithm
	- http://csclab.murraystate.edu/~bob.pilgrim/445/munkres.html
	- https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
	- https://github.com/bmc/munkres
	- https://www.youtube.com/watch?v=cQ5MsiGaDY8

License
----

MIT