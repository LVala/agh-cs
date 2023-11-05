package main.java;

import com.zeroc.Ice.Current;
import com.zeroc.Ice.Util;

public class FUWSObjectI implements Demo.FUWSObject {
  private final int servantId;
  private int counter = 0;

  public FUWSObjectI(int id) {
    servantId = id;
    System.out.println("Created new FUWS servant with id " + id);
  }

  public int incrementAndGet(Current current) {
    System.out.println("incrementAndGet called on object " 
      + Util.identityToString(current.id) + ", servant id: " + servantId);
    return ++counter;
  }
}
