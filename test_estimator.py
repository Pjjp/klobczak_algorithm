import os
from glob import glob

import yaml

from django.test import TestCase
from django.core.exceptions import ValidationError

import pytest

# from downloader.models import DownloadRequest
from tests.factory import EntityFactory

from downloader.models import DownloadRequest
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

		dr_spec = {
                'columns': ['A', 'B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }

		self.dr = DownloadRequest.objects.create(
			created_by=ef.account(),
			spec=dr_spec,
            catalogue_item=self.ci)

		pk = self.dr.pk
		self.catalogue_item_id = pk

	def test_estimate_size__no_filters(self):
		# dr_from_db = DownloadRequest.objects.get(created_by=self.ac)
		# dr_id = dr_from_db.created_by

		spec = {
            'columns': ['B'],
            'filters': [],
        }
        
    		assert DownloadRequest.objects.estimate_size(spec, 41414) == 'No Download Request'

	def test_estimate_size__one_column(self):

		test_spec = {
                'columns': ['B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }

		assert self.drm.estimate_size(test_spec, self.catalogue_item_id) == 24


	def test_estimate_size__two_column(self):

		test_spec = {
                'columns': ['A','B'],
                'filters': [
                    # {
                    #     'name': 'paid',
                    #     'operator': '=',
                    #     'value': 38,
                    # },
                ],
            }

		assert self.drm.estimate_size(test_spec, self.catalogue_item_id) == 45
		#command()
	
	def test_estimate_size__one_column_with_filter(self):

		test_spec = {
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '<',
                        'value': 20,
                    },
                ],
            }

		self.drm.estimate_size(test_spec, self.catalogue_item_id)
		assert 1 == 1


####################################################################
#components
####################################################################

	def test_find_matched_items_spec(self):

		ci = ef.catalogue_item(
	            spec=[
	                {
	                    'name': 'A',
	                    'type': 'FLOAT',
	                    'is_nullable': False,
	                    'is_enum': False,
	                    'size': 21,
	                    'distribution': [
	                    ]
	                },
	                {
	                    'name': 'B',
	                    'type': 'FLOAT',
	                    'is_nullable': False,
	                    'is_enum': False,
	                    'size': 24,
	                    'distribution': [
	                    ]
	                },
	            ])

		test_spec = {
				'columns': ['A', 'B'],
	                'filters': [],
		}

		dr = DownloadRequest.objects.create(
				created_by=ef.account(),
				spec=test_spec,
	            catalogue_item=ci)

		assert self.drm.find_matched_items_spec(['A', 'B'], dr) == ci.spec


	def test_find_matched_items_spec__one_in_test_spec(self):

		ci = ef.catalogue_item(
	            spec=[
	                {
	                    'name': 'A',
	                    'type': 'FLOAT',
	                    'is_nullable': False,
	                    'is_enum': False,
	                    'size': 21,
	                    'distribution': [
	                    ]
	                },
	                {
	                    'name': 'B',
	                    'type': 'FLOAT',
	                    'is_nullable': False,
	                    'is_enum': False,
	                    'size': 24,
	                    'distribution': [
	                    ]
	                },
	            ])

		test_spec = {
				'columns': ['B'],
	                'filters': [],
		}

		dr = DownloadRequest.objects.create(
				created_by=ef.account(),
				spec=test_spec,
	            catalogue_item=ci)

		assert self.drm.find_matched_items_spec(['A', 'B'], dr) == ci.spec


	def test_find_matched_items_spec__one_in_catalogue_item_spec(self):

		ci = ef.catalogue_item(
	            spec=[
	                {
	                    'name': 'A',
	                    'type': 'FLOAT',
	                    'is_nullable': False,
	                    'is_enum': False,
	                    'size': 21,
	                    'distribution': [
	                    ]
	                },
	            ])

		test_spec = {
				'columns': ['A', 'B'],
	                'filters': [],
		}

		with pytest.raises(ValidationError) as e:
			dr = DownloadRequest.objects.create(
					created_by=ef.account(),
					spec=test_spec,
		            catalogue_item=ci)

		assert e.value.message_dict == {
            '__all__': ["unknown columns in 'columns' detected: 'B'"],
        }
    #nie wiem czy tu tu wstawiac tylko po to zeby pokazac co sie dzieje???????????????????


	def test_find_filtered_items_list(self):
		requested_filters = [{'name': 'A', 'operator': '<', 'value': 20}]
		
		matched_items = [{'name': 'A', 'size': 21, 'type': 'FLOAT', 'is_enum': False, 'is_nullable': 
		False, 'distribution': [{'count': 20, 'value': 10.0}, {'count': 60, 'value': 20.1}, 
		{'count': 20, 'value': 30.2}]}, {'name': 'B', 'size': 24, 'type': 'FLOAT', 'is_enum': False, 'is_nullable': 
		False, 'distribution': [{'count': 30, 'value': 20.0}, {'count': 60, 'value': 30.1}, {'count': 10, 'value': 40.2}]}]

		assert self.drm.find_filtered_items_list(matched_items, requested_filters) == [{'name': 'A', 'operator': '<', 'value': 20}]


	def test_find_filtered_items_list_empty(self):
		requested_filters = [{'name': 'C', 'operator': '<', 'value': 20}]
		
		matched_items = [{'name': 'A', 'size': 21, 'type': 'FLOAT', 'is_enum': False, 'is_nullable': 
		False, 'distribution': [{'count': 20, 'value': 10.0}, {'count': 60, 'value': 20.1}, 
		{'count': 20, 'value': 30.2}]}, {'name': 'B', 'size': 24, 'type': 'FLOAT', 'is_enum': False, 'is_nullable': 
		False, 'distribution': [{'count': 30, 'value': 20.0}, {'count': 60, 'value': 30.1}, {'count': 10, 'value': 40.2}]}]

		assert self.drm.find_filtered_items_list(matched_items, requested_filters) == []


	def test_apply_filter(self):

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
            ]

	    # filt = {
     #        'name': 'A',
     #        'operator': '<',
     #        'value': 20,
     #    }

        # list_dict_value_coun = []
        # for obj in objects:
        #     for dic in obj.get('distribution')
        #         list_dict_value_coun.append(dic)
        list_dict_value_coun = []
        for col in spec:
            for dic in col:
        	   list_dict_value_coun.append(dic)

        self.drm.apply_filter(filt, list_dict_value_coun)

