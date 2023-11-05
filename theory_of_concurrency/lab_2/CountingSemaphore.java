class CountingSemaphore {
    private int count;
    private BinarySemaphore binarySemaphore;

    public CountingSemaphore() {
        this.count = 1;
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