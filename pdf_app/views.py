from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
import io
import boto3
from datetime import datetime
import os


def upload_pdf_to_s3(pdf_data, s3_key):
    # Initialize S3 client
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                      region_name=os.getenv('AWS_S3_REGION_NAME'))

    # Upload PDF data to S3
    s3.upload_fileobj(io.BytesIO(pdf_data),
                      os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_key)


@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        html_content = request.body.decode('utf-8')
        pdf_file = HTML(string=html_content).write_pdf()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_file_{timestamp}.pdf"

        upload_pdf_to_s3(pdf_file, f'./filename')

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="generated.pdf"'
        return response

    return HttpResponse("Only POST requests are allowed.", status=405)
