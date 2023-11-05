import java.util.concurrent.locks.ReentrantLock;

class BlockingList {
    public class ListElement {
        public Object value;
        public ListElement next;

        public ListElement(Object value, ListElement next) {
            this.value = value;
            this.next = next;
        }
    }

    ReentrantLock lock = new ReentrantLock();

    // dummy first element
    ListElement first = new ListElement(null, null);

    private boolean sublistContains(Object value, ListElement element) {
        if (element.value == value) return true;
        else if (element.next != null) return sublistContains(value, element.next);
        else return false;
    }

    public boolean contains(Object value) {
        lock.lock();
        if (first.next == null) return false;
        boolean res = sublistContains(value, first.next);
        lock.unlock();
        return res;
    }

    private void sublistRemove(Object value, ListElement element, ListElement prevElement) {
        if (element.value == value) {
            prevElement.next = element.next;
        } else if (element.next != null) {
            sublistRemove(value, element.next, element);
        }
    }

    public void remove(Object value) {
        lock.lock();
        if (first.next != null) {
            sublistRemove(value, first.next, first);
        }
        lock.unlock();
    }

    private void sublistAdd(Object value, ListElement element) {
        if (element.next == null) element.next = new ListElement(value, null);
        else sublistAdd(value, element.next);
    }

    public void add(Object value) {
        lock.lock();
        sublistAdd(value, first);
        lock.unlock();
    }
}

class FineGrainedList {
    public class ListElement {
        public ReentrantLock lock = new ReentrantLock();
        public Object value;
        public ListElement next;

        public ListElement(Object value, ListElement next) {
            this.value = value;
            this.next = next;
        }
    }

    // dummy first element
    ListElement first = new ListElement(null, null);

    private boolean sublistContains(Object value, ListElement element) {
        if (element.value == value) {
            element.lock.unlock();
            return true;
        }
        if (element.next != null) {
            element.next.lock.lock();
            element.lock.unlock();
            return sublistContains(value, element.next);
        }
        element.lock.unlock();
        return false;
    }

    public boolean contains(Object value) {
        first.lock.lock();
        if (first.next == null) {
            first.lock.unlock();
            return false;
        }
        return sublistContains(value, first.next);
    }

    private void sublistRemove(Object value, ListElement element, ListElement prevElement) {
        if (element.value == value) {
            prevElement.next = element.next;
            prevElement.lock.unlock();
            element.lock.unlock();
        } else if (element.next != null) {
            prevElement.lock.unlock();
            element.next.lock.lock();
            sublistRemove(value, element.next, element);
        } else {
            prevElement.lock.unlock();
            element.lock.unlock();
        }
    }

    public void remove(Object value) {
        if (first.next != null) {
            first.lock.lock();
            first.next.lock.lock();
            sublistRemove(value, first.next, first);
        }
    }

    private void sublistAdd(Object value, ListElement element) {
        if (element.next == null) {
            element.next = new ListElement(value, null);
            element.lock.unlock();
        } else {
            element.next.lock.lock();
            element.lock.unlock();
            sublistAdd(value, element.next);
        }
    }
    
    public void add(Object value) {
        first.lock.lock();
        sublistAdd(value, first);
    }
}

public class ListsComparison {
    public static void main(String[] args) {

        FineGrainedList list = new FineGrainedList();
    }
}
