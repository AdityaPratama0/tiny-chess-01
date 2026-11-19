# Development notes

The engine uses a 0x88 board and six single-phase signed-byte piece-square tables. Black squares are mirrored with `sq ^ 0x70`. Search retains PVS, the Zobrist-keyed transposition table, four-ply capture/promotion quiescence, mate-distance adjustment, the 120000-node cap, and the eight-second guard.

The practice book required the requested size-contingency cuts through killer moves: history, null-move pruning, and killer moves were removed. Quiescence remains at depth four.
