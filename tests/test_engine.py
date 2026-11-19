import engine

START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

def perft(depth):
    if not depth:return 1
    n=0
    for move in engine.gen():
        if engine.make(move):
            n+=perft(depth-1);engine.unmake()
    return n

def test_start_perft():
    engine.load(START)
    assert [perft(d) for d in (1,2,3)]==[20,400,8902]
