

Build Docker Image:

```
cd  data_collector
docker build -t collector  ./

```

Run Image:

```


docker run -v $mounted_dir$:/data collector --url $URL$ --depth $depth$ --fetch_concurrency $fetch_concurrency$  --parse_concurrency $parse_concurrency$

Replace: 

$mounted_dir$ - path on local machine that I will save the data (sqllite) so you can query the results
$URL$ with valid url example: https://huggingface.co/valhalla/distilbart-mnli-12-1
$depth$ with valid depth exmple: 2
$fetch_concurrency with concurrency number (number of threads ti download pages) - Optional
$parse_concurrency$ - number of threads to parse html - Optional 

```

Examples:

1. docker run -v /var/d1:/data collector --url https://huggingface.co/facebook/bart-large-mnli --depth 1 --fetch_concurrency 2  --parse_concurrency 2
2. docker run -v /var/d1:/data collector --url https://www.tutorialspoint.com/index.htm --depth 1


