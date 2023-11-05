class Producer implements CSProcess {
    private One2OneChannelInt[] out;
    private One2OneChannelInt[] yet;
    private int n;
    
    public Producer(One2OneChannelInt[] out, One2OneChannelInt[] yet, int n) {
        this.out = out;
        this.yet = yet;
        this.n = n;
    }

    public void run() {
        var guards = new Guard[yet.length];
        for (int i=0; i<out.length; ++i) {
            guards[i] = yet[i].in();
        }

        var alt = new Alternative(guards);
        for (int i=0; i<n; ++i) {
            var idx = alt.select();
            yet[idx].in().read();

            var item = n;
            out[idx].out().write(item);
        }
    }
}

class Consumer implements CSProcess {
    private One2OneChannelInt[] in;
    private int n;

    public Consumer(One2OneChannelInt[] in, int n) {
        this.in = in;
        this.n = n;
    }

    public void run() {
        var start = System.currentTimeMillis();
        var guards = new Guard[in.lenght];
        for (int i=0; i< in.length; ++i) {
            guards[i] = int[i].in();
        }

        var alt = new Alternative(guards);
        for (int i=0; i<n; ++i) {
            int idx = alt.select();
            int item = in[idx].in().read();
        }

        var end = System.currentTimeMillis();
        System.out.println("Time: " + (end - start) + " ms");
        System.exit(0);
    }
}

class Buffer implements CSProcess {
    private One2OneChannelInt in;
    private One2OneChannelInt out;
    private One2OneChannelInt yet;

    public Buffer(One2OneChannelInt in, One2OneChannelInt out, One2OneChannelInt yet) {
        this.out = out;
        this.in = in;
        this.yet = yet;
    }

    public void run() {
        while (true) {
            yet.out().write(0);
            out.out().write(in.in().read());
        }
    }
}

class Main {
    public static void main(String[] args) {
        int buffers = 100;
        int items = 10000;
        var channelIntFactory = new StandardChannelIntFactory();
        var prodChannel = channelIntFactory.createOne2One(buffers);
        var consChannel = channelIntFactory.createOne2One(buffers);
        var bufferChannel = channelIntFactory.createOne2One(buffers);

        var procs = new CSProcess[buffers + 2];
        procs[0] = new Producer(prodChannel, bufferChannel, items);
        procs[1] = new Consumer(consChannel, items);

        for (int i=0; i<buffers; ++i) {
            procs[i+2] = new Buffer(prodChannel[i], consChannel[i], bufferChannel[i]);
        }

        new Parallel(procs).run();
    }
}
