#!/usr/bin/env python3
"""Rebuild an Android boot image with MediaTek headers on the kernel and ramdisk.

Older MediaTek bootloaders refuse images whose kernel/ramdisk lack the 512-byte
MTK header. Usage: mtk_header.py <in.img> <out.img> [ramdisk-name]
"""
import hashlib
import struct
import sys

MTK_MAGIC = 0x58881688


def mtk_wrap(data, name):
    hdr = struct.pack('<II32s', MTK_MAGIC, len(data), name.encode())
    return hdr + b'\xff' * (512 - len(hdr)) + data


def pad(data, page):
    return data + b'\0' * (-len(data) % page)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    rd_name = sys.argv[3] if len(sys.argv) > 3 else 'RECOVERY'
    img = open(src, 'rb').read()
    if img[:8] != b'ANDROID!':
        sys.exit('not an Android boot image')
    (k_size, k_addr, r_size, r_addr, s_size, s_addr, tags, page) = struct.unpack_from('<8I', img, 8)
    pages = lambda n: (n + page - 1) // page
    k_off = page
    r_off = k_off + pages(k_size) * page
    s_off = r_off + pages(r_size) * page
    kernel = img[k_off:k_off + k_size]
    ramdisk = img[r_off:r_off + r_size]
    second = img[s_off:s_off + s_size]
    if struct.unpack_from('<I', kernel)[0] == MTK_MAGIC:
        sys.exit('image already has MTK headers')
    kernel = mtk_wrap(kernel, 'KERNEL')
    ramdisk = mtk_wrap(ramdisk, rd_name)

    header = bytearray(img[:page])
    struct.pack_into('<I', header, 8, len(kernel))
    struct.pack_into('<I', header, 16, len(ramdisk))
    sha = hashlib.sha1()
    for blob in (kernel, ramdisk, second):
        sha.update(blob)
        sha.update(struct.pack('<I', len(blob)))
    digest = sha.digest()
    header[576:576 + 32] = digest + b'\0' * (32 - len(digest))

    out = bytes(header) + pad(kernel, page) + pad(ramdisk, page) + pad(second, page)
    open(dst, 'wb').write(out)
    print('%s: %d bytes' % (dst, len(out)))


if __name__ == '__main__':
    main()
