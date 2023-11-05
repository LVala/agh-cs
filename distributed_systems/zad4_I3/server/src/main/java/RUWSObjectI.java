package main.java;

import com.zeroc.Ice.Current;
import com.zeroc.Ice.Util;

public class RUWSObjectI implements Demo.RUWSObject {
  private final int servantId;

  public RUWSObjectI(int id) {
    servantId = id;
    System.out.println("Created new RUWS servant with id " + id);
  }

  public void saveALotOfData(String data, Current current) {
    System.out.println("saveALotOfData called on object " 
      + Util.identityToString(current.id) + ", servant id: " + servantId + ", data: " + data);
    // do something with data that requires a lot of memory
    // and not sharing this objects state with other threads
  }
}
