import warnings
from summeriser.summariser import summariser_point_form

warnings.filterwarnings("ignore")

documents = {
    'Tesla': 'docs/k_8/tsla-20240102-gen.pdf',
    'Nvidia': 'docs/k_8/6498cd48-aa46-4547-bcd9-061f74e17c4e.pdf',
    'Alphabet': 'docs/k_8/7f7120e075a47cf9e0aa0d9c3607227a.pdf'
}


def summarise_8_k(document_path):
    doc_summary = summariser_point_form(document_path)
    return doc_summary


for company, document in documents.items():
    k_8_summary = summarise_8_k(document)
    path = "docs/8_k_summaries"
    """ save the company's 8-K summary to a file named {company_name}_8_k_summary.txt """
    with open(f"{path}/{company}_8_k_summary.txt", "w") as file:
        file.write(k_8_summary)
