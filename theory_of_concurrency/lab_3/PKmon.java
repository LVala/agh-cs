import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.w3c.dom.css.CSS2Properties;

import java.util.Random;

class BinarySemaphore {
    private boolean state;

    public BinarySemaphore() {
        this.state = true;
    }

    public synchronized void P() {
        while (!state) {
            try {
                wait();  
            }
            catch (InterruptedException e) {
                System.exit(0);
            }
        }

        state = false;
    }
    
    public synchronized void V() {
        state = true;
        notifyAll();
    }
}

class CountingSemaphore {
    private int count;
    private BinarySemaphore binarySemaphore;

    public CountingSemaphore(int count) {
        this.count = count;
        this.binarySemaphore = new BinarySemaphore();
    }

    public void P() {
        binarySemaphore.P();
        synchronized (this) {
            --count;
            if (count > 0) {
                binarySemaphore.V();
            }
        }
    }
    
    public synchronized void V() {
        ++count;
        if (count == 1) {
            binarySemaphore.V();
        }
    }
} 

class Producer extends Thread {
	private Buffer buf;
    private int iters;

    public Producer(Buffer buf, int iters) {
        this.buf = buf;
        this.iters = iters;
    }

	public void run() {
	  for (int i = 0; i < iters; ++i) {
		buf.put(i);
        try {
            sleep(100);
        } catch (InterruptedException e) {
            System.exit(0);
        }
	  }
	}
}
		
class Consumer extends Thread {
	private Buffer buf;
    private int iters;

    public Consumer(Buffer buf, int iters) {
        this.buf = buf;
        this.iters = iters;
    }

	public void run() {
	  for (int i = 0; i < iters; ++i) {
		System.out.println(buf.get());
        try {
            sleep(100);
        } catch (InterruptedException e) {
            System.exit(0);
        }
	  }
	}
}

class Processor extends Thread {



    public void run() {

    }
}
		
class Buffer {
    private List<Integer> buf = new ArrayList<Integer>();
    private CountingSemaphore empty;
    private CountingSemaphore full;

    public Buffer(int size) {
        this.empty = new CountingSemaphore(size);
        this.full = new CountingSemaphore(0);
    }

    public synchronized void put(int i) {

        empty.P();
        buf.add(i);
        full.V();
    }

    public synchronized int get() {

        full.P();
        int index = new Random().nextInt(buf.size());
        int retVal = buf.get(index);
        buf.remove(index);
        empty.V();
        return retVal;
    }
}

public class PKmon {    
    public static void main(String[] args) throws InterruptedException {
        Buffer buf = new Buffer(100);
        int n1 = 3;
        int n2 = 3;

        int iters1 = 70;
        int iters2 = 70;

        if (n1*iters1 != n2*iters2) throw new RuntimeException("Invalid parameters");

        ExecutorService service = Executors.newFixedThreadPool(n1 + n2);

        final long startTime = System.currentTimeMillis();

        for(int i=0; i<n1; ++i) {
            service.submit(new Producer(buf, iters1));
        }

        for(int i=0; i<n2; ++i) {
            service.submit(new Consumer(buf, iters2));
        }

        service.shutdown();
        while (!service.awaitTermination(24L, TimeUnit.HOURS)) 
            ;
        final long endTime = System.currentTimeMillis();
        System.out.println(endTime - startTime);
    }
}