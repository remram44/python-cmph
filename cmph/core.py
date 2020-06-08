import typing

from cmph._ffi import ffi, lib


class CmphError(Exception):
    """Error from cmph extension."""


class PerfectHash(object):
    """A perfect hash function.
    """
    def __init__(self, mph):
        self._mph = mph

    def __del__(self):
        if self._mph is not None:
            lib.destroy_hash(self._mph)
            self._mph = None

    @staticmethod
    def load(filename: str) -> 'PerfectHash':
        mph = lib.load_hash(filename.encode('utf-8'))
        if mph == ffi.NULL:
            raise CmphError("Error loading file: %r" % filename)
        return PerfectHash(mph)

    @staticmethod
    def build(
        keys: typing.List[str],
        algo: str,
    ) -> 'PerfectHash':
        mph = lib.build_hash(
            [
                ffi.new('char[]', k.encode('utf-8'))
                for k in keys
            ],
            len(keys),
            ffi.new('char[]', algo.encode('utf-8')),
        )
        if mph == ffi.NULL:
            raise CmphError("Error building hash")
        return PerfectHash(mph)

    @staticmethod
    def build_brz(
        filename: str,
        keys: typing.List[str],
    ):
        ret = lib.build_hash_brz(
            ffi.new('char[]', filename.encode('utf-8')),
            [
                ffi.new('char[]', k.encode('utf-8'))
                for k in keys
            ],
            len(keys),
        )
        if ret != 0:
            raise CmphError("Error building hash")

    def find(self, key: str) -> int:
        return lib.find_key(
            self._mph,
            key.encode('utf-8'),
        )
