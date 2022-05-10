from tkinter.tix import Form
from django.contrib import admin

from core.models import Faculty, Direction, Format, Document

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'faculty'
    ]


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'direction'
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'format'
    ]

