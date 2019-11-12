from flask import Flask, escape, request, render_template

import stanfordnlp
stanfordnlp.download('ru', 'stanfordnlp_resources')
nlp = stanfordnlp.Pipeline(lang='ru',models_dir='stanfordnlp_resources')

features = ['index', 'text', 'lemma', 'upos', 'xpos', 'feats', 'governor', 'dependency_relation']
def stanford_parse(sentence):
    # Parses the sentence and outputs CONLL parse
    doc = nlp(sentence)    
    return "\n".join(["\t".join(["{}".format(getattr(w, k)) for k in features if getattr(w, k) is not None])
                      for w in doc.sentences[0].words])

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello():
    sentence = request.args.get("sentence", "Россия объявила в международный розыск журналиста Александра Шварева из-за публикаций о миллиардере Алишере Усманове.")
    parse = stanford_parse(sentence) 
    return render_template('parse.html',sentence=sentence,parse=parse)
