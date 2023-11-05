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
    private CountingSemaphore semaphore;

    public IThread(Counter counter, CountingSemaphore semaphore) {
        this.counter = counter;
        this.semaphore = semaphore;
    }

    public void run() {
        for (int i=0; i<10_000; ++i) {
            semaphore.P();
            counter.inc();
            semaphore.V();
        }
    }
}

class DThread extends Thread {
    private Counter counter;
    private CountingSemaphore semaphore;

    public DThread(Counter counter, CountingSemaphore semaphore) {
        this.counter = counter;
        this.semaphore = semaphore;
    }

    public void run() {
        for (int i=0; i<10_000; ++i) {
            semaphore.P();
            counter.dec();
            semaphore.V();
        }
    }
}

public class Race {
    public static void main(String[] args) throws InterruptedException {

        Counter cnt = new Counter(0);
        CountingSemaphore semaphore = new CountingSemaphore();
        DThread dthread = new DThread(cnt, semaphore);
        IThread ithread = new IThread(cnt, semaphore);

        dthread.start();
        ithread.start();
        dthread.join();
        ithread.join();

        System.out.println(cnt.value());
    }
}
