stc
===

A tool for Short Text Categorization. 
A library and a console application designed for short text classification. It let you train and use classifiers of short texts such as filenames. The input texts are provided in XML files (console application, library) or as C structures (library). 


Download the data
-----------------

Training data and the ready to use models can be downloaded from http://cental.fltr.ucl.ac.be/team/panchenko/stc/data.tgz. 
Download this archive and extract to the data directory:

```
cd ./data && wget http://cental.fltr.ucl.ac.be/team/panchenko/stc/data.tgz && tar xzf data.tgz && rm -f data.tgz
```

The archive contains several models:

- **gallery** -- The *Gallery* dataset, composed of titles of pornographic galleries (positives) and wikipedia articles (negatives). Here the model was trained on 90% of the data (train.xml) and can be tested on 10% of the rest data (valid.xml)

- **gallery-full** -- The *Gallery* dataset. Here the model was train on the entire dataset (train.xml contain 100% of the dataset).

- **tdt** -- The *PirateBay Title-Description-Tag* dataset, composed of file names of PirateBay torrent tracker. Positives are file names under the 'Porn' category. Negatives are file names of all other categories e.g. 'Games', 'Music', etc.  Here the model was trained on 90% of the data (train.xml) and can be tested on 10% of the rest data (valid.xml)

- **tdt-full** -- The *PirateBay Title-Description-Tag*. Here the model was train on the entire dataset (train.xml contain 100% of the dataset).

- **tt** -- The *PirateBay Title-Tag* dataset, composed of file names of PirateBay torrent tracker. Positives are file names under the 'Porn' category. Negatives are file names of all other categories e.g. 'Games', 'Music', etc.  Here the model was trained on 90% of the data (train.xml) and can be tested on 10% of the rest data (valid.xml)

- **tt-full** -- The *PirateBay Title-Tag*. Here the model was train on the entire dataset (train.xml contain 100% of the dataset).

- **test** -- Test model.

- **relations.csv** -- Set of semantic relations used by the models.

 **relations-large.csv** -- An alternative large scale set of semantic relations.


Binary Verison 
--------------

**Synopsis**

Directory *bin* contains a ready to use binary of the software for Ubuntu Linux platform (32-bit version), which consist of the follwing files:

- *libshort_text_classifier.so*
A shared library which which implements the text classifier. This library has the following dependencies: *libboost_filesystem.so, libboost_regex.so, libboost_system.so, liblinear.so*.

- *textclassifier.h*
A header file which provide a C interface to the text classification library.

- *iniparams.h* 
An additional header file.

- *libboost_filesystem.so*
A dependency of *libshort_text_classifier.so*.

- *libboost_regex.so*
A dependency of *libshort_text_classifier.so*.

- *libboost_system.so*
A dependency of *libshort_text_classifier.so*.

- *liblinear.so*
A dependency of *libshort_text_classifier.so*.

**System requirements**

Ubuntu Linux. The software was tested on 64-bit Ubuntu Lunux 11.10 and 12.04.
The program was compiled in 32-bit Release mode with g++ (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3 
on Ubuntu Linux 12.04 64-bit. 

**Installation**

0. For Ubuntu 12.04 -- install 32-bit C++ libraries: "sudo apt-get install ia32-libs"

1. Copy library files (.so) to /usr/lib32/. Make sure that you did not overwrite existing .so libraries.

2. Register the new shared libraries: "sudo ldconfig"

3. Copy the binary *stc* in any directory. 

**Usage of the console application**

./stc [OPTIONS]

Options:

 -M - mode, required:
         t - train a text classification model.
         p - classify text with an existing model.
         e - extract features from text.

 -i - input XML file with texts, required.

 -s - stopwords file, required.

 -p - stop part of speech file, required.

 -r - semantic relations file, required.

 -V - vocabulary file, required. Input for prediction mode, output for the training mode.

 -m - model file, required. Input for prediction mode, output for training mode.

 -N - normalization of bag-of-word feature vectors, default 'u'.
         0 - frequency counts of words (no normalization)
         1 - unit length normalization

 -v true - verbose output

 -R - type of the text expansion, default '0'.
         0 - no expansion
         1 - first order expansion
         2 - second order expansion
         3 - recursive expansion

 -E - number of per term expansions, default '0'.

 -W - weight [0;1] of the expanded terms w.r.t. original terms, default '0'.

 -h - print this help message

**Usage of the library**

3. Link your C or C++ program to *libshort_text_classifier.so*. Directory client-sample contains an example of a C program linked to the library (see makefile in Debug directory). You can open client-sample with Eclipse CDT or compile it with the provided makefile. 

4. Copy *textclassifier.h* and *iniparam.h* to your include directory.

5. Include *textclassifier.h* file in your C or C++ program.

6. Use functions defined *textclassifier.h* to manipulate the classifier (see the header for the documentation). An example of library usage:

```
IniParam* ip = get_iniparam();
void* cm = TextClassifier_Create(ip);
TextClassifier_PrintInfo(cm);
TextClassifier_Reload(cm, ip);
TextClassifier_PrintInfo(cm);
TextToClassify* text = classifier->load_texts(params.inputFile);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 1, text);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 2, text);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 3, text);
TextClassifier_Train(cm, 3, text);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 1, text);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 2, text);
TextClassifier_Predict(cm, (params.inputFile + ".xml").c_str(), 3, text);
TextClassifier_PrintInfo(cm);
TextClassifier_Destroy(cm);
```

Data
----

The training/test data are in the *data* directory. 
To downloat all training data:

1. cd ./data

2. wget http://cental.fltr.ucl.ac.be/team/panchenko/stc/data.tgz && tar xzf data.tgz && rm -f data.tgz

Recompilation
-------------

On Ubuntu 11.10 or higher install in addition to the packages indicated above:

1. cd ./include

2. wget http://cental.fltr.ucl.ac.be/team/panchenko/stc/boost-include.tgz && tar xzf boost-include.tgz && rm -f boost-include.tgz

3. sudo apt-get install libc6-dev-i386

4. sudo apt-get install g++-multilib

5. make

Note: Alternatively to the make, you can build the sources in Eclipse. The Eclipse CDT projects are in library and client directories. Build in the Release mode.

