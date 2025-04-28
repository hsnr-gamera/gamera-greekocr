=========================================================
A basic example for using the GreekOCR toolkit for Gamera
=========================================================

This archive contains a test image and training data for
demonstrating the GreekOCR toolkit for Gamera.

Have fun,

Christian Brandt, Christoph Dalitz
Niederrhein University of Applied Sciences
Krefeld, Germany


Prerequisites
-------------

To run the usage examples, you must have a working installation
of the following software:

 - Gamera framework for document analysis and recognition
 - OCR toolkit for Gamera
 - GreekOOCR toolkit for Gamera

All of these are available from the Gamera home page

    http://gamera.sf.net/


Contents
--------

 - ``image.png``
   A test image that can be recognized with the given training data.
   The image has been scanned from J. Borst: "Herodot Geschichten."
   Klett Verlag, Stuttgart (1951), p.5. The image is provided for
   testing purposes only to demonstrate the use of the GreekOCR
   toolkit.

 - ``training-wholistic.xml`` ``training-separatistic.xml``
   Training data for wholistic resp. separatistic recognition.

 - ``symbols-wholistic.xml`` ``symbols-separatistic.xml``
   Example symbol tables for wholistic resp. separatistic training.
   These can be useful during the training process; they can
   be loaded into the classifier GUI via the menu
   "File/Symbol names/Import"


Usage examples
--------------

To create a Unicode textfile "wholistic.txt" using the wholistic
approach, enter at the shell prompt

  greekocr4gamera -x training-wholistic.xml -w --unicode wholistic.txt image.png


To create a Unicode textfile "seaparatistic.txt" using the separatistic
approach, enter at the shell prompt

  greekocr4gamera -x training-separatistic.xml -s --unicode separatistic.txt image.png


To create an LaTeX file "wholistic.tex" using the wholistic approach
and the Teubner style for representing Greek letters and accents,
enter at the shell prompt

  greekocr4gamera -x training-wholistic.xml -w --teubner wholistic.tex image.png


To create an LaTeX file "separatistic.tex" using the separatistic
approach and the Teubner style for representing Greek letters and
accents, enter at the shell prompt

  greekocr4gamera -x training-separatistic.xml -s --teubner separatistic.tex image.png


The latex files can be translated to a readable PDF file with (beware that,
on Ubuntu, this requires installation of the package ``cm-super``)

  pdflatex wholistic.tex
  pdflatex separatistic.tex


