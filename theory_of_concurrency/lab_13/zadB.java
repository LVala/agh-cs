class Producer implements CSProcess {
    private One2OneChannel out;
    private int n;
    
    public Producer(One2OneChannelInt out, int n) {
        this.out = out;
        this.n = n;
    }

    public void run() {
        for (int i=0; i<n; ++i) {
            var item = n;
            out.out().write(item);
        }
    }
}

class Consumer implements CSProcess {
    private One2OneChannelInt in;
    private int n;
    
    public Consumer(One2OneChannelInt in, int n) {
        this.in = in;
        this.n = n;
    }

    public void run() {
        var start = System.currentTimeMillis();
        for (int i=0; i<n; ++i) {
            int item = in.in().read();
        }

        var end = System.currentTimeMillis();
        System.out.println("Time: " + (end - start) + " ms");
        System.exit(0);
    }
}

class Buffer implements CSProcess {
    private One2OneChannelInt in;
    private One2OneChannelInt out;

    public Buffer(One2OneChannelInt in, One2OneChannelInt out) {
        this.out = out;
        this.in = in;
    }

    public void run() {
        while (true) {
            out.out().write(in.in().read());
        }
    }
}

class Main {
    public static void main(String[] args) {
        int buffers = 100;
        int items = 10000;
        var channelIntFactory = new StandardChannelIntFactory();
        var channels = channelIntFactory.createOne2One(buffers + 1);

        var procs = new CSProcess[buffers + 2];
        procs[0] = new Producer(channels[0], items);
        procs[1] = new Consumer(channels[buffers], items);

        for (int i=0; i<buffers; ++i) {
            procs[i+2] = new Buffer(channels[i], channels[i + 1]);
        }

        new Parallel(procs).run();
    }
}