from cmph.core import PerfectHash
from cmph._ffi import ffi, lib


def test_direct_brz():
    # Example from http://cmph.sourceforge.net/
    vector = [
        "aaaaaaaaaa", "bbbbbbbbbb", "cccccccccc", "dddddddddd", "eeeeeeeeee",
        "ffffffffff", "gggggggggg", "hhhhhhhhhh", "iiiiiiiiii", "jjjjjjjjjj",
    ]
    ret = lib.build_hash_brz(
        ffi.new('char[]', '/tmp/temp.mph'.encode('utf-8')),
        [ffi.new('char[]', k.encode('utf-8')) for k in vector],
        len(vector),
    )
    assert ret == 0

    mph = lib.load_hash('/tmp/temp.mph'.encode('utf-8'))
    for key in vector:
        h = lib.find_key(
            mph,
            key.encode('utf-8'),
        )
        print("%s %d" % (key, h))

    lib.destroy_hash(mph)


def test_brz():
    vector = [
        "aaaaaaaaaa", "bbbbbbbbbb", "cccccccccc", "dddddddddd", "eeeeeeeeee",
        "ffffffffff", "gggggggggg", "hhhhhhhhhh", "iiiiiiiiii", "jjjjjjjjjj",
    ]
    PerfectHash.build_brz('/tmp/temp.mph', vector)

    mph = PerfectHash.load('/tmp/temp.mph')
    for key in vector:
        h = mph.find(key)
        print("%s %d" % (key, h))


def test_bmz():
    vector = [
        "aaaaaaaaaa", "bbbbbbbbbb", "cccccccccc", "dddddddddd", "eeeeeeeeee",
        "ffffffffff", "gggggggggg", "hhhhhhhhhh", "iiiiiiiiii", "jjjjjjjjjj",
    ]
    mph = PerfectHash.build(vector, 'BMZ')
    for key in vector:
        h = mph.find(key)
        print("%s %d" % (key, h))

    mph = PerfectHash.load('/tmp/temp.mph')
    for key in vector:
        h = mph.find(key)
        print("%s %d" % (key, h))


if __name__ == '__main__':
    test_direct_brz()
    test_brz()
    test_bmz()
