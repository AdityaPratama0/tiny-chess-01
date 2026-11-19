import engine

def test_packed_tables():
    assert len(engine.T)==6*64
    assert all(-128<=x<128 for x in engine.T)

def test_black_square_is_mirrored():
    assert (7-(16>>4))*8==(7-((96^0x70)>>4))*8
