import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Condition;

class Producer extends Thread {
	private Buffer buf;
    private int max;

    public Producer(Buffer buf, int max) {
        this.buf = buf;
        this.max = max;
    }

	public void run() {
      int iters = ThreadLocalRandom.current().nextInt(0, max + 1);

	  for (int i = 0; i < iters; ++i) {
		buf.put(i);
	  }
	}
}

class Consumer extends Thread {
	private Buffer buf;
    private int max;

    public Consumer(Buffer buf, int max) {
        this.buf = buf;
        this.max = max;
    }

	public void run() {
      int iters = ThreadLocalRandom.current().nextInt(0, max + 1);

	  for (int i = 0; i < iters; ++i) {
		System.out.println(buf.get());
	  }
	}
}

class Buffer {
    private List<Integer> buf = new ArrayList<Integer>();
    private int size;

    private ReentrantLock lock = new ReentrantLock();
    Condition stackEmptyCondition = lock.newCondition();
    Condition stackFullCondition = lock.newCondition();

    public Buffer(int size) {
        this.size = size;
    }

    public void put(int i) {
        try {
            lock.lock();
            while(buf.size() == size) {
                stackFullCondition.await();
            }
            buf.add(i);
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                System.exit(0);
            }
            stackEmptyCondition.signalAll();
        } catch (InterruptedException e) {
            System.exit(0);
        } finally {
            lock.unlock();
        }
    }

    public int get() {
        try {
            lock.lock();
            while(buf.isEmpty()) {
                stackEmptyCondition.await();
            }
            int retVal = buf.get(0);
            buf.remove(0);
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                System.exit(0);
            }
            return retVal;
        } catch (InterruptedException e) {
            System.exit(0);
            return 0;
        } finally {
            stackFullCondition.signalAll();
            lock.unlock();
        }  
    }
}

public class ProdConUtils {

    public static void main(String[] args) throws InterruptedException {
        int M = 100;
        Buffer buff = new Buffer(2*M);

        int m = 3;
        int n = 3;

        ExecutorService service = Executors.newFixedThreadPool(n + m);

        long startTime = System.nanoTime();

        for (int i=0; i<m; ++i) {
            service.submit(new Producer(buff, M));
        }

        for (int i=0; i<m; ++i) {
            service.submit(new Consumer(buff, M));
        }

        service.shutdown();
        while (!service.awaitTermination(24L, TimeUnit.HOURS)) 
            ;

        long endTime = System.nanoTime();
        System.out.println((endTime-startTime)/1000000);
    }
}
