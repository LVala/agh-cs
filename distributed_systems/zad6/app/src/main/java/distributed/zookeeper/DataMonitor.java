package distributed.zookeeper;

import java.util.List;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.AsyncCallback.StatCallback;
import org.apache.zookeeper.AsyncCallback.ChildrenCallback;
import org.apache.zookeeper.KeeperException.Code;
import org.apache.zookeeper.data.Stat;

public class DataMonitor implements Watcher, StatCallback, ChildrenCallback {
    ZooKeeper zk;
    String znode;
    boolean dead;
    DataMonitorListener listener;

    public DataMonitor(ZooKeeper zk, String znode, DataMonitorListener listener) {
        this.zk = zk;
        this.znode = znode;
        this.listener = listener;
        zk.exists(znode, true, this, null);
        zk.getChildren(znode, true, this, null);
    }

    public interface DataMonitorListener {
        void exists(boolean exists);
        void descendantChanged();
        void closing(int rc);
    }

    public void process(WatchedEvent event) {
        String path = event.getPath();
        if (event.getType() == Event.EventType.None) {
            switch (event.getState()) {
            case SyncConnected:
                break;
            case Expired:
                dead = true;
                listener.closing(KeeperException.Code.SessionExpired);
                break;
            }
        } else {
            if (path != null && path.equals(znode)) {
                zk.exists(znode, true, this, null);
            }
            if (path != null && path.startsWith(znode)) {
                zk.getChildren(path, true, this, null);
            }
        }
    }

    public void processResult(int rc, String path, Object ctx, Stat stat) {
        boolean exists;
        switch (rc) {
        case Code.Ok:
            exists = true;
            break;
        case Code.NoNode:
            exists = false;
            break;
        case Code.SessionExpired:
        case Code.NoAuth:
            dead = true;
            listener.closing(rc);
            return;
        default:
            zk.exists(znode, true, this, null);
            return;
        }

        listener.exists(exists);
    }

    public void processResult(int rc, String path, Object ctx, List<String> children) {
        boolean exists;
        switch (rc) {
        case Code.Ok:
            exists = true;
            break;
        case Code.NoNode:
            exists = false;
            break;
        case Code.SessionExpired:
        case Code.NoAuth:
            dead = true;
            listener.closing(rc);
            return;
        default:
            zk.getChildren(path, true, this, null);
            return;
        }

        listener.descendantChanged();

        if (exists) {
            for (String child : children) {
                zk.getChildren(path + "/" + child, true, this, null);
            }
        }
        
    }
}
