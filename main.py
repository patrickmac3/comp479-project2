from index import Index
from pdf_crawler import PdfCrawler
from pipeline import Pipeline


def main():
    
    # initialize the pipeline 
    pipeline = Pipeline()
    
    # start the pipeline with the pdf crawler and a limit of  pdfs
    limit = 400
    pipeline.start(PdfCrawler, limit)
    
    # save the index after the pipeline is done
    pipeline.index.save()


if __name__ == '__main__':
    main()