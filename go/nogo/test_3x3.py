import unittest
from solve_3x3 import legal_moves,groups_have_liberties,solve,optimal_line
class TestNoGo(unittest.TestCase):
 def test_empty_board(self):self.assertEqual(len(list(legal_moves(0,0,0))),9)
 def test_no_suicide(self):
  # Black surrounds center with four black stones; placing white at center is suicide.
  b=sum(1<<i for i in (1,3,5,7))
  self.assertNotIn(4,list(legal_moves(b,0,1)))
 def test_no_capture(self):
  # White center has exactly one liberty at bottom-center; black cannot fill it.
  w=1<<4;b=sum(1<<i for i in (1,3,5))
  self.assertNotIn(7,list(legal_moves(b,w,0)))
 def test_no_occupied(self):self.assertNotIn(0,list(legal_moves(1,0,1)))
 def test_terminal(self):
  # A full board admits no placements, irrespective of whose turn it is.
  self.assertEqual(list(legal_moves(0b111111111,0,1)),[])
 def test_optimal_line(self):
  win,d=solve(0,0,0);line,loser=optimal_line()
  self.assertEqual(len(line),d)
  self.assertEqual(loser==1,win)
  b=w=0;turn=0
  for t,i,nb,nw in line:
   self.assertEqual(t,turn)
   self.assertIn(i,list(legal_moves(b,w,turn)))
   b,w,turn=nb,nw,1-turn
  self.assertFalse(list(legal_moves(b,w,turn)))
if __name__=='__main__':unittest.main()
