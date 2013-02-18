###  Chmura słów - word clouds engine ###

This is a statistical engine for word clouds  that takes the Polish language
flexibility into account. 

* Licence

See COPYING. This project is (C) Centrum Cyfrowe: Projekt Polska and is
covered by GNU General Public Licence V3 or later.

* Deployment

This is a set of two Django apps. To deploy this project create Django
runtime environment (django-admin startproject <directory>), deploy the apps
in that directory, enable them in settings.py and do a syncdb.

* The language problem

In Polish language words are flexible, almost all words. The words
"przetwarzać", "przetwarzałem", "przetworzę" ale the same word in various
forms. Thus before making a "word cloud" visualization it is needed to
transform all of the words of the text into basic forms (lemmas). Only after
then the statistics may be produced and displayed

** Database

The core of the statistics engine is the word database. It consists of
following tables (Django data models):

 # Lemma (table: word_lemma)

This is the canonical form of the word, as it will be displayed in
statistics and all of the actual speech words will point to it.

 -- in case of nouns, it should be the nominative article, singular form
    (mianownik liczby pojedyńczej)

 -- verbs should be in the infinitive form

 -- for adjectives it is best to be stored in indefinite third person
    neutral gender form

 # Word (table: word_word)

This is the actual word taken from a speech. It has following properties
(columns):

  -- prev/next - pointers (ForeignKeys) to previous/next Word of the speech
     (double linked list)

  -- lemma - pointer to Lemma of the word

  -- word - clean (lowercase, punctuation stripped) form of the word

  -- display - actual form of the word in speech text with punctuation and
     uppercase letters

  -- speech - pointer to Speech object describing the speech that the word
     belongs to.

It is possible to have a few copies of a single speech in the word database,
but it will break all the statistics count.  To prevent this, the example
loader script will try to delete all the word objects that point to speech
it is loading before the process starts.  Due to limitations in the Django
ORM, the process may fail, it is then necessary to delete the data from SQL
console by hand. 

 # Dict

This is a dictionary that maps clean words (word.word) to lemmas.

  -- word - clean form of the word for lookup

  -- lemma - pointer to lemma of the word

 # Ignore

Ignore list, lemmas that are linked in that table will be skipped from the
display.

 # Stat

This is a cache of word counts in speeches. It needs to be refreshed (by
triggering 'chmura.word.views.cache' view after any change to the word
database.

** The loading process

Supplied in the word application directory is "loader.py" script. It is an
example loader that supports building the word database and dictionary from
supplied speeches texts. During the process the loader extracts consecutive
words from the texts and matches them to lemma and dictionary databases.

 --  if the word matches a known dictionary word, it is added automatically.

 -- if the word is similar to any of the lemmas, the user is asked whether to
assign it to any of the lemmas, or to create a new lemma by hand.

* Contact

In case of question please contact Alex Urbanowicz <aurbanowicz at
centrumcyfrowe.pl>.