VFClust
=======

This package is designed to generate clustering analyses for
transcriptions of semantic and phonemic verbal fluency test responses.
In a verbal fluency test, the subject is given a set amount of time
(usually 60 seconds) to name as many words as he or she can that
correspond to a given specification. For a phonemic test, subjects are
asked to name words that begin with a specific letter. For a semantic
fluency test, subjects are asked to provide words of a certain category,
e.g. animals. VFClust groups words in responses based on phonemic or
semantic similarity, as described below. It then calculates metrics
derived from the discovered groups and returns them as a CSV file or
Python dict object. For a detailed explanation of the reasoning
underlying the computation of these measures, please see:

Ryan et al., Computerized Analysis of a Verbal Fluency Test
[http://rxinformatics.umn.edu/downloads/VFCLUST/ryan\\\_acl2013.pdf](http://rxinformatics.umn.edu/downloads/VFCLUST/ryan\_acl2013.pdf)

Verbal fluency tests are often used in test batteries used to study
cognitive impairment arising from e.g. Alzheimer's disease, Parkinson's
disease, and certain medications. The following reference provides an
introduction to the use of clustering in cognitive evaluation.

Mayr, U. (2002). On the dissociation between clustering and switching in
verbal fluency: Comment on Troyer, Moscovitch, Winocur, Alexander and
Stuss. Neuropsychologia, 40(5), 562-566.

Clustering in VFClust
---------------------

VFClust finds adjacent subsets of words of the following types:

-   **clusters**: every entry in a cluster is sufficiently similar to every
    :   other entry

-   **chains**: every entry in a chain is sufficiently similar to adjacent
    :   entries

where "entry" corresponds to a word, compound word, or multiple adjacent
words with the same stem.

Similarity scores between words are thresholded and binarized using
empirically-derived thresholds. Overlap of clusters is allowed (a word
can be part of multiple clusters), but overlapping chains are not
possible, as any two adjacent words with a lower-than-threshold
similarity breaks the chain. Clusters subsumed by other clusters are not
counted.

The similarity measures used are the following:

-   **PHONETIC/"phone"**: the phonetic similarity score (PSS) is calculated
    :   between the phonetic representations of the input units. It is
        equal to 1 minus the Levenshtein distance between two strings,
        normalized to the length of the longer string. The strings
        should be compact phonetic representations of the two words.
        (This method is a modification of a Levenshtein distance
        function available at
        <http://hetland.org/coding/python/levenshtein.py>.)

-   **PHONETIC/"biphone"**: the binary common-biphone score (CBS) depends on
    :   whether two words share their initial and/or final biphone
        (i.e., set of two phonemes). A score of 1 indicates that two
        words have the same intial and/or final biphone; a score of 0
        indicates that two words have neither the same initial nor final
        biphone This is also calculated using the phonetic
        representation of the two words.

-   **SEMANTIC/"lsa"**: a semantic relatedness score (SRS) is calculated as
    :   the COSINE of the respective term vectors for the first and
        second word in an LSA space of the specified
        clustering\_parameter. Unlike the PHONETIC methods, this method
        uses the .text property of the input Unit objects.

-   **SEMANTIC/"custom"**: the user can specify a custom file of word similarities,
    :   in which each pair of words is given a custom similarity score.

### Output

After chains/clusters are discovered using the methods relevant for the
type of fluency test performed, metrics are derived from the clusters
and output to screen and a .csv file (if run as a script) or to a python
dict object (if run as a package). The following metrics are calculated:

Counts of different token types in the raw input. Each of these is
prefaced by ''COUNT\_'' in the output.

-   **total\_words**: count of words (i.e. utterances with semantic content)
    :   spoken by the subject. Filled pauses, silences, coughs, breaths,
        words by the interviewer, etc. are all excluded from this count.

-   **permissible\_words**: Number of words spoken by the subject that
    :   qualify as a valid response according to the clustering
        criteria. Compound words are counted as a single word in
        SEMANTIC clustering, but as two words in PHONETIC clustering.

-   **exact\_repetitions**: Number of words which repeat words spoken earlier
    :   in the response. Responses in SEMANTIC clustering are lemmatized
        before this function is called, so slight variations (dog, dogs)
        may be counted as exact responses.

-   **stem\_repetitions**: Number of words stems identical to words uttered
    :   earlier in the response, according to the Porter Stemmer. For
        example, 'sled' and 'sledding' have the same stem ('sled'), and
        'sledding' would be counted as a stem repetition.

-   **examiner\_words**: Number of words uttered by the examiner. These start
    :   with "E\_" in .TextGrid files.

-   **filled\_pauses**: Number of filled pauses uttered by the subject. These
    :   begin with "FILLEDPAUSE\_" in the .TextGrid file.

-   **word\_fragments**: Number of word fragments uttered by the subject.
    :   These end with "-" in the .TextGrid file.

-   **asides**: Words spoken by the subject that do not adhere to the test
    :   criteria are counted as asides, i.e. words that do not start
        with the appropriate letter or that do not represent an animal.

-   **unique\_permissible\_words**: Number of works spoken by the subject,
    :   less asides, stem repetitions and exact repetitions.

Measures derived from clusters/chains in the response. Each of these is
prefaced by ''COLLECTION\_'', along with the similarity measure used and
the collection type the measure was calculated over.

-   **pairwise\_similarity\_score\_mean**: mean of pairwise similarity
    :   scores. The pairwise similarity is calculated as the sum of
        similarity scores for all pairwise word pairs in a response --
        except any pair composed of a word and itself -- divided by the
        total number of words in an attempt. I.e., the mean similarity
        for all pairwise word pairs.

-   **count**: number of collections
-   **size\_mean**: mean size of collections
-   **size\_max**: size of largest collection
-   **switch\_count**: number of changes between clusters

Measures derived from timing information in the response, along with
clusters/chains. Each of these is prefaced by ''TIMING\_'' along with
the along with the similarity measure used and the collection type the
measure was calculated over.

-   **response\_vowel\_duration\_mean**: average vowel duration of all vowels
    :   in the response.

-   **response\_continuant\_duration\_mean**: average vowel duration of all
    :   vowels in the response.

-   **between\_collection\_interval\_duration\_mean**: average interval
    :   duration separating clusters. Negative intervals (for
        overlapping clusters) are counted as 0 seconds. Intervals are
        calculated as being the difference between the ending time of
        the last word in a collection and the start time of the first
        word in the subsequent collection. Note that these intervals are
        not necessarily silences, and may include asides, filled pauses,
        words from the examiner, etc.

-   **within\_collection\_interval\_duration\_mean**: the mean time between
    :   the end of each word in the collection and the beginning of the
        next word. Note that these times do not necessarily reflect
        pauses, as collection members could be separated by asides or
        other noises.

-   **within\_collection\_vowel\_duration\_mean**: average duration of vowels
    :   that occur within a collection

-   **within\_collection\_continuant\_duration\_mean**: average duration of
    :   continuants that occur within a collection.

### Dependencies

This package has been tested on Mac OS X (Mavericks). In order to run
the package you must have the following installed on your machine:

0.  Python 2.7
1.  **pip**: pip should install with Python 2.7. If for some reason pip
    :   is not installed, go to your terminal or commandline of choice
        and enter the command below:

<!-- -->

    easy_install pip

2.  **NLTK**: VFClust requires the Natural Language Toolkit (NLTK), as
    it uses the NLTK lemmatizer and stemmer in parsing subject
    responses. Check <http://www.nltk.org> for more information on how
    to install NLTK.

<!-- -->

    pip install nltk

3.  **numpy**: Some of the data files are stored as numpy arrays. This
    will change in future releases, but for now numpy is required to

<!-- -->

    pip install numpy

4.  **gcc**: On Mac OS X, you will need to install the latest version of
    Xcode compatible with your version of OS X with Command-line tools
    package (<https://developer.apple.com/xcode/>). Keep in mind that
    you may need to enable command-line tools in Xcode in order to be
    able to use the gcc compiler. If you can't run gcc from command-line
    after installing Xcode, go to the Xcode Preferences/Downloads tab
    and select the "Install" button, next to "Command Line Tools."

Installation
------------

There are two ways to install the package. VFClust is registered at
<http://pypi.python.org/>, so you can install it using:

    $ sudo pip install vfclust

The `sudo` is included because the setup process includes compiling a
file (t2p.c) and placing it in the install directory.

To install the package manually, download the .zip file from github.com
or the .tar.gz file from pypi.python.org. Extract the file, navigate to
the new directory in the terminal, and type

    $ sudo python setup.py install

You will need to have the gcc compiler installed on your system.
Installing also includes compiling a C executable for the
grapheme-to-phoneme conversion (t2p) that the phonetic clustering
package uses. If everything went okay, you should see the following
output in the console:

    success S AH0 K S EH1 S

along with other output from the install process.

There are three ways to run VFClust, and therefore three tests to make
sure it's running properly. If you installed using pip, you can test the
program using some of the included example files. You should be able to
type:

    $ vfclust test

If you simply downloaded the package, you can navigate to the "vfclust"
directory and type

    $ python vfclust.py test

If you are using vfclust within Python, type:

    >> import vfclust
    >> vfclust.test_script()

All results are the same in each case.

Deploying
---------

### *Input*

VFClust operations are performed on transcriptions of verbal fluency
tests. These can be recorded as either CSV files or TextGrid files. For
a CSV file, the first field should be the subject ID number, and each
remaining field should contain a response. For example:

    12345,fort,friend,fry,fetch,follow,um,i,don't,know,fall,felt

For a .TextGrid file, at this point the program expects two tiers, where
the first includes the word strings and the second includes the phone
strings. Here are the first few lines of an example file:

    File type = "ooTextFile"
    Object class = "TextGrid"

    xmin = 0
    xmax = 59.72
    tiers? <exists>
    size = 2
    item []:
        item [1]:
            class = "IntervalTier"
            name = "word"
            xmin = 0
            xmax = 59.72
            intervals: size = 65
            intervals [1]:
                 xmin = 0.00
                 xmax = 1.31
                 text = "!SIL"
            intervals [2]:
                 xmin = 1.31
                 xmax = 1.83
                 text = "CAT"
            intervals [3]:
                 xmin = 1.83
                 xmax = 2.22
                 text = "!SIL"
            intervals [4]:
                 xmin = 2.22
                 xmax = 2.72

In both .TextGrid and .csv files, non-word noises and responses can be
annotated using the following:

-   !SIL = silence
-   starts with E\_ = examiner word
-   FILLEDPAUSE\_um or FILLEDPAUSE\_ah = filled pause
-   T\_NOISE = noise
-   T\_COUGH = cough
-   T\_LIPSMACK = lipsmack
-   T\_BREATH = breath

These special tags will be used to generate a list of counts for Any
entry that is not one of these and does not fit into the specified
clustering category will be labeled as an aside.

### *As a script*

After installation, you should be able to use vfclust from the command
line simply by typing:

    vfclust [-h] [-s SEMANTIC] [-p PHONEMIC] [-o OUTPUT_PATH] [-q]
                  [--similarity-file SIMILARITY_FILE] [--threshold THRESHOLD]
                  source_file_path

with the relevant parameters.

If for some reason this doesn't work, you can navigate to the directory
containing the vfclust.py file (it should be in the vfclust/
subdirectory of the installed package) and type:

    python vfclust.py [-h] [-s SEMANTIC] [-p PHONEMIC] [-o OUTPUT_PATH] [-q]
                  [--similarity-file SIMILARITY_FILE] [--threshold THRESHOLD]
                  source_file_path

Bracketed arguments are optional, but either -s (semantic) or -p
(phonemic) must be selected. The arguments are as follows:

    positional arguments:
      source_file_path      Full path of textgrid or csv file to parse

    optional arguments:
      -h, --help            show this help message and exit
      -s SEMANTIC           Usage: -s animals If included, calculates measures for
                            the given category for the semantic fluency test, i.e.
                            animals, fruits, etc.
      -p PHONEMIC           Usage: -p f If included, calculates measures for the
                            given category for the phonemic fluency test, i.e. a,
                            f, s, etc.
      -o OUTPUT_PATH        Where to put output - default is the same directory as
                            the input file working directory.
      -q                    Use to eliminate output (default is print everything
                            to stdout).
      --similarity-file SIMILARITY_FILE
                            Usage: --similarity-file /path/to/similarity/file
                            Location of custom word similarity file. Each line
                            must contain two words separated by a space, followed
                            by a comma and the similarity number. For example,
                            "horse dog,1344.3969" is a valid line. If used, the
                            default "LSA" option is overridden. You must also
                            include a threshold number with --threshold X.
      --threshold THRESHOLD
                            Usage: --threshold X, where X is a number. A custom
                            threshold is required when including a custom
                            similarity file. A custom threshold can also be set
                            when using semantic or phonemic clustering. In this
                            case, it would override the default threshold
                            implemented in the program.

For example, to run clustering on a phonetic verbal fluency test using
the letter "f", where the response was saved as a .csv file, type:

    vfclust  -p f /path/to/response/response.csv

Similarly, to run clustering on a semantic verbal fluency test using the
category "animals", where the response is recorded as a .TextGrid file,
type

    vfclust  -s animals /path/to/response/response.TextGrid

To use a custom similarity file, type something like the following:

    python vfclust.py --similarity-file path/to/similarity/file.txt --threshold 0.5 /path/to/response/response.TextGrid

By default, the results are printed to screen and a .csv file is created
in the same directory as the response.csv file. You can output the
results to a different directory by using the -o flag.

### *As a Python package*

The functionality in the `vfclust` script is accessed using the
`vfclust.get_duration_measures` method. The method inputs are as
follows:

    :param source_file_path: Required. Location of the .csv or .TextGrid file to be
        analyzed.
    :param output_path: Path to which to write the resultant csv file. If left None,
        path will be set to the source_file_path.  If set to False, no file will be
        written.
    :param phonemic: The letter used for phonetic clustering. Note: should be False if
        semantic clustering is being used.
    :param semantic: The word category used for semantic clustering. Note: should be
        False if phonetic clustering is being used.
    :param quiet: Set to True if you want to suppress output to the screen during processing.
    :param similarity_file (optional): When doing semantic processing, this is the path of
        a file containing custom term similarity scores that will be used for clustering.
        If a custom file is used, the default LSA-based clustering will not be performed.
    :param threshold (optional): When doing semantic processing, this threshold is used
        in conjunction with a custom similarity file. The value is used as a semantic
        similarity cutoff in clustering. This argument is required if a custom similarity
        file is specified.  This argument can also be used to override the built-in
        cluster/chain thresholds.

    :return data: A dictionary of measures derived by clustering the input response.

and can be called by typing

    >> import vfclust
    >> results = vfclust.get_duration_measures(source_file_path = '/path/to/response/response.TextGrid',
                                                output_path = '/output/directory/'
                                                phonemic = 'a')

If you enter invalid arguments or both the "phonemic" and "semantic"
arguments, an exception will be raised.

### *Using a custom similarity file*

You can also specify word similarities using a separate file. If this is
done, words in the response will be counted as "permissible" and as
legitimate members of clusters only if they appear somewhere in this
file. VFClust will also assume all words in the file are already
tokenized, i.e. "polar bear" should be written as "polar\_bear".

Each line of the file must be formatted with two words separated by a
space, followed by a comma and a number:

    elk bison,114.9277
    guinea_pig mouse,113.2803
    panther puma,112.4150
    cat skunk,112.2775
    cardinal finch,111.5717
    squirrel elephant,111.2780

When using a custom similarity file, you must also explicitly specify a
custom threshold using the --threshold argument.

ACKNOWLEDGEMENTS
----------------

This package uses a grapheme-to-phoneme conversion (t2p) implementation
by the MBRDICO Project (<http://tcts.fpms.ac.be/synthesis/mbrdico/>).

The English Open Word List is used as a basic dictionary of English
words. <http://dreamsteep.com/projects/the-english-open-word-list.html>

The NLTK (<http://www.nltk.org>) WordNet 3.0 Corpus is used for
lemmatizing words.

License
-------

All files which are included as a part of the VFClust Phonetic
Clustering Module are provided under an Apache license, excluding:

-   t2p.c in the data/t2p directory, which is provided under a GPL
    license
-   the NLTK WordNet 3.0 corpus, which is Copyright 2006 by Princeton
    University. The full text of the license is available in the corpus
    files.
-   english\_words.txt in the data/EOWL directory, which is a
    modification of the UK Advanced Cryptics Dictionary and is released
    with the following licensing:

Copyright J Ross Beresford 1993-1999. All Rights Reserved. The following
restriction is placed on the use of this publication: if the UK Advanced
Cryptics Dictionary is used in a software package or redistributed in
any form, the copyright notice must be prominently displayed and the
text of this document must be included verbatim.

