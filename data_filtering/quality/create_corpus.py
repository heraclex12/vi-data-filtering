import os
import re
from datasets import load_dataset
import markdown
from bs4 import BeautifulSoup
import multiprocessing
from ..filtering import Filtering, LoadParameters
from ..parameters_filtering import parameters_filtering

model_path = '../models'
sentencepiece_model = LoadParameters.load_sentencepiece_model(os.path.join(model_path, 'vi.sp.model'))
kenlm_model = LoadParameters.load_kenlm_model(os.path.join(model_path, 'vi.arpa.bin'))


def clean_text(document):
    text = document['text']
    html = markdown.markdown(text)
    text = BeautifulSoup(html, features='html.parser').get_text()
    cleaned_text = re.sub(r'\n\s*\*', ' ', text)
    cleaned_text = ' '.join(cleaned_text.split())
    cleaned_text = re.sub(r'(\| — \|)|\|', ' ', cleaned_text)
    cleaned_text = re.sub(r'[_*#-=]{2,}', ' ', cleaned_text)
    cleaned_text = re.sub(r'([-—]\s){2,}', ' ', cleaned_text)
    cleaned_text = ' '.join(cleaned_text.split())
    document['text'] = cleaned_text
    return document


def filter_ppl(document):
    return Filtering.check_perplexity(document['text'],
                                      sentencepiece_model=sentencepiece_model,
                                      kenlm_model=kenlm_model,
                                      perplexity_max_cutoff=parameters_filtering["perplexity_max_cutoff"])


if __name__ == '__main__':
    data_dir = "./data"
    with open(os.path.join(data_dir, "data_train.txt"), "w") as out_f:
        # Load data from the Wikipedia corpus
        # And output them as label "__label__wiki"
        dataset = load_dataset("json", data_files={"wiki": os.path.join(data_dir, "data_training_wikiref.json")})
        dataset['wiki'] = dataset['wiki'].map(clean_text, num_proc=multiprocessing.cpu_count())
        dataset['wiki'] = dataset['wiki'].filter(filter_ppl, num_proc=multiprocessing.cpu_count())
        unique = set()
        for row in dataset['wiki']:
            if row["url"] in unique:
                continue
            unique.add(row['url'])
            if int(row["content_length"]) < 1000:
                continue

            out_f.write("__label__wiki " + " ".join(clean_text(row["text"]).splitlines()))
            out_f.write("\n")

        dataset = load_dataset("json", data_files={"cc": os.path.join(data_dir, "data_training_cc.json")})
        dataset['cc'] = dataset['cc'].map(clean_text, num_proc=multiprocessing.cpu_count())
        # Output CommonCrawl data as label "__label__cc"
        for row in dataset['cc']:
            out_f.write("__label__cc " + " ".join(clean_text(row["text"]).splitlines()))
            out_f.write("\n")
