#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import pdb

from django.db import models

from bs4 import BeautifulSoup, Tag

DOC_TYPE = [
    (0, 'Учебный план'),
    (1, 'Рабочая программа'),
]


class Faculty(models.Model):
    """
    Факультет
    """

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "факультет"
        verbose_name_plural = "Факультеты"


class Direction(models.Model): 
    """
    Направление
    """

    faculty = models.ForeignKey(
        Faculty,
        verbose_name=u'Факультет',
        on_delete=models.CASCADE,
    )
    
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "направление"
        verbose_name_plural = "Направления"


class Format(models.Model):
    """
    Формат обучения
    """

    direction = models.ForeignKey(
        Direction,
        verbose_name=u'Направление',
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    url = models.URLField(
        verbose_name='ссылка на файл',
        max_length = 20000,
        null=True
    )

    def __str__(self):
        return f'{self.direction.title}, {self.title}'

    class Meta:
        verbose_name = "формат"
        verbose_name_plural = "Форматы обучения"


class DocumentType(models.Model):
    """
    Тип документа
    """
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    def __str__(self):
        return f'{self.title}'


class Document(models.Model):
    """
    Документ
    """

    format = models.ForeignKey(
        Format,
        verbose_name=u'Формат обучения',
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    url = models.URLField(
        verbose_name='ссылка на файл',
        max_length = 20000
    )

    type = models.ForeignKey(
        DocumentType,
        verbose_name="Тип программы",
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "Документы"




# Класс, который парсит таблицу
class Extractor(object):
    def __init__(self, input, id_=None, **kwargs):

        # validate the input
        if not isinstance(input, str) and not isinstance(input, Tag):
            raise Exception('Unrecognized type. Valid input: str, bs4.element.Tag')

        soup = BeautifulSoup(input, 'html.parser').find() if isinstance(input, str) else input

        # locate the target table
        if soup.name == 'table':
            self._table = soup
        else:
            self._table = soup.find(id=id_)

        # if 'transformer' in kwargs:
        #     self._transformer = kwargs['transformer']
        # else:
        #     self._transformer = str

        self._output = []

    def parse(self):
        self._output = []
        row_ind = 0
        col_ind = 0
        for row in self._table.find_all('tr'):
            # record the smallest row_span, so that we know how many rows
            # we should skip
            smallest_row_span = 1

            for cell in row.children:
                if cell.name in ('td', 'th'):
                    # check multiple rows
                    # pdb.set_trace()
                    row_span = int(cell.get('rowspan')) if cell.get('rowspan') else 1

                    # try updating smallest_row_span
                    smallest_row_span = min(smallest_row_span, row_span)

                    # check multiple columns
                    col_span = int(cell.get('colspan')) if cell.get('colspan') else 1

                    # find the right index
                    while True:
                        if self._check_cell_validity(row_ind, col_ind):
                            break
                        col_ind += 1

                    # insert into self._output
                    try:
                        self._insert(row_ind, col_ind, row_span, col_span, cell)
                    except UnicodeEncodeError:
                        raise Exception( 'Failed to decode text; you might want to specify kwargs transformer=unicode' )

                    # update col_ind
                    col_ind += col_span

            # update row_ind
            row_ind += smallest_row_span
            col_ind = 0
        return self

    def return_list(self):
        return self._output

    def write_to_csv(self, path='.', filename='output.csv'):
        with open(os.path.join(path, filename), 'w') as csv_file:
            table_writer = csv.writer(csv_file)
            for row in self._output:
                table_writer.writerow(row)
        return

    def _check_validity(self, i, j, height, width):
        """
        check if a rectangle (i, j, height, width) can be put into self.output
        """
        return all(self._check_cell_validity(ii, jj) for ii in range(i, i+height) for jj in range(j, j+width))

    def _check_cell_validity(self, i, j):
        """
        check if a cell (i, j) can be put into self._output
        """
        if i >= len(self._output):
            return True
        if j >= len(self._output[i]):
            return True
        if self._output[i][j] is None:
            return True
        return False

    def _insert(self, i, j, height, width, val):
        # pdb.set_trace()
        for ii in range(i, i+height):
            for jj in range(j, j+width):
                self._insert_cell(ii, jj, val)

    def _insert_cell(self, i, j, val):
        while i >= len(self._output):
            self._output.append([])
        while j >= len(self._output[i]):
            self._output[i].append(None)

        if self._output[i][j] is None:
            self._output[i][j] = val
