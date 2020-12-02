#!/usr/bin/env python3

import pytest

from . import misc


def test_misc_test_version_tag_eval():
    def _ver_eval(ver_tags, version):
        r = misc.test_version_tag_eval(ver_tags, version)
        assert r is True or r is False

        def _invert_op(op):
            if op == "+=":
                return "-"
            if op == "+":
                return "-="
            if op == "-":
                return "+="
            assert op == "-="
            return "+"

        ver_tags_invert = [(_invert_op(op), ver) for op, ver in ver_tags]

        r2 = misc.test_version_tag_eval(ver_tags_invert, version)
        assert r2 is True or r2 is False
        if r == r2:
            pytest.fail(
                f'Version "{version}" is {"satisfied" if r else "unsatisfied"} by {ver_tags}, but it is also wrongly {"satisfied" if r2 else "unsatisfied"} by the inverse {ver_tags_invert}'
            )

        return r

    assert _ver_eval([("+=", [1, 26])], [1, 28, 5])
    assert _ver_eval([("+=", [1, 26])], [1, 26, 5])
    assert _ver_eval([("+=", [1, 26])], [1, 26, 0])
    assert not _ver_eval([("+=", [1, 26])], [1, 25, 6])
    assert not _ver_eval([("+=", [1, 26])], [1, 25, 0])

    assert _ver_eval([("+", [1, 26])], [1, 28, 5])
    assert not _ver_eval([("+", [1, 26])], [1, 26, 5])
    assert not _ver_eval([("+", [1, 26])], [1, 26, 0])
    assert not _ver_eval([("+", [1, 26])], [1, 25, 6])
    assert not _ver_eval([("+", [1, 26])], [1, 25, 0])

    assert not _ver_eval([("-=", [1, 26])], [1, 28, 5])
    assert _ver_eval([("-=", [1, 26])], [1, 26, 5])
    assert _ver_eval([("-=", [1, 26])], [1, 26, 0])
    assert _ver_eval([("-=", [1, 26])], [1, 25, 6])
    assert _ver_eval([("-=", [1, 26])], [1, 25, 0])

    assert not _ver_eval([("-", [1, 26])], [1, 28, 5])
    assert not _ver_eval([("-", [1, 26])], [1, 26, 5])
    assert not _ver_eval([("-", [1, 26])], [1, 26, 0])
    assert _ver_eval([("-", [1, 26])], [1, 25, 6])
    assert _ver_eval([("-", [1, 26])], [1, 25, 0])

    assert _ver_eval([("+=", [1, 26, 0])], [1, 28, 5])
    assert _ver_eval([("+=", [1, 26, 0])], [1, 26, 5])
    assert _ver_eval([("+=", [1, 26, 0])], [1, 26, 0])
    assert not _ver_eval([("+=", [1, 26, 0])], [1, 25, 6])
    assert not _ver_eval([("+=", [1, 26, 0])], [1, 25, 0])

    assert _ver_eval([("+", [1, 26, 0])], [1, 28, 5])
    assert _ver_eval([("+", [1, 26, 0])], [1, 26, 5])
    assert not _ver_eval([("+", [1, 26, 0])], [1, 26, 0])
    assert not _ver_eval([("+", [1, 26, 0])], [1, 25, 6])
    assert not _ver_eval([("+", [1, 26, 0])], [1, 25, 0])

    assert not _ver_eval([("-=", [1, 26, 0])], [1, 28, 5])
    assert not _ver_eval([("-=", [1, 26, 0])], [1, 26, 5])
    assert _ver_eval([("-=", [1, 26, 0])], [1, 26, 0])
    assert _ver_eval([("-=", [1, 26, 0])], [1, 25, 6])
    assert _ver_eval([("-=", [1, 26, 0])], [1, 25, 0])

    assert not _ver_eval([("-", [1, 26, 0])], [1, 28, 5])
    assert not _ver_eval([("-", [1, 26, 0])], [1, 26, 5])
    assert not _ver_eval([("-", [1, 26, 0])], [1, 26, 0])
    assert _ver_eval([("-", [1, 26, 0])], [1, 25, 6])
    assert _ver_eval([("-", [1, 26, 0])], [1, 25, 0])

    assert _ver_eval([("+=", [1, 26, 2])], [1, 28, 5])
    assert _ver_eval([("+=", [1, 26, 2])], [1, 26, 5])
    assert _ver_eval([("+=", [1, 26, 2])], [1, 26, 2])
    assert not _ver_eval([("+=", [1, 26, 2])], [1, 26, 0])
    assert not _ver_eval([("+=", [1, 26, 2])], [1, 25, 6])
    assert not _ver_eval([("+=", [1, 26, 2])], [1, 25, 0])

    assert _ver_eval([("+", [1, 26, 2])], [1, 28, 5])
    assert _ver_eval([("+", [1, 26, 2])], [1, 26, 5])
    assert not _ver_eval([("+", [1, 26, 2])], [1, 26, 2])
    assert not _ver_eval([("+", [1, 26, 2])], [1, 26, 0])
    assert not _ver_eval([("+", [1, 26, 2])], [1, 25, 6])
    assert not _ver_eval([("+", [1, 26, 2])], [1, 25, 0])

    assert not _ver_eval([("-=", [1, 26, 2])], [1, 28, 5])
    assert not _ver_eval([("-=", [1, 26, 2])], [1, 26, 5])
    assert _ver_eval([("-=", [1, 26, 2])], [1, 26, 2])
    assert _ver_eval([("-=", [1, 26, 2])], [1, 26, 0])
    assert _ver_eval([("-=", [1, 26, 2])], [1, 25, 6])
    assert _ver_eval([("-=", [1, 26, 2])], [1, 25, 0])

    assert not _ver_eval([("-", [1, 26, 2])], [1, 28, 5])
    assert not _ver_eval([("-", [1, 26, 2])], [1, 26, 5])
    assert not _ver_eval([("-", [1, 26, 2])], [1, 26, 2])
    assert _ver_eval([("-", [1, 26, 2])], [1, 26, 0])
    assert _ver_eval([("-", [1, 26, 2])], [1, 25, 6])
    assert _ver_eval([("-", [1, 26, 2])], [1, 25, 0])

    assert _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 28, 5])
    assert _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 26, 5])
    assert not _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 26, 2])
    assert not _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 26, 0])
    assert not _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 25, 6])
    assert not _ver_eval([("+", [1, 26, 2]), ("+", [1, 27])], [1, 25, 0])

    assert not _ver_eval(
        [("+=", [1, 26, 8]), ("+=", [1, 28, 6]), ("+=", [1, 29, 4])], [1, 28, 5]
    )
    assert _ver_eval(
        [("+=", [1, 26, 8]), ("+=", [1, 28, 6]), ("+=", [1, 29, 4])], [1, 28, 8]
    )

    assert _ver_eval([("+=", [1, 26, 8]), ("+=", [1, 28])], [1, 28, 5])
    assert _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28])], [1, 29, 0])
    assert not _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28])], [1, 28, 5])
    assert not _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28, 4])], [1, 28, 2])
    assert not _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28, 4])], [1, 28, 4])
    assert _ver_eval([("+=", [1, 26, 8]), ("+=", [1, 28, 4])], [1, 28, 4])
    assert _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28, 4])], [1, 28, 5])
    assert _ver_eval([("+=", [1, 26, 8]), ("+", [1, 28, 4])], [1, 29, 0])

    # the following is a special case during release candidate phase.
    # Imagine a fix/feature gets added to (before) 1.29.3, and also
    # backported to nm-1-28 branch. At that time, 1.28.0 is not yet released,
    # but nm-1-28 is after 1.27.90 and the backport happens (before) 1.27.90.
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 26, 0],
    )
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 26, 4],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 26, 5],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 26, 6],
    )
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 27, 0],
    )
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 27, 90],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 27, 91],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 27, 92],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 27, 99],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 28, 0],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 28, 1],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 28, 2],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 28, 99],
    )
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 29, 0],
    )
    assert not _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 29, 1],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 29, 2],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 29, 3],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 29, 99],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 30, 0],
    )
    assert _ver_eval(
        [
            ("+=", [1, 26, 5]),
            ("+=", [1, 27, 91]),
            ("+=", [1, 28, 0]),
            ("+=", [1, 29, 2]),
        ],
        [1, 30, 2],
    )

    # Now the inverse...
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 26, 0],
    )
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 26, 4],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 26, 5],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 26, 6],
    )
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 27, 0],
    )
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 27, 90],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 27, 91],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 27, 92],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 27, 99],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 28, 0],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 28, 1],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 28, 2],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 28, 99],
    )
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 29, 0],
    )
    assert _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 29, 1],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 29, 2],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 29, 3],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 29, 99],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 30, 0],
    )
    assert not _ver_eval(
        [("-", [1, 26, 5]), ("-", [1, 27, 91]), ("-", [1, 28, 0]), ("-", [1, 29, 2]),],
        [1, 30, 2],
    )
