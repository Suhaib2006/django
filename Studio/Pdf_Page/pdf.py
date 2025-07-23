from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML


def HtmlPdf(template_source,context_dict={}):
    html=render_to_string(template_source,context_dict)
    pdf_file=HTML(string=html).write_pdf()
    response=HttpResponse(pdf_file,content_type="application/pdf")
    response['Content-Dispostion']='inline;filename=""Journal.pdf"'
    return response