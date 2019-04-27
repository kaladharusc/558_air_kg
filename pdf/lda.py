import sys
import warnings
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from io import StringIO
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation

class MyParser(object):
    def __init__(self, pdf):
        parser = PDFParser(open(pdf, 'rb'))
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        codec = 'utf-8'
        device = TextConverter(rsrcmgr, retstr,
                               codec = codec,
                               laparams = laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        self.records = []
        lines = retstr.getvalue().splitlines()
        for line in lines:
            self.handle_line(line)

    def handle_line(self, line):
        self.records.append(line)

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    p = MyParser(sys.argv[1])
    #print('\n'.join(p.records))
    list = p.records[] # [:30]
    #print(list)
    f1 = 0
    abstract = ""
    for item in list:
        if('Abstract' in item):
            f1 = 1
            abstract+=item
        if(f1 == 1):
            if(item.strip()):
                abstract+=item
            else:
                break
    print(abstract)
    print("\n LDA:")
    # LDA
    no_features = 10
    tf_vectorizer = CountVectorizer(max_df=2, min_df=0.95, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform([abstract])
    tf_feature_names = tf_vectorizer.get_feature_names()
    no_topics = 5
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    no_top_words = 2
    display_topics(lda, tf_feature_names, no_top_words)
