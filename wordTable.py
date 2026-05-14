   class WordTable {
      // OVERVIEW: Keeps track of both interesting and uninteresting words.
      //   The uninteresting words are obtained from a private file. Records
      //   the number of times each interesting word occurs in each document.

      // constructors
      WordTable ( ) throws NotPossibleException
         // EFFECTS: If the file cannot be read throws NotPossibleException
         //   else initializes the table to contain all the words in the file
         //   as uninteresting words.

      // methods
      boolean isInteresting (String w)
         // EFFECTS: If w is null or a nonword or an uninteresting word
         //    returns false else returns true.


   void addDoc (Doc d)
 
      // REQUIRES: d is not null 
      // MODIFIES: this
      // EFFECTS: Adds all interesting words of d to this with a count
      // of their number of occurrences.


Vector lookup (String k)
// requires: k is not null.
// effects: Returns a vector of DocCnts where the Doc contains k cnt times.
Hashtable addDoc (Doc d)
// requires: d is not null
// modifies: this
// effects: Adds information about d’s interesting words and their
// number of occurrences to this; also returns a table mapping each
// interesting word in d to its number of occurrences



   }
