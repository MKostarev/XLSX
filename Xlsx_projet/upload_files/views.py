import openpyxl
from celery import shared_task
from django.contrib import messages
from .forms import UploadFileForm
from .tasks.tasks import process_excel_file
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, ProductGroup
import logging

logger = logging.getLogger(__name__)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = f'media/uploads/{file.name}'
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            process_excel_file.delay(file_path)
            messages.success(request, 'Файл принят в обработку!')
            return render(request, 'upload_files/upload_file.html', {'form': UploadFileForm()})
    else:
        form = UploadFileForm()
    return render(request, 'upload_files/upload_file.html', {'form': form})


@login_required
def check_data(request):
    products = Product.objects.all()
    return render(request, 'upload_files/check_data.html', {'products': products})


@shared_task(bind=True)
def process_excel_file(self, file_path):
    try:
        logger.info(f"Начало обработки файла: {file_path}")
        print(f"[Celery] Начало обработки: {file_path}")  # Дублируем в консоль

        wb = openpyxl.load_workbook(filename=file_path)
        sheet = wb.active

        default_group, _ = ProductGroup.objects.get_or_create(name='Запчасти')
        processed_rows = 0

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                if not row[0] or not row[1]:  # Проверка обязательных полей
                    continue

                # Обработка товарной группы
                group_name = row[5] if row[5] else 'Запчасти'
                product_group, _ = ProductGroup.objects.get_or_create(
                    name=group_name,
                    defaults={'parent': default_group}
                )

                # Создание/обновление товара
                Product.objects.update_or_create(
                    article=row[1],
                    defaults={
                        'brand': row[0],
                        'trading_numbers': row[2] or '',
                        'description': row[3] or '',
                        'additional_name': row[4] or '',
                        'product_group': product_group,
                        'product_status': row[6] or 'Новый',
                        'specifications': row[7] or ''
                    }
                )
                processed_rows += 1

            except Exception as e:
                logger.error(f"Ошибка в строке {row_idx}: {str(e)}")
                continue

        logger.info(f"Успешно обработано строк: {processed_rows}")
        print(f"[Celery] Обработка завершена. Строк: {processed_rows}")
        return processed_rows

    except Exception as e:
        logger.error(f"Критическая ошибка обработки: {str(e)}")
        print(f"[Celery] Ошибка: {str(e)}")
        raise self.retry(exc=e, countdown=60)

