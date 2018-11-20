#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gobanpdf` package."""


import unittest
from click.testing import CliRunner
import os

from gobanpdf import gobanpdf


class TestGobanpdf(unittest.TestCase):
    """Tests for `gobanpdf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""

        runner = CliRunner()
        help_result = runner.invoke(gobanpdf.board_to_pdf, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

        sgfs = [
            """(
                ;GM[1]FF[4]CA[UTF-8]KM[7.5]SZ[19]
                ;B[ar]
                ;W[as]
                ;B[bs]
                ;W[br]LB[ar:A][br:B]SQ[as]MA[bs]
                )""",
            """(;EV[ Gu Li vs. Lee Sedol Jubango, game 1]
                DT[2014-01-26]
                PB[Lee Sedol]BR[9p]
                PW[Gu Li]WR[9p]
                KM[7.5]RE[B+R]
                SO[Go4Go.net]
                ;B[pd];W[dp];B[qp];W[dc];B[fq];W[dn];B[lq];W[eq];B[fp];W[ip];B[ci];W[ck];B[ce];W[op];B[lo];W[go];B[qn];W[jq];B[en];W[dm];B[em];W[gm];B[do];W[co];B[eo];W[dl];B[fl];W[fr];B[hq];W[im];B[cp];W[cq];B[bp];W[bo];B[bq];W[cr];B[br];W[bs];B[er];W[es];B[gr];W[fs];B[fj];W[hj];B[kl];W[qq];B[rq];W[ln];B[mn];W[lm];B[mo];W[di];B[jn];W[gp];B[gq];W[gl];B[gk];W[hk];B[fi];W[rr];B[in];W[hn];B[hp];W[jm];B[ho];W[ko];B[km];W[kn];B[io];W[kp];B[il];W[lp];B[pq];W[nq];B[qr];W[jl];B[jk];W[hm];B[kk];W[ii];B[ik];W[hl];B[mk];W[nl];B[nk];W[ol];B[ml];W[mm];B[on];W[nn];B[ok];W[pl];B[pk];W[ql];B[hh];W[jh];B[qk];W[rl];B[jf];W[lh];B[lf];W[nh];B[ph];W[mf];B[le];W[ig];B[ki];W[kh];B[mg];W[gh];B[gi];W[hi];B[gg];W[hg];B[fh];W[he];B[ed];W[hc];B[ec];W[ng];B[mh];W[mi];B[lg];W[oi];B[li];W[nd];B[md];W[pi];B[qi];W[qh];B[rj];W[nc];B[mc];W[ri];B[qj];W[ne];B[of];W[pf];B[qg];W[kc];B[id];W[hd];B[jb];W[eb];B[fb];W[gb];B[db];W[jc];B[nb];W[ob];B[mb];W[pc];B[ic];W[ib];B[kb];W[ja];B[ka];W[fc];B[ea];W[fd];B[fe];W[ff];B[ee];W[gf];B[if];W[hf];B[dh];W[ia];B[lc];W[ie];B[jd];W[je];B[kd];W[ga];B[qd];W[qc];B[rd];W[pg];B[rh];W[oe];B[bj];W[bk];B[lr];W[oo];B[mq];W[mp];B[rb];W[rc];B[sc];W[qb];B[dj];W[or];B[ep];W[dq];B[jr];W[pr];B[qs];W[ir];B[kr];W[iq];B[is];W[qf];B[rf];W[pn];B[po];W[pm];B[jg];W[ge];B[bm];W[bl];B[gs];W[dr];B[cj];W[el];B[fm];W[ek];B[fk];W[eg];B[ef];W[fg];B[dg];W[ro];B[rn];W[sn];B[sm];W[so];B[qo];W[rm];B[nr];W[oq];B[sp];W[sl];B[rp];W[sm];B[gh];W[ih];B[sr];W[oh];B[qh];W[bn];B[ns];W[aj];B[ai];W[ak];B[sb];W[oa];B[ej];W[ra];B[dk];W[me];B[ap])
                """]
        move_numbers = ['5', '40']

        with runner.isolated_filesystem():
            for i in range(len(sgfs)):
                with open('example.' + str(i) + '.sgf', 'w') as f:
                    f.write(sgfs[i])
                result = runner.invoke(gobanpdf.board_to_pdf, ['example.' + str(i) + '.sgf', move_numbers[i], 'example.' + str(i) + '.pdf'])
                assert result.exit_code == 0

                # Test that the output file exists
                assert os.path.isfile('example.' + str(i) + '.pdf')

                # ... and test that it's a pdf
                with open('example.' + str(i) + '.pdf', 'rb') as f: line = f.readline()
                assert '%PDF' in line.decode("utf-8")



