class Query {
      // OVERVIEW: Provides information about the keywords of a query and
      //   the documents that match those keywords. size returns the number
      //   of matches. Documents can be accessed using indexes between 0 and
      //   size. Documents are ordered by the number of matches they
      //   contain, with document 0 containing the most matches.

      // methods
      String[ ] keys ( )
        // EFFECTS: Returns the keywords of this.

      int size ( )
        // EFFECTS: Returns a count of the documents that match the query.
   
      Doc fetch (int i) throws IndexOutOfBoundsException
         //  EFFECTS: If 0 <= i < size returns the ith matching document else
         //   throws IndexOutOfBoundsException.
         
     // constructors
     Doc (String d) throws NotPossibleException
        // EFFECTS: If d cannot be processed as a document throws
        // NotPossibleException else makes this be the Doc
        // Corresponding to d.

      void addDoc (Doc d, Hashtable h)
// requires: d is not null and h maps strings (the interesting words
// in d) to integers (the count of occurrences of the word in d).
// modifies: this
// effects: If each keyword of this is in h, adds d to matches of this.


   }