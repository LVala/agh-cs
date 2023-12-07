import java.util.Random;

public class Point {

    public int type = 0;
    public int speed = 0;
    public Point next;
    public boolean moved = false;
    public int p = 50;  // % 0-100
    

    public void move() {
        if (type == 1 && moved == false) {
            // acceleration
            speed = (speed < 5) ? ++speed : speed;

            // element of randomness
            Random ran = new Random();
            int x = ran.nextInt(100);
            speed = (x < p && speed > 0) ? --speed : speed;

            // slowing down
            Point curNext = this;
            for (int i = 0; i <= speed; ++i) {
                if (curNext.next.type == 1 || i == speed) {
                    speed = i;
                    break;
                }
                curNext = curNext.next;
            }

            // actual moving
            type = 0;
            curNext.type = 1;
            curNext.speed = speed;
            moved = true;
            curNext.moved = true;
        }
    }

    public void clicked() {
        type = 1;
    }

    public void clear() {
        type = 0;
    }
}