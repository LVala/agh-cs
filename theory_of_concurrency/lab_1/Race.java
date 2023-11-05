class Counter {
    private int _val;
    public Counter(int n) {
        _val = n;
    }
    public void inc() {
        _val++;
    }
    public void dec() {
        _val--;
    }
    public int value() {
        return _val;
    }
}

class IThread extends Thread {
    private Counter counter;

    public IThread(Counter counter) {
        this.counter = counter;
    }

    public void run() {
        for (int i=0; i<10_000; ++i) {
            counter.inc();
        }
    }
}

class DThread extends Thread {
    private Counter counter;

    public DThread(Counter counter) {
        this.counter = counter;
    }

    public void run() {
        for (int i=0; i<10_000; ++i) {
            counter.dec();
        }
    }
}

public class Race {
    public static void main(String[] args) throws InterruptedException {

        Counter cnt = new Counter(0);
        DThread dthread = new DThread(cnt);
        IThread ithread = new IThread(cnt);

        dthread.start();
        ithread.start();
        dthread.join();
        ithread.join();

        System.out.println(cnt.value());
    }
}
