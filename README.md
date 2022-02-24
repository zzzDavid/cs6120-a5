# CS6120-A5

This repository contains utilities to analyze dominance.

## Usage
```
❯ python main.py -h
usage: main.py [-h] [-dom] [-domtree] [-frontier] [-worklist] [-verify]
               [-visualize] [-f FILENAME]

optional arguments:
  -h, --help   show this help message and exit
  -dom         print dominator
  -domtree     print dominance tree
  -frontier    print dominance frontier
  -worklist    use worklist algorithm to find dominators
  -verify      verify dominance result
  -visualize   visualize results
  -f FILENAME  json file
```

Run with Bril utilities:

```
$ bril2json < dom/*.bril | python main.py {-arg} 
```

To run all tests with `turnt`: 
```
❯ turnt dom/*.bril
```

## Ideas
### Finding dominators
I followed the pseudo code to take intersection of each predecessors's dominator and adding itself. 
### Build dominance tree
The idea is to identify the immediate dominators in each node's set of dominators. My implementation checks if a vertex's dominator dominates other dominators in the set, if it doesn't, then it's an immediate dominator. 
### Find domination frontier
My implementation checks the successors of vertices dominated by the current vertex. If it is not dominated by the current vertex, it's in the frontier.

A new thing for me is that a vertex's dominance frontier can contain itself. 

### Verification
I implemented a verifier to check if the domination relation is correct. For a given vertex and its dominators, the verifier visits all the predecessors of the vertex and make sure every upstream path goes through every dominator. If any upstream path doesn't go through a dominator when it meets the root (entry) block, the verification fails.

## CFG and Dominance Tree Visualization

I find graphviz is a great visualizer for CFGs. This repo comes with a visualizer that plots CFG and Basic Blocks for any given Bril function. 

<p align="center">
<img width=80% alt="Screen Shot 2022-02-23 at 21 57 20" src="https://user-images.githubusercontent.com/33577135/155449254-fc60c859-3c5a-4293-b05c-af66eed0b445.png">
</p>
