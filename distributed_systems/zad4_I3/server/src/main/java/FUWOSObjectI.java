package main.java;

import com.zeroc.Ice.Current;
import com.zeroc.Ice.Util;

public class FUWOSObjectI implements Demo.FUWOSObject {
  private final int servantId;

  public FUWOSObjectI(int id) {
    servantId = id;
    System.out.println("Created new FUWOS servant with id " + id);
  }

  public String concatWords(String first, String second, Current current) {
    System.out.println("concatWords called on object " 
      + Util.identityToString(current.id) + ", servant id: " + servantId);
    return first + second;
  }
}
