from django.core.exceptions import ValidationError
from catalogue.models import CatalogueItem

COUNT = 1000

CHUNKS = CatalogueItem.create_chunks(COUNT)
RANGE = 100

# FIXME: what if min, max are strings?

def complexityEstimator(CHUNKS, RANGE):

    if all(CHUNKS[i]['column'] <= CHUNKS[i+1]['column'] for i in range(len(CHUNKS-1))):
        left_min = CHUNKS[0].borders['minimum']
        right_max = CHUNKS[-1].borders['maximum']

        sample_chunks = []
        while(RANGE):
            for ch in CHUNKS:
                sample_chunks.append({
                    # 'minimum': randrange(ch.borders['minimum'], ch.borders['maximum']-1)
                    # 'maximum': randrange(sample_chunk['minimum'], ch.borders['maximum'])
                })

    else:
        raise ValidationError(
            'chunks have to be sorted'
        )

def percent_of_whole(CHUNKS, sample_chunks):
    
    chunks_area = 1
    for ch in CHUNKS:
        chunks_area = chunks_area*(ch.borders['maximum'] - ch.borders['minimum'])
    
    sample_chunks_area = 1
    for s_ch in sample_chunks:
        sample_chunks_area = sample_chunks_area*chunks_area*(s_ch.borders['maximum'] - s_ch.borders['minimum'])

    return (sample_chunks_area/chunks_area)*100