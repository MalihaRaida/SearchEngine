class DocCnt implements Comparable {
// overview: DocCnt is a record like type with two fields, a Doc
// and an integer.
// methods
int compareTo (Object x) throws ClassCastException, NullPointerException
// effects: If x is null throws NullPointerException; if x isn’t a DocCnt
// object, throws ClassCastException. Otherwise, if this.cnt < x.cnt
// returns -1; if this.cnt = x.cnt returns 0; else returns 1.
}