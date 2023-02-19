# Combining ML and SNA to reveal organizational structure
This work represents a simplified version of code designed to combine ML(Machine Learning) and SNA(Social Network Analysis) to reveal organizational structure.


## Local Installation

Clone the repo

```bash
  git clone https://github.com/moharastegaran/
Combining-ML-and-SNA-to-reveal-organizational-structure.git
```

Go to the project directory
```bash
  cd Combining-ML-and-SNA-to-reveal-organizational-structure
```

Once you cloned the repo, you'll have to need to install missing libraries using pip
```bash
  pip install -e
```
And you're good to go. Run GWO_TSP.py to plot graph as result of solving problem.

## Test & Run
- First, navigate to src folder and run the preprocess.py file.

    It will do the preprocess on dataset which consists of emails & communications.

- Second, in the src folder, run the create_features.py file to create & calculate associated features on data.

- Third, run the network.py file to create graph based on processed data and created features.

- Finally, run the collective_classification.py to run the algorithm used to combine macine learning and social network features and plot graphed result.

## License
This work is an implementation of [this article](https://www.mdpi.com/2076-3417/10/5/1699). 
Primary implementation of this article is [this](https://github.com/gotsdanker/organizational-structure-detection). For the matter of simplicity, only important parts of the main project used and altered here.
Code and methods are documeted for better readability. 
