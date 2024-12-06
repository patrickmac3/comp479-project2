from collections import defaultdict
import nltk 
import json
import string 
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import os 

class Index:
    
    def __init__(self, load=False, index_path="index/index.json", mapper_path="index/mapper.json" ):
        # index 
        self.index = defaultdict(lambda: defaultdict(list)) # {word: {doc_id: frequency}}
        # document id mapper 
        self.mapper = defaultdict(str) # {doc_id: url}
        # counter to generate the unique document id 
        self.counter = 0
        # file path to save index and mapper 
        self.index_path = index_path
        self.mapper_path = mapper_path   

        # Check if index_path and mapper_path exist, if they don't create them
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.mapper_path), exist_ok=True)
        
        # Quick way of getting id for url since it is beeing passed page by page 
        self.previous_id = None
        self.previous_url = None
    
        # Load index and mapper if they exist
        if load: 
            self._load()
        # Download necessary NLTK resources
        nltk.download('punkt')
        nltk.download('stopwords')
    
        # for tokenization 
        self.stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
        self.stemmer = PorterStemmer()
        

    def tokenize(self, text):
        """ Tokenize text with improvements """

        # Lowercase and remove accents
        text = text.lower()
        text = unidecode(text)

        # Remove special characters
        text = re.sub(r'[\n\t]', '', text) # remove new lines and tabs
        text = re.sub(rf"[{re.escape(string.punctuation)}]", '', text)  # Remove punctuation

        # Tokenize and remove stop words
        for token in word_tokenize(text):

            # Remove non-alphabetic characters
            token = ''.join(c for c in token if c.isalpha())

            # Stem and remove stop words
            if token and token not in self.stop_words:
                yield self.stemmer.stem(token)

    
    
    def add(self, url, content):
        """ Add to index """
        
        # get or generate document id 
        id = self._get_id(url)
        for token in self.tokenize(content):
            if token not in self.index.keys():
                self.index[token][id] = 1
            elif id not in self.index[token].keys(): 
                self.index[token][id] = 1
            else:
                self.index[token][id] += 1

            
    def save(self):
        """ save the index and mapper to their respective files """
        with open(self.index_path, 'w') as index_file:
            json.dump(self.index, index_file)

        with open(self.mapper_path, 'w') as mapper_file:
            json.dump(self.mapper, mapper_file)
    
    
    """ Private Methods  """
    
    def _get_id(self, url):
        """ Get a document id for a given url  """
        # if current url is the same as previous url, return previous id
        if url == self.previous_url:
            return self.previous_id
        # if url exists in the mapper, return the document id
        if self._url_exists(url):
            return self._get_document_id(url)
        # generate new document id
        self.counter += 1
        self.previous_id = self.counter
        self.previous_url = url
        self.mapper[self.counter] = url
        return self.counter
    
    def _url_exists(self, url):
        """ Check if url exists in the mapper """   
        return url in self.mapper.values()
    
    def _get_document_id(self, url):
        """ Get the document id for the given url """
        return [k for k, v in self.mapper.items() if v == url][0]
    
    def _load(self):
        """ Load the index and mapper from file """
        with open(self.index_path, 'r') as index_file:
            self.index = json.load(index_file)

        with open(self.mapper_path, 'r') as mapper_file:
            self.mapper = json.load(mapper_file)
