from index import Index
from pdf_crawler import PdfCrawler
from pipeline import Pipeline


def main():
    pipeline = Pipeline()
    pipeline.start(PdfCrawler)
    pipeline.index.save()


if __name__ == '__main__':
    main()