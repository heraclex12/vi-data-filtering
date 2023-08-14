## Quality Classifier

Quote from the LLaMA paper:
> we trained a linear model to classify pages used as references in Wikipedia v.s. randomly sampled pages, and discarded pages not classified as references.

#### Crawling Wikipedia References
We downloaded the most recent Vietnamese Wikipedia dump available by May 1, 2023 from https://dumps.wikimedia.org/viwiki/latest. Unizpping the large bz2 folder with the following script should leave you with an XML file.

``` 
bzip2 -dk viwiki-latest-pages-articles-multistream.xml.bz2 
``` 

Extract all the reference URLs from the XML and put them in a newline-delimited text file with ``` extract_urls.py```. You can specify input and output file. The default output file is `extracted_urls.txt`.

In `extracted_urls.txt`, we provide 38M URLs that are processed from the Wikipedia dump. We early stop this process to only keep 300K pages.

```
wget –-timeout=5 -i urls_random.txt --warc-file=warc_wikipedia.warc -O /dev/null
```

We then run the same `cc-net` pipeline on `warc_wikipedia.warc`, which produces `warc_wikipedia.warc.wet`.

The next step is to random sample the same number of CommonCrawl pages as Wikipedia References:

```
python create_corpus.py
```

#### Train a Classifier for Filtering
We then train a classifier using fastText:

```
fasttext supervised -input data_train -output model
```

We then classify each CommonCrawl webpage using the trained classifier. The model weights can be downloaded [here](https://drive.google.com/file/d/1DnsfpWWE0jFPCoYe6clwqb3Ub5Ac92s1/view?usp=share_link). 

```
python classify.py
```

This will create:

```
A.gz.result              // content after deduplication
A.gz.dedup.classifier.gz // result with classifier probability
```

Finally, we filter out all documents that have score less than `0.25`:
```commandline
bash cc_classifier.sh cc_data/
```