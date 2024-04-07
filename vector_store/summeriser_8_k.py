from dotenv import load_dotenv

from summeriser.summariser import summariser_point_form

load_dotenv()

docs_to_summarise = {
    'tesla': '../docs/k_8/tsla-20240102-gen.pdf',
    'nvidia': '../docs/k_8/6498cd48-aa46-4547-bcd9-061f74e17c4e.pdf',
    'alphabet': '../docs/k_8/7f7120e075a47cf9e0aa0d9c3607227a.pdf',
}

doc_summery_paths = {
    'tesla': '../docs/k_8_sum/tesla_8_k_summary.txt',
    'nvidia': '../docs/k_8_sum/nvidia_8_k_summary.txt',
    'alphabet': '../docs/k_8_sum/alphabet_8_k_summary.txt'
}

"""" loop through the docs_to_summarise dictionary and summarize each document """

for company, path in docs_to_summarise.items():

    """ summarize the document """
    summary = summariser_point_form(path)

    """ save the summary to a file """
    with open(doc_summery_paths[company], 'w') as f:
        f.write(summary)
