# online_chess
An online chess game is created using pygame. Server with localhost is created in socket. Thread is used to handle multiple users.


**Required package:**
socket, _thread, pickle, time, pygame, os


**How to play:**
Server.py should be run first but only by the first player. Then to run the game.py to join the game.


**Note:**
1. Pawn can only be promoted to Queen in this game.
2. Castling: click rook first, then click king.
3. En passant capture is not availabe in this game but will update in the future.
4. To resign, press Q
