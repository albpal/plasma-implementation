from typing import (
    NewType,
    TypeVar,
    Union,
)

Address = NewType('Address', bytes)  # for canonical Addresses
BlockNumber = NewType('BlockNumber', int)
ContractName = NewType('ContractName', str)
Hash32 = NewType('Hash32', bytes)
HexAddress = NewType('HexAddress', str)  # for hex encoded addresses
HexStr = NewType('HexStr', str)
Primitives = Union[bytes, int, bool]  # for conversion utils
URI = NewType('URI', str)

ChecksumAddress = NewType('ChecksumAddress', HexAddress)  # for hex addresses with checksums

AnyAddress = TypeVar('AnyAddress', Address, HexAddress, ChecksumAddress)
