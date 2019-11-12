Intruvu
=======

## Installation

```bash
python -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Défi

Main file to launch for the challenge.

### Execution

```bash
python defi.py
```

### Arguments

```bash
  -h, --help            show this help message and exit
  -r                    Index files to ElasticSearch and exit the program.
                        Files must be indexed before working with classifiers.
  --index INDEX         Name of the ElasticSearch index to use.
                        default: "flow"
  --dir_train DIR_TRAIN
                        Directory to load the XML training file(s) from.
                        This directory contain the file(s) used for the training.
                        It shouldn't contain any file with unknown tag.
                        default: "./defi_train"
  --dir_test DIR_TEST   Directory to load the XML test file(s) from.
                        This directory contain the file(s) used for the test.
                        default: "./defi_test"
  --output OUTPUT       Name of the output file containing the results.
                        default: "output"
```

## Main

Main file we used for the project.

### Execution

```bash
python main.py
```

### Arguments

```bash
  -h, --help            show this help message and exit
  -r                    Index files to ElasticSearch and exit the program.
                        Files must be indexed before working with classifiers.
  --index INDEX         Name of the ElasticSearch index to use.
                        default: "flow"
  --dir DIR             Directory to load the XML file(s) from. 
                        This directory contain the file(s) used for the classification.
                        default: "./ISCX_train"
```

## Zipf

Display a Zipf diagram.

### Execution

```bash
python zipf.py
```

### Arguments

```bash
  -h, --help            show this help message and exit
  -r                    Index files to ElasticSearch and exit the program.
                        Files must be indexed before working with classifiers.
  --index INDEX         Name of the ElasticSearch index to use.
                        default: "flow"
  --dir DIR             Directory to load the XML file(s) from. 
                        This directory contain the file(s) used for the classification.
                        default: "./ISCX_train"
```