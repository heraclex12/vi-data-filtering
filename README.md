## Data Filtering and Data Deduplication

This is the data filtering code used to clean the ROOTS dataset.

### Straightforward Usage
1. Download KenLM and Sentencpiece models:
```commandline
bash scripts/download_sentencepiece_kenlm_models.sh
```
2. Run the command below to proceed filtering data:
```commandline
python main_filtering.py --dataset_name CC_raw --num_proc 256
```
Refer to `main_filtering.py` to change other arguments you want.

### Filtering

#### 0. Understand the filtering pipeline

Take a look at the pdf [explanation filtering pipeline](https://drive.google.com/file/d/1cCJ8sWE88TRLDAa3eHLmXO4JlkR2QzLY/view?usp=sharing) for an explanation of the filtering pipeline.

#### 1. Define the lists of stopwords and flagged words, and check how the anonymization and the normalization of texts are done

You might want to redefine the lists of stop words (closed class words) and flagged words for robustness or ethical reasons in the files [stopwords.py](./stopwords.py) and [flagged_words.py](./flagged_words.py).

Less importantly, you can also check how the anonymization and the normalization of texts are done in the files [anonymization.py](./anonymization.py) and [normalization.py](./normalization.py) (if applicable, default is not to use both).

#### 2. Download everything you need

To run the filtering code, it is necessary to download the necessary models, which are the Fasttext model for language identification (download [here](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)) and the Sentencepiece and KenLM models for tokenization and calculation of perplexity scores (download with the file [download_sentencepiece_kenlm_models.sh](./scripts/download_sentencepiece_kenlm_models.sh)).

#### 3. Choose the filtering parameters

The filtering parameters are to be specified in the file [parameters_filtering.py](./parameters_filtering.py). It is strongly recommended to look at the data and use the visualization code in the directory [visualization](./visualization) to choose these parameters.

#### 4. Run the filtering

Run the filtering with the file [main_filtering.py](./main_filtering.py), specifying the dataset used and the links to the downloaded models. The different filters are coded in the file [filtering.py](./filtering.py).

Some common issues:
- OSCAR-v2 metadata can cause cryptic Arrow bugs. The `remove_meta` flag will take care of this and/or space issues
- Too-long documents can cause hangs. Use `max_len_prefilter` to remove outliers. 
- Memory issues can arise, causing hard-to-debug hangs if a process dies silently. Reducing the number of processes will help in this case.
- If your dataset is very large, you may have space issues in the saving stage. In this case, you will find an equivalent `.arrow` file in your `datasets` cache (typically the last-modified file in `.cache/huggingface/datasets/<dataset_name>/....`) anyway. The saving stage is mostly for better clarity and to avoid manipulating the `datasets` cache. 

#### 5. Do the deduplication

Do the deduplication, which is detailed in the sub folder [deduplicate](./deduplicate).



## Citation
```
@inproceedings{
bigscience-roots:2022,
title={The BigScience {ROOTS} Corpus: A 1.6{TB} Composite Multilingual Dataset},
author={Hugo Lauren{\c{c}}on and Lucile Saulnier and Thomas Wang and Christopher Akiki and Albert Villanova del Moral and Teven Le Scao and Leandro Von Werra and Chenghao Mou and Eduardo Gonz{\'a}lez Ponferrada and Huu Nguyen and J{\"o}rg Frohberg and Mario {\v{S}}a{\v{s}}ko and Quentin Lhoest and Angelina McMillan-Major and G{\'e}rard Dupont and Stella Biderman and Anna Rogers and Loubna Ben allal and Francesco De Toni and Giada Pistilli and Olivier Nguyen and Somaieh Nikpoor and Maraim Masoud and Pierre Colombo and Javier de la Rosa and Paulo Villegas and Tristan Thrush and Shayne Longpre and Sebastian Nagel and Leon Weber and Manuel Romero Mu{\~n}oz and Jian Zhu and Daniel Van Strien and Zaid Alyafeai and Khalid Almubarak and Vu Minh Chien and Itziar Gonzalez-Dios and Aitor Soroa and Kyle Lo and Manan Dey and Pedro Ortiz Suarez and Aaron Gokaslan and Shamik Bose and David Ifeoluwa Adelani and Long Phan and Hieu Tran and Ian Yu and Suhas Pai and Jenny Chim and Violette Lepercq and Suzana Ilic and Margaret Mitchell and Sasha Luccioni and Yacine Jernite},
booktitle={Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
year={2022},
url={https://openreview.net/forum?id=UoEw6KigkUn}
}
```
