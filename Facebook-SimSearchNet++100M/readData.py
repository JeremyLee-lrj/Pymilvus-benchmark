import json
import struct
import numpy as np

# with open("D:/Download/dqs_address.txt", "r", encoding="utf-8") as file:
#     lines = file.readlines()
#
# data = []
#
# for line in lines:
#     data.append(line)
# print(len(data))
# with open("D:/Download/dqs_address.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, ensure_ascii=False)


def read_fbin(filename, start_idx=0, chunk_size=None):
    """ Read *.fbin file that contains float32 vectors
    Args:
        :param filename (str): path to *.fbin file
        :param start_idx (int): start reading vectors from this index
        :param chunk_size (int): number of vectors to read.
                                 If None, read all vectors
    Returns:
        Array of float32 vectors (numpy.ndarray)
    """
    with open(filename, "rb") as f:
        nvecs, dim = np.fromfile(f, count=2, dtype=np.int32)
        # print(nvecs, dim)
        nvecs = (nvecs - start_idx) if chunk_size is None else chunk_size
        arr = np.fromfile(f, count=nvecs * dim, dtype=np.uint8,
                          offset=start_idx * 4 * dim)
    return arr.reshape(nvecs, dim)


data = read_fbin("FB_ssnpp_database.u8bin")
print(data.shape)

print(data[0][0])
print(type(data[0][0]))
