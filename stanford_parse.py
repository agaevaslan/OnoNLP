import stanfordnlp
from anytree import Node, RenderTree, NodeMixin


stanfordnlp.download('ru', 'stanfordnlp_resources')
nlp = stanfordnlp.Pipeline(lang='ru', models_dir='stanfordnlp_resources')

features = ['index', 'text', 'lemma', 'upos', 'xpos',
            'feats', 'governor', 'dependency_relation']


def stanford_print_parse(sentence):
    # Parses the sentence and outputs CONLL parse
    doc = nlp(sentence)
    return "\n".join(
        ["\t".join(["{}".format(getattr(w, k))
                    for k in features if getattr(w, k) is not None])
         for w in doc.sentences[0].words])


class Token(object):
    pass


class TokenNode(Token, NodeMixin):
    def __init__(self, name, text, lemma, upos, xpos, feats,
                 dependency_relation, governor, parent_node=None, children=[]):
        self.name = name
        self.text = text
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.feats = feats
        self.dependency_relation = dependency_relation
        self.governor = governor
        self.parent_node = parent_node
        if children:
            self.children = children


def sentence_as_tree(sentence):
    """Parses a sentence and outputs anytree tree"""
    doc = nlp(sentence)
    tokens = [TokenNode(w.index, w.text, w.lemma, w.upos, w.xpos, w.feats,
                        w.dependency_relation, int(w.governor))
              for w in doc.sentences[0].words]
    for t in tokens:
        if t.governor != 0:
            t.parent_node = tokens[t.governor-1]
            tokens[int(t.governor-1)
                   ].children = tokens[int(t.governor-1)].children + (t,)
    root = [t for t in tokens if not t.parent_node][0]
    return root, tokens

def tsort(items):
    return sorted(items, key=lambda x: x.name)

def print_ascii_tree(root):
    # root, _ = sentence_as_tree(sentence)
    for pre, _, node in RenderTree(root, childiter=tsort):
        treestr = f"{pre}{node.name}"
        print(treestr.ljust(8), node.lemma, node.upos,
              node.feats, node.dependency_relation)


def extract_keyphrases(sentence):
    candidates = []
    root, _ = sentence_as_tree(sentence)
    for pre, _, node in RenderTree(root, childiter=tsort):
        if node.upos == 'NOUN':
            candidate = []
            candidate.append(node.lemma)
            # print(node.lemma)
            for anc in sorted(node.descendants, key = lambda x: x.name):
                if anc.name > node.name:
                    candidate.append(anc.text)
                    # print(anc.name, anc.text, anc.dependency_relation)
            # print()
            candidates.append(candidate)
    kp = [" ".join(c).lower() for c in candidates if len(c) > 1]
    return kp


def extract_normalized_keyphrases(sentence):
    kp = extract_keyphrases(sentence)
    return kp
    

# Local Variables:
# python-shell-interpreter: "nix-shell"
# python-shell-interpreter-args: "--run python"
# End:
