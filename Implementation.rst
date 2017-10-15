Implementation Notes
====================

The main requirement for this program
was to be easily deployable.
Therefore, the following restrictions were put in place:

(1) it will be written in an interpreted language, so Python 3 was chosen;
(2) the whole program should be a single file; and
(3) it should not require any library besides the modules
    coming with a standard Python distribution.


XML pretty-printing
-------------------

While the standard Python `xml`_ module provide a pretty-printing functionality,
it is not customizable enough.

.. _xml: https://docs.python.org/3.6/library/xml.html

Among the desired functionality was:

- ability to specify which tags should be considered *inline* or *block*;
- ability to have text wrap (at word level) at a maximum line length;
- ability to specify the level indentation depth;
- ... and possibly others.

Therefore I wrote the pretty-printing myself,
working on the XML tree node by node.

In case one has never attempted a pretty-printing before,
a couple of the most important references are:

- John Hughes, “The design of a pretty-printing library” in *Advanced
  functional programming: First international spring school on advanced
  functional programming techniques, Båstad, Sweden, May 24–30, 1995*,
  Johan Jeuring and Erik Meijer (eds.),. Springer Berlin
  Heidelberg, Berlin, Heidelberg, pp. 53–96, 1995.
  https://doi.org/10.1007/3-540-59451-5_3
- Philip Wadler, “A prettier printer” in *Journal of functional
  programming*, pp. 223–244, 1998.


Line wrapping
-------------

Again, the standard Python library includes `textwrap.fill`_
but no invocation could guarantee the exact match
of the generated text (e.g. no adding or removing of spaces
in significant places).

.. _textwrap.fill: https://docs.python.org/3/library/textwrap.html

I ended up implementing the Knuth algorithm (used in TeX etc.)
for breaking a text into a series of balanced lines.
Coming up with an efficient implementation was a matter
of reading the appropriate papers in literature.

For the curious, this was my bibliography;
the first is the original Knuth paper,
while the rest deal with optimizations.

1. Donald E. Knuth and Michael F. Plass, “Breaking paragraphs into
   lines”, *Software: Practice and Experience*, vol. 11, no. 11, pp.
   1119–1184, 1981. https://doi.org/10.1002/spe.4380111102

2. A Aggarwal, M Klawe, S Moran, P Shor, and R Wilber, “Geometric
   applications of a matrix searching algorithm” in *Proceedings of the
   second annual symposium on computational geometry* (SCG ’86), pp.
   285–292., 1986. https://doi.org/10.1145/10515.10546

3. Daniel S. Hirschberg and Lawrence Louis Larmore, “New applications of
   failure functions”, *Journal of the ACM*, vol. 34, no. 3, pp. 616–625,
   1987. https://doi.org/10.1145/28869.28875

4. Daniel S. Hirschberg and Lawrence Louis Larmore, “The least weight
   subsequence problem”, *SIAM Journal on Computing*, vol. 16, no. 4, pp.
   628–638, 1987. https://doi.org/10.1137/0216043

5. Robert Wilber, “The concave least-weight subsequence problem
   revisited”, *Journal of Algorithms*, vol. 9, no. 3, pp. 418–425, 1988.
   https://doi.org/10.1016/0196-6774(88)90032-6

6. Zvi Galil and Raffaele Giancarlo, “Speeding up dynamic programming
   with application to molecular biology”, *Theoretical Computer Science*,
   vol. 64, no. 1, pp. 107–118, 1989.
   https://doi.org/10.1016/0304-3975(89)90101-1

7. David Eppstein, “Sequence comparison with mixed convex and concave
   costs”, *Journal of Algorithms*, vol. 11, no. 1, pp. 85–101, 1990.
   https://doi.org/10.1016/0196-6774(90)90031-9

8. Zvi Galil and Kunsoo Park, “A linear-time algorithm for concave
   one-dimensional dynamic programming”, *Information Processing Letters*,
   vol. 33, no. 6, pp. 309–311, 1990.
   https://doi.org/10.1016/0020-0190(90)90215-J

9. David Eppstein, Zvi Galil, Raffaele Giancarlo, and Giuseppe F.
   Italiano, “Sparse dynamic programming ii: Convex and concave cost
   functions”, *Journal of the ACM*, vol. 39, no. 3, pp. 546–567, 1992.
   https://doi.org/10.1145/146637.146656

10. Alok Aggarwal and Takeshi Tokuyama, “Consecutive interval query and
    dynamic programming on intervals” in *Algorithms and computation: 4th
    international symposium, isaac ’93 hong kong, december 15–17, 1993
    proceedings*, K. W. Ng, P. Raghavan, N. V. Balasubramanian and F. Y. L.
    Chin (eds.),. Springer Berlin Heidelberg, Berlin, Heidelberg, pp.
    466–475., 1993. https://doi.org/10.1007/3-540-57568-5_278

11. Peter Becker, “Construction of nearly optimal multiway trees” in
    *Computing and combinatorics: Third annual international conference,
    cocoon ’97 shanghai, china, august 20–22, 1997 proceedings*, Tao Jiang
    and D. T. Lee (eds.),. Springer Berlin Heidelberg, Berlin, Heidelberg,
    pp. 294–303., 1997. https://doi.org/10.1007/BFb0045096

12. Oege de Moor and Jeremy Gibbons, “Bridging the algorithm gap: A
    linear-time functional program for paragraph formatting”, *Science of
    Computer Programming*, vol. 35, no. 1, pp. 3–27, 1999.
    https://doi.org/http://dx.doi.org/10.1016/S0167-6423(99)00005-2


Argument processing
-------------------

I usually use `click`_
for command-line utilities,
but due to the restriction (3) above,
all the argument processing was written in pure `argparse`_.

.. _click: http://click.pocoo.org/
.. _argparse: https://docs.python.org/3/library/argparse.html

