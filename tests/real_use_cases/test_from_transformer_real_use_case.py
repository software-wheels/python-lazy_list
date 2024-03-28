from . import LazyList
from dataclasses import dataclass
from time import sleep, time
import lzma
from typing import *

@dataclass
class File:
    content: str

@dataclass
class ZipFile:
    compressed_content: bytes

@dataclass
class ZipArchive:
    compressed_files: List[ZipFile]

class Zip:
        
    def compress_file(self, file: File) -> ZipFile:
        return ZipFile(compressed_content=lzma.compress(file.content.encode()))
    
    def compress_files(self, files: List[File]) -> ZipArchive:
        return ZipArchive(compressed_files=[self.compress_file(file) for file in files])
    
    def extract_zip_file(self, zip_file: ZipFile):
        sleep(1) # decompressing time
        return File(content=lzma.decompress(zip_file.compressed_content).decode())
    
    def extract_zip_archive(self, zip_archive: ZipArchive, lazy=True) -> Sequence[File]:
        if lazy:
            return LazyList.from_transformer(zip_archive.compressed_files, self.extract_zip_file)
        else:
            return [self.extract_zip_file(zip_file) for zip_file in zip_archive.compressed_files]



def test_from_transformer_real_use_case():
    
    file1 = File(content="data1")
    file2 = File(content="data2")
    file3 = File(content="data3")

    zip = Zip()
    zip_archive = zip.compress_files([file1, file2, file3])

    start = time()
    files = zip.extract_zip_archive(zip_archive=zip_archive, lazy=True) # use lazy
    second_file = files[1]
    end = time()

    assert second_file.content == "data2"
    assert 1 < end - start < 2 # assert that we only extracted one file. each file take 1 second.

    start = time()
    files = zip.extract_zip_archive(zip_archive=zip_archive, lazy=False) # not use lazy
    second_file = files[1]
    end = time()

    assert second_file.content == "data2"
    assert 3 < end - start # since we not using lazy, all files will be extracted. this should take at least 3 seconds.