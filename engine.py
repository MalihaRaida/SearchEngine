  class Engine {
     // OVERVIEW: An engine has a state as described in the search engine
     //   data model. The methods throw the NotPossibleException
     //   when there is a problem; the exception contains a string explaining
     //   the problem. All instance methods modify the state of this.

     // constructors
     Engine( ) throws NotPossibleException
        // EFFECTS: If the uninteresting words cannot be retrieved from the
        //  persistent state throws NotPossibleException else creates NK and
        //  initializes the application state appropriately.

     // methods
     Query queryFirst (String w) throws NotPossibleException
        // EFFECTS: If ¬WORD(w) or w in NK throws NotPossibleException else
        //  sets Key = { w }, performs the new query, and returns the result.

     Query queryMore (String w) throws NotPossibleException
        // EFFECTS: If ¬WORD(w) or w in NK or Key = { } or w in Key throws
        //  NotPossibleException else adds w to Key and returns the query result.

     Doc findDoc (String t) throws NotPossibleException
        // EFFECTS: If t not in Title throws NotPossibleException
        //   else returns the document with title t.
 
     Query addDocs (String u) throws NotPossibleException
        // EFFECTS: If u is not a URL for a site containing documents or u in URL
        //  throws NotPossibleException else adds the new documents to Doc.
        //  If no query was in progress returns the empty query result else
        //  returns the query result that includes any matching new documents.
 }