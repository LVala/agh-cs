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
