package main.java;

import com.zeroc.Ice.Util;
import com.zeroc.Ice.Object;
import com.zeroc.Ice.Current;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.ServantLocator;

class RUWSServantLocator implements ServantLocator {
  private int assignedId = 1;

  public ServantLocator.LocateResult locate(Current current) {
    RUWSObjectI ruws = new RUWSObjectI(assignedId++);
    return new ServantLocator.LocateResult(ruws, null);
  }

  public void finished(Current current, Object servant, java.lang.Object cookie) {}
  public void deactivate(String category) {}
}

public class Server {
  private void serve(String[] args) {
    try(com.zeroc.Ice.Communicator communicator = Util.initialize(args)) {
      ObjectAdapter adapter = communicator.createObjectAdapter("DemoAdapter");

      // create single servant for "singleton" object and add it to ASM
      Object fuws = new FUWSObjectI(1);
      adapter.add(fuws, Util.stringToIdentity("singleton"));

      // add servant locator for "ruws" category
      RUWSServantLocator sl = new RUWSServantLocator();
      adapter.addServantLocator(sl, "ruws");

      // add default servant for "fuwos" category
      FUWOSObjectI fuwos = new FUWOSObjectI(1);
      adapter.addDefaultServant(fuwos, "fuwos");

      adapter.activate();
      System.out.println("Entering event processing loop...");
      communicator.waitForShutdown();
    }
  }

  public static void main(String[] args) {
    Server app = new Server();
    app.serve(args);
  }
}
