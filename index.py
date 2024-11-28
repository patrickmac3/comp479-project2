from collections import defaultdict
import nltk 
import json

# nltk.download('punkt_tab')

class Index:
    
    def __init__(self):
        
        # index 
        self.index = defaultdict(lambda: defaultdict(list)) # {word: {doc_id: frequency}}
        # document id mapper 
        self.mapper = defaultdict(str) # {doc_id: url}
        # counter to generate the unique document id 
        self.counter = 0
        # file path to save index and mapper 
        self.index_path = "index/index.json"
        self.mapper_path = "index/mapper.json"   
        # Quick way of getting id for url since it is beeing passed page by page 
        self.previous_id = None
        self.previous_url = None
    
        # TODO: add limit ? 
        # TODO: add method for loading index and mapper from file 
         
    def tokenize(self, text):
        """ Tokenize text """
        return nltk.word_tokenize(text)
    
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