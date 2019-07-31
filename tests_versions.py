import os
from glob import glob

import yaml

from django.test import TestCase
#from django.core.exceptions import ValidationError

import pytest

# from downloader.models import DownloadRequest
from tests.factory import EntityFactory

from downloader.models import DownloadRequest
from downloader.models import DownloadRequestManager
from catalogue.management.commands.create_fake_catalogue_items import command

ef = EntityFactory()


class DownloadRequestManagerTestCase(TestCase):

	def setUp(self):
		ef.clear()

		self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'A',
                    'type': 'FLOAT',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': 21,
                    'distribution': [
                        {'value': 10.0, 'count': 20},
                        {'value': 20.1, 'count': 60},
                        {'value': 30.2, 'count': 20},
                    ]
                },
                {
                    'name': 'B',
                    'type': 'FLOAT',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': 24,
                    'distribution': [
                        {'value': 20.0, 'count': 30},
                        {'value': 30.1, 'count': 60},
                        {'value': 40.2, 'count': 10},
                    ]
                },
            ])

		test_spec = {
                'columns': ['A', 'B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }
		
		self.ac = ef.account()

		self.dr = DownloadRequest.objects.create(
			created_by=self.ac,
			spec=test_spec,
            catalogue_item=self.ci)

		self.catalogue_item_id = self.ac
		# to nie jest najlepsze id!!!!!!!!!!!!!!!!!!!!!!!!!

		pk = self.dr.pk
		

	def test_estimate_size__no_download_request(self):
		# dr_from_db = DownloadRequest.objects.get(created_by=self.ac)
		# dr_id = dr_from_db.created_by

		dr_spec = {
                'columns': ['B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }

		drm = DownloadRequestManager()
		#assert drm.estimate_size(dr_spec, self.ac) == 'No Download Request'
		assert drm.estimate_size(dr_spec, ef.account()) == 'No Download Request'

		
	def test_estimate_size__one_column(self):

		dr_spec = {
                'columns': ['B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }
		
		drm = DownloadRequestManager()
		assert drm.estimate_size(dr_spec, self.catalogue_item_id) == 24


	def test_estimate_size__two_column(self):

		dr_spec = {
                'columns': ['A','B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }
		
		drm = DownloadRequestManager()
		assert drm.estimate_size(dr_spec, self.catalogue_item_id) == 45
		#command()
	
	def test_estimate_size__one_column_with_filter(self):

		dr_spec = {
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '<',
                        'value': 20,
                    },
                ],
            }
		
		drm = DownloadRequestManager()
		assert drm.estimate_size(dr_spec, self.catalogue_item_id) == 45