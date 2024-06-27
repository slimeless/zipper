**Compressor CLI Documentation**
=============================

Overview
--------

The Compressor CLI is a command-line interface for compressing and decompressing files using various algorithms. Currently, it supports Huffman Coding and LZW (Lempel-Ziv-Welch) algorithms. This tool is designed to be easy to use for both beginners and experienced users.

Commands
--------

### 1. Compression (`cmp`)

Compresses the specified file using the chosen algorithm.

#### Usage:
```
zipper cmp [OPTIONS] PATH
```

#### Arguments:

* `PATH`: The path of the file to be compressed. This argument is required.

#### Options:

* `--algorithm`, `-a`: The algorithm to be used for compression. Supported values are `huff` for Huffman Coding and `lzw` for Lempel-Ziv-Welch. This option is required.

#### Example:
```
zipper cmp -a lzw /path/to/file
```

### 2. Decompression (`ucmp`)

Decompresses the specified file.

#### Usage:
```
zipper ucmp [OPTIONS] PATH
```

#### Arguments:

* `PATH`: The path of the file to be decompressed. The file must have a `.lzw` or `.huff` extension. This argument is required.

#### Options:

* `--output`, `-o`: The path of the output file or directory. If not specified, the decompressed file will be placed in the same directory as the input file.

#### Example:
```
zipper ucmp /path/to/file.lzw -o /path/to/output
```

Handling Errors
--------------

The CLI is designed to handle errors gracefully. If an error occurs during compression or decompression, the CLI will display an error message. Additionally, users have the option to automatically generate an issue link with the error details, which can be sent to the developers for further assistance.

#### Example:
```
Would you like to send issue? [y/N]: y
```

Contributing
------------

Contributions to the Compressor CLI are welcome. Please refer to the project's CONTRIBUTING guide for more details on how to contribute.

License
-------

The Compressor CLI is licensed under the MIT License. See the LICENSE file for more details.