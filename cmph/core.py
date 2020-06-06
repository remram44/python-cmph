from cmph._ffi import ffi, lib


def test():
    # Example from http://cmph.sourceforge.net/
    vector = [
        "aaaaaaaaaa", "bbbbbbbbbb", "cccccccccc", "dddddddddd", "eeeeeeeeee",
        "ffffffffff", "gggggggggg", "hhhhhhhhhh", "iiiiiiiiii", "jjjjjjjjjj",
    ]
    lib.build_hash(
        '/tmp/temp.mph'.encode('utf-8'),
        [ffi.new('char[]', k.encode('utf-8')) for k in vector],
        len(vector),
    )

    for key in vector:
        lib.find_key(
            '/tmp/temp.mph'.encode('utf-8'),
            key.encode('utf-8'),
        )
