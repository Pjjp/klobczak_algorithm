def estimate_size(self, dr_spec, catalogue_item_id):
        try:
            dr_from_db = DownloadRequest.objects.get(created_by=catalogue_item_id)
        except DownloadRequest.DoesNotExist:
            dr_from_db = None

        if(dr_from_db is not None):
            pass
            size = 0
            for i in dr_spec.get('columns'):
                for j in dr_from_db.catalogue_item.spec.get('columns'):
                    if(i==j.get('name')): 
                        size += j.get('size')
            return size
        else:
            return 'No Download Request'
#################################################################


def estimate_size(self, dr_spec, catalogue_item_id):
        try:
            dr_from_db = DownloadRequest.objects.get(created_by=catalogue_item_id)
        except DownloadRequest.DoesNotExist:
            dr_from_db = None

        if(dr_from_db is not None):
            requested_columns = dr_spec.get('columns')
            requested_filters = dr_spec.get('filters')
            matched_columns = self.find_matched_columns(requested_columns, dr_from_db)
            #match - same as in catalogue_item

            estimated_size = 0
            for i in matched_columns:
                estimated_size += i.get('size')

            return estimated_size
        else:
            return 'No Download Request'


    def find_matched_columns(self, requested_columns, dr_from_db):
        m_columns = []
        for i in requested_columns:
                for j in dr_from_db.catalogue_item.spec:
                    if(i==j.get('name')): 
                        m_columns.append(j)
        return m_columns
        # FIXME: probably not the fastest method !!!!


#########################################################################


def estimate_size(self, dr_spec, catalogue_item_id):
        try:
            dr_from_db = DownloadRequest.objects.get(created_by=catalogue_item_id)
        except DownloadRequest.DoesNotExist:
            dr_from_db = None
            #dr_from_db = DownloadRequest.objects.filter(created_by=catalogue_item_id).first()

        if(dr_from_db is not None):
            requested_columns = dr_spec.get('columns')
            requested_filters = dr_spec.get('filters')
            matched_items_spec = self.find_matched_items_spec(requested_columns, dr_from_db)
            #match - same as in catalogue_item

            estimated_size = 0
            for i in matched_items_spec:
                estimated_size += i.get('size')

            return estimated_size
        else:
            return 'No Download Request'


    def find_matched_items_spec(self, requested_columns, dr_from_db):
        m_items = []
        for column in requested_columns:
                for item_spec in dr_from_db.catalogue_item.spec:
                    if(column==item_spec.get('name')): 
                        m_items.append(item_spec)
        return m_items
        # FIXME: probably not the fastest method !!!!


    def find_count_ratio(self, matched_items, requested_filters):
        filtered_items_ratios = {}
        for filt in requested_filters:
            for m_item in matched_items:
                if(filt.get('name')==m_item.get('name')):
                    #filtered_items_list.add(m_item)
                    pass