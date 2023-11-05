class Fork {
    private boolean available = true;

    public synchronized void pickUp() {
        while (!available) {
            try {
                wait();
            } catch (InterruptedException e) {
                System.exit(0);
            }
        }
        
        available = false;
    }
    
    public synchronized void putDown() {
        available = true;
        notifyAll();
    }

    public boolean isAvailable() {
        return this.available;
    }
}
    
class Philosopher extends Thread {
    private int counter = 0;
    private Fork rightFork;
    private Fork leftFork;
    private Waiter waiter;

    public Philosopher(Fork leftFork, Fork rightFork, Waiter waiter) {
        this.leftFork = leftFork;
        this.rightFork = rightFork;
        this.waiter = waiter;
    }
    
    public void run() {
        while (true) {

        thinkOrEat(500);
    
        waiter.giveForks(leftFork, rightFork);

        thinkOrEat(100);
        ++counter;
        if (counter % 100 == 0) {
            System.out.println("Philosopher: " + Thread.currentThread() + 
                " have eaten " + counter + " times");
        }

        waiter.takeForks(leftFork, rightFork);
        }
    }

    public void thinkOrEat(long time) {
        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            System.exit(0);
        }
    }
}

class Waiter {
    private int forksTaken = 0;

    public synchronized void giveForks(Fork leftFork, Fork rightFork) {
        while (!leftFork.isAvailable() || !rightFork.isAvailable()) 
            try {
                wait();
            } catch (InterruptedException e) {
                System.exit(0);
            }

        while (forksTaken == 4) {
            try {
                wait();
            } catch (InterruptedException e) {
                System.exit(0);
            }
        }

        forksTaken += 2;
        leftFork.pickUp();
        rightFork.pickUp();
    }

    public synchronized void takeForks(Fork leftFork, Fork rightFork) {
        forksTaken -= 2;
        leftFork.putDown();
        rightFork.putDown();
        notifyAll();
    }

}
    
public class Fil5mon {
    public static void main(String[] args) throws InterruptedException {
        int n = 5;

        Philosopher[] philosophers = new Philosopher[n];
        Fork[] forks = new Fork[n];

        for (int i=0; i<n; ++i) {
            forks[i] = new Fork();
        }

        Waiter waiter = new Waiter();

        for (int i=0; i<n; ++i) {
            philosophers[i] = new Philosopher(forks[i], forks[(i+1)%n], waiter);
        }

        for (int i=0; i<n; ++i) {
            philosophers[i].start();
        }

        for (int i=0; i<n; ++i) {
            philosophers[i].join();
        }
    }
}