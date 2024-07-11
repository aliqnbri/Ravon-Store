from django.db import models
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv



def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    
    # Set the HTTP response headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    
    # Create CSV writer object
    writer = csv.writer(response)
    
    # Get fields excluding many-to-many and one-to-many relations
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    
    # Write header row
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # Convert datetime objects to a formatted string
            if isinstance(value, timezone.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response


export_to_csv.short_description = 'Export to CSV'