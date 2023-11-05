import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

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

    public Buffer(int size) {
        this.size = size;
    }

    public synchronized void put(int i) {
        while (buf.size() >= size) {
            try {
                wait();
            } catch (InterruptedException e) {
                System.exit(0);
            }
        }

        buf.add(i);
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            System.exit(0);
        }
        notifyAll();
    }

    public synchronized int get() {
        while (buf.isEmpty()) {
            try {
                wait();
            } catch (InterruptedException e) {
                System.exit(0);
            }
        }

        int retVal = buf.get(0);
        buf.remove(0);
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            System.exit(0);
        }
        notifyAll();
        return retVal;
    }
}

public class ProdCon {

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
        System.out.print("TIME: ");
        System.out.println((endTime - startTime)/1000000);
    }
}
