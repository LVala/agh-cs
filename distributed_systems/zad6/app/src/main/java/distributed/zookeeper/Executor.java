package distributed.zookeeper;

import java.io.IOException;
import java.util.List;

import javafx.application.Platform;
import javafx.stage.Stage;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

public class Executor
    implements Watcher, Runnable, DataMonitor.DataMonitorListener {
    private final String ADDRESS = "localhost:2181,localhost:2182,localhost:2183";
    private final String znode = "/z";

    private String cmd;
    private DataMonitor dm;
    private ZooKeeper zk;
    private Process child;

    private MainWindow mainWindow;

    public Executor(String cmd) throws KeeperException, IOException {
        this.cmd = cmd;
        this.zk = new ZooKeeper(ADDRESS, 3000, this);
        this.dm = new DataMonitor(this.zk, znode, this);

        this.mainWindow = new MainWindow(this);
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Missing `cmd` argument");
            System.exit(2);
        }
        try {
            new Executor(args[0]).run();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void run() {
        Platform.startup(() -> {
            Stage stage = new Stage();
            this.mainWindow.start(stage);
        });

        try {
            synchronized (this) {
                while (!dm.dead) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
        }
    }

    public void process(WatchedEvent event) {
        dm.process(event);
    }

    public void closing(int rc) {
        synchronized (this) {
            notifyAll();
        }
    }

    public void exists(boolean exists) {
        if (exists && child == null) {
            try {
                String exec[] = {cmd};
                child = Runtime.getRuntime().exec(exec);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else if (!exists && child != null) {
            child.destroy();
            try {
                child.waitFor();
            } catch (InterruptedException e) {
            }
            child = null;
        }
    }

    public void descendantChanged() {
        int number = doGetDescendantsNumber(this.znode);
        Platform.runLater(() -> {
            this.mainWindow.updateDescendantsCountLabel(number - 1);
        });
    }

    private int doGetDescendantsNumber(String node) {
        int number = 1; 
        try {
            List<String> children = zk.getChildren(node, false);
            for (String child: children) {
                number += doGetDescendantsNumber(node + "/" + child);
            }
        } catch (KeeperException e) {
            if (e.code() == KeeperException.Code.NONODE) {
                return 0;
            }
            System.exit(1);
        } catch (InterruptedException e) {
            System.exit(1);
        }
        return number;
    }

    public String getDescendantsTreeString() {
        StringBuilder tree = new StringBuilder(); 
        doGetDescandantsTreeString(tree, this.znode);
        return tree.toString();
    }

    private void doGetDescandantsTreeString(StringBuilder tree, String node) {
        try {
            List<String> children = zk.getChildren(node, false);
            tree.append(node + "\n");
            for (String child: children) {
                doGetDescandantsTreeString(tree, node + "/" + child);
            }
        } catch (KeeperException e) {
            if (e.code() == KeeperException.Code.NONODE) {
                return;
            }
            System.exit(1);
        } catch (InterruptedException e) {
            System.exit(1);
        }
    }
}
