from app.utils.pagination import paginate


def test_paginate_collects_all():
    pages = [([1, 2], "a"), ([3], None)]

    def fetch(token):
        return pages.pop(0)

    out = paginate(fetch)
    assert out == [1, 2, 3]

