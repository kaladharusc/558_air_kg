import PyPDF2
from PyPDF2 import PdfFileReader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        # get the first page
        page = pdf.getPage(0)
        #print(page)
        print("Number of pages:", pdf.getNumPages())
        #print('Page type: {}'.format(str(type(page))))
        text = page.extractText()
        #print(text)
        tokens = word_tokenize(text)
        punctuations = ['(',')',';',':','[',']',',']
        stop_words = stopwords.words('english')
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
        #print(keywords)
        text = text.split('\n')
        for ind,line in enumerate(text):
            if('IndexTerms' in line):
                print(text[ind+1])
                break
if __name__ == '__main__':
    path = '07889018.pdf'
    text_extractor(path)
