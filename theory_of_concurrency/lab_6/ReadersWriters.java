import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

class Writer extends Thread {
    Resource resource;
    int count;

    public Writer(Resource resource, int count) {
        this.resource = resource;
        this.count = count;
    }

    public void run() {
        for (int i=0; i<count; ++i) {
            try {
                resource.write();
            } catch (InterruptedException e) {
                System.exit(1);
            }
        }
    }
}

class Reader extends Thread {
    Resource resource;
    int count;

    public Reader(Resource resource, int count) {
        this.resource = resource;
        this.count = count;
    }

    public void run() {
        for (int i=0; i<count; ++i) {
            try {
                resource.read();
            } catch (InterruptedException e) {
                System.exit(1);
            }
        }
    }
}

class Resource {
    ReentrantLock lock = new ReentrantLock();
    Condition isAvailableCondition = lock.newCondition();
    boolean isAvailable = true;
    int readCount = 0;

    public void write() throws InterruptedException {
        lock.lock();
        while (!isAvailable) {
            isAvailableCondition.await();
        }
        isAvailable = false;
        lock.unlock();

        // writing
        Thread.sleep(ThreadLocalRandom.current().nextInt(10) * 9);

        lock.lock();
        isAvailable = true;
        isAvailableCondition.signalAll();
        lock.unlock();
    }

    public void read() throws InterruptedException {
        lock.lock();
        ++readCount;
        if (readCount == 1) {
            while (!isAvailable) {
                isAvailableCondition.await();
            }
            isAvailable = false;
        }
        lock.unlock();

        // reading
        Thread.sleep(ThreadLocalRandom.current().nextInt(10) * 3);

        lock.lock();
        --readCount;
        if (readCount == 0) isAvailable = true;
        isAvailableCondition.signalAll();
        lock.unlock();
    }
}

public class ReadersWriters {
    public static void main(String[] args) throws InterruptedException {
        for (int writers=1; writers<11; ++writers) {
            for (int readers=10; readers<101; readers += 10) {
                Resource resource = new Resource();
            
                ExecutorService service = Executors.newFixedThreadPool(writers + readers);

                long startTime = System.nanoTime();

                for (int i=0; i<writers; ++i) {
                    service.submit(new Writer(resource, 3));
                }

                for (int i=0; i<readers; ++i) {
                    service.submit(new Reader(resource, 3));
                }

                service.shutdown();
                while (!service.awaitTermination(24L, TimeUnit.HOURS)) 
                    ;

                long endTime = System.nanoTime();


                System.out.print(writers + " " + readers + " ");
                System.out.println((endTime - startTime)/1000000);
            }
        }
    }
}
