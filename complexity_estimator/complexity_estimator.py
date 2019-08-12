import math
numb_of_elements = 10000

def estimate(VOLUME, chunks):
    
    s_chunks = sorted(chunks, key = lambda k: k["column"])
    numb_of_d = len(s_chunks[0])
    
    math.floor(numb_of_elements/numb_of_d)

    for col in s_chunks:
        
    shape = {}

def how_many_chunks(min, max, col, chunks):

    col_chunks = []
    for chunk in chunks:
        if chunk["column"] = col:
            col_chunks.append(chunk)

    number_of_chunks = 0
    for chunk in col_chunks:
        if chunk["minimum"]>min and chunk["maximum"]<max:
            number_of_chunks += 1

    # col_chunks_min = min([min for min in chunk["minimum"]])
    # col_chunks_max = max([max for max in chunk["maximum"]])
