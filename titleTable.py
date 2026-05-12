   class TitleTable {
      //OVERVIEW: Keeps track of documents with their titles.
     

      // constructors
      TitleTable ( )
         // EFFECTS: Initializes this to be an empty table.


      // methods
      void addDoc (Doc d) throws DuplicateException
         // REQUIRES: d is not null 
         // MODIFIES:  this 
         // EFFECTS: If a document with d ’s title is already in this throws
         //   DuplicateException else adds d with its title to this.
 
      Doc lookup (String t) throws NotPossibleException
         // EFFECTS: If t is null or there is no document with title t in this 
         //        throws NotPossibleException else returns the document with title t.

   }