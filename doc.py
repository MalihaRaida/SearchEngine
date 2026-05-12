class Doc {
      // OVERVIEW: A document contains a title and a text body.
  
      // methods
      String title ( )
          // EFFECTS: Returns the title of this.

      String body ( )
          // EFFECTS: Returns the body of this.
          
        // constructors
      Query ( )
         // EFFECTS: Returns the empty query.


      Query (WordTable wt, String w)
        // REQUIRES: wt and w are not null
        // EFFECTS: Makes a query for the single keyword w.


      // methods
      void addKey (String w) throws NotPossibleException
         // REQUIRES: w is not null
         // MODIFIES:  this
         // EFFECTS: If this is empty or w is already a keyword in the query
         //   throws NotPossibleException else modifies this to contain the
         //   query for w and all keywords already in this.
 
      void addDoc (Doc d)
        // REQUIRES: d is not null
        // MODIFIES: this 
        // EFFECTS: If this is not empty and d contains all the keywords of
        //this adds it to this as a query result else does nothing.

   }

