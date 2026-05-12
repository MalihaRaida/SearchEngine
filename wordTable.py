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

   }
