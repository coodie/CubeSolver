#!/usr/bin/python3

import unittest

import os.path
import cube


proper_perm = set(range(0, 54))


class TestBasePermutations(unittest.TestCase):

    def test_Uperm(self):
        self.assertEqual(set(cube.Uperm), proper_perm)

    def test_Lperm(self):
        self.assertEqual(set(cube.Lperm), proper_perm)

    def test_Fperm(self):
        self.assertEqual(set(cube.Fperm), proper_perm)

    def test_Rperm(self):
        self.assertEqual(set(cube.Rperm), proper_perm)

    def test_Bperm(self):
        self.assertEqual(set(cube.Bperm), proper_perm)

    def test_Dperm(self):
        self.assertEqual(set(cube.Dperm), proper_perm)


class TestSolving(unittest.TestCase):

    def test1(self):
        cube_str = "RURUUURFRFBFRRRURUURUFFDFFBDDLDDBDDLBFBLLLLLLDLDUBBFBB"
        solution = "U2 F2 B2 L' D2 L2 D' R2 L' U F2 L2 B2 R2 F2 D L2 U R2"
        self.solve_attempt(cube_str, solution)

    def test2(self):
        cube_str = "UUUUUUUUURRBRRRRRRFLFFFFFFFDDDDDDDDDBFLLLLLLLLBRBBBBBB"
        solution = "L U2 L' U2 L F' L' U' L U L F L2 U"
        self.solve_attempt(cube_str, solution)

    def test3(self):
        cube_str = "DDBBULBDFLDDRRRURDRRUFFBDUBFFLLDFFDBLUULLLRURLBFUBBRFU"
        solution = "D B' L2 F' D' B2 R' F B U2 L F2 L2 D F2 B2 D' F2 U F2 U2"
        self.solve_attempt(cube_str, solution)

    def solve_attempt(self, cube_str, solution):
        c = cube.Cube(cube_str)
        c.execute(solution)
        self.assertEqual(c.get_string(), cube.get_solved_string())


class FindImages(unittest.TestCase):
    images_names = "U Up U2 U2p R Rp R2 R2p F Fp F2 F2p D Dp D2 D2p L Lp L2 L2p B Bp B2 B2p"

    def test_find_images(self):
        for name in FindImages.images_names.split(" "):
            self.try_to_find_image("./images/"+name+".gif")

    def try_to_find_image(self, fname):
        self.assertTrue(os.path.isfile(fname))


if __name__ == "__main__":
    unittest.main()
