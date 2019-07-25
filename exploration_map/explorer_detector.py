
def exploration_detector(self, current_download_request):
        klobczaks_entery = find_chunk_entery(current_download_request)


def find_klobczak_entery(self, current_download_request):
    pass


from django.test import TestCase
import pytest
from tests.factory import EntityFactory
from downloader.models import DownloadRequest
from downloader.models import DownloadRequestManager


class ExplorationDetectorTestCase(TestCase):

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

        self.drm = DownloadRequestManager()


    def is_or_not(self):
        current_download_request = self.dr
        exploration_detector(self, current_download_request)