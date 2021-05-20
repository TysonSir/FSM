"""
词法分析测试用例
"""

import unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../app'))
from model import trans_conflict_check as TCC

class TestLexicalAnalysis(unittest.TestCase):
    def setUp(self):
        self.tcc = TCC.TransConflictCheck()

    def tearDown(self):
        pass

    def test_Not(self):
        src = '!Activate'
        expect_dst = 'Not(Activate)'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_And(self):
        src = 'S_ChannelA & S_ChannelB'
        expect_dst = 'And(S_ChannelA,S_ChannelB)'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_And_Multi(self):
        return # 暂不支持二元以上逻辑
        src = 'S_ChannelA & S_ChannelB & S_ChannelC'
        expect_dst = 'And(S_ChannelA,S_ChannelB,S_ChannelC)'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_Or(self):
        src = 'S_ChannelA XOR S_ChannelB'
        expect_dst = 'Or(S_ChannelA,S_ChannelB)'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_Not_And(self):
        src = '!S_ChannelA & !S_ChannelB'
        expect_dst = 'And(Not(S_ChannelA),Not(S_ChannelB))'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_Not_Or(self):
        src = '!S_ChannelA XOR !S_ChannelB'
        expect_dst = 'Or(Not(S_ChannelA),Not(S_ChannelB))'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_Other1(self):
        src = 'S_ChannelB'
        expect_dst = 'S_ChannelB'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)

    def test_Other2(self):
        src = 'Timer >= DiscrepancyTime'
        expect_dst = 'Timer >= DiscrepancyTime'

        dst = self.tcc.change_format(src)
        self.assertEqual(dst, expect_dst)


if __name__ == '__main__':
    unittest.main()
