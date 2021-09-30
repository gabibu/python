

# shellapp:

## main file has two optional arguments:

1. probs_file_path - path to file that contains technologies probabilities (see data/technology_prob.parquet for example)
default - (data/technology_prob.parquet)
2. number_of_top_stories - number of top stories to show (default = 40)


Before running please install requirements.txt.


Follow the console to understand how to use the app.

you will have 3 options on the main page:
1. top stories - will show the top **<number_of_top_stories>**
2. technologies - will let you select technology from list how technologies and
it will preset the monthly probability for the selected technology.



#jupyter notebook:

monthly_probs.ipynb - contains the code that I used to calculate monthly probabilities for the technologies that were given.

### To run locally:

1. unzip hackernews.zip
2. cd hackernews
3. python3.9 -m shellapp.main




