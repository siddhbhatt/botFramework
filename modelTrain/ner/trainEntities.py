from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import pickle
import re
import json
import sys
import os

botname = sys.argv[1]
BOTCONFIG_PATH = 'bots/'+botname+'/config/'+botname+'.json'
#TRAIN_DATA_PATH = 'models/ner/train_data/data.pkl'
#MODEL_PATH = 'models/ner/model'
MODEL_PATH = 'bots/'+botname+'/models/ner'

botdata = json.load(open(BOTCONFIG_PATH))
aoi = botdata['ner']
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def prepareTrainData():
    train_set = []
    if aoi:
        for a in aoi:
            for b in a['patterns']:
                l=[]
                for c in a['entities']:
                    pos = re.search(c['keyword'], b)
                    if pos:
                        pos_tup = (pos.span()[0], pos.span()[1], c['name'])
                        l.append(pos_tup)
                if l:
                    train_item = (b, {'entities': l})
                    train_set.append(train_item)

        print ("train_set = \n", train_set)
        #pickle.dump(train_set, open(TRAIN_DATA_PATH, 'wb'))
    return train_set

"""
@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
"""
def main(model=None, output_dir=MODEL_PATH, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    #get training data
    TRAIN_DATA = prepareTrainData()

    if TRAIN_DATA:
        # add labels
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        # only train NER
        with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            # reset and initialize the weights randomly – but only if we're
            # training a new model
            if model is None:
                nlp.begin_training()
            i=0
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses, "iter", i)
                i=i+1

        # test the trained model
        for text, _ in TRAIN_DATA:
            doc = nlp(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            #print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

        # save model to output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            for text, _ in TRAIN_DATA:
                doc = nlp2(text)
                print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
                #print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    #plac.call(main)
    main()