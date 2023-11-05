import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import javax.swing.JFrame;

class MandelbrotCallable implements Callable<Integer> {
    private BufferedImage image;
    private int maxIter;
    private double zoom;
    private int y;
    private int maxWidth;

    private double zx, zy, cX, cY, tmp;

    public MandelbrotCallable(BufferedImage image, int maxIter, double zoom, int maxWidth, int y) {
        this.image = image;
        this.maxIter = maxIter;
        this.zoom = zoom;
        this.maxWidth = maxWidth;
        this.y = y;
    }

    public Integer call() {
            for (int x = 0; x < maxWidth; x++) {
                zx = zy = 0;
                cX = (x - 400) / zoom;
                cY = (y - 300) / zoom;
                int iter = maxIter;
                while (zx * zx + zy * zy < 4 && iter > 0) {
                    tmp = zx * zx - zy * zy + cX;
                    zy = 2.0 * zx * zy + cY;
                    zx = tmp;
                    iter--;
                }
                image.setRGB(x, y, iter | (iter << 8));
            }

        return 0;
    }
} 

class MainExecutor extends JFrame {
    private BufferedImage image;
    
    private final int MAX_ITER = 10000;
    private final double ZOOM = 150;

    public MainExecutor() {
        super("Mandelbrot Set with Executor");
        setBounds(100, 100, 800, 600);
        setResizable(false);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        image = new BufferedImage(getWidth(), getHeight(), BufferedImage.TYPE_INT_RGB);

        ExecutorService executor = Executors.newWorkStealingPool(6);
        List<Future<Integer>> futures = new ArrayList<>();

        long start = System.currentTimeMillis();

        for (int y=0; y<getHeight(); ++y) {
            MandelbrotCallable callable = new MandelbrotCallable(image, MAX_ITER, ZOOM, getWidth(), y);
            Future<Integer> future = executor.submit(callable);
            futures.add(future);
        }

        for(Future<Integer> future : futures) {
            try {
                future.get();
            } catch (ExecutionException | InterruptedException e) {
                System.exit(1);
            }
        }

        long end = System.currentTimeMillis();
        System.out.println(end-start);
    }   

    @Override
    public void paint(Graphics g) {
        g.drawImage(image, 0, 0, this);
    }

    public static void main(String[] args) {
        new MainExecutor().setVisible(true);
    }
}
