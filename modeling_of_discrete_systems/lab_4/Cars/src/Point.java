public class Point {

    public static Integer[] types = {0, 1, 2, 3, 5};
    public int type = 0;
    public int speed;
    public Point next;
    public Point prev;
    public Point left;
    public Point right;
    public boolean moved = false;
    

    public void move() {
        Point curPrev = this;
        Point otherNext = left == null ? this.right : this.left;
        Point otherPrev = otherNext;
        int d_prev = 0;
        int d_other_prev = 0;
        int d_other_next = 0;

        // ochydny ten kod, ale bywa i tak
        if (type != 0 && type != 5 && moved == false) {
            //  calculation free space
            for (int i = 0; i <= 8; ++i) {
                if (curPrev.prev.type != 0 || i == 8) {
                    d_prev = i;
                    break;
                }
                curPrev = curPrev.prev;
            }
            for (int i = 0; i <= 8; ++i) {
                if (otherNext.next.type != 0 || i == 8) {
                    d_other_next = i;
                    break;
                }
                otherNext = otherNext.next;
            }
            for (int i = 0; i <= 8; ++i) {
                if (otherPrev.prev.type != 0 || i == 8) {
                    d_other_prev = i;
                    break;
                }
                otherPrev = otherPrev.prev;
            }

            if (this.right != null && this.right.type == 0) {
                if (d_prev >= 7 && d_other_prev >= 7 && d_other_next >= speed) {
                    Point newPoint = right;
                    for (int i=0; i<speed-1; ++i)
                        newPoint = newPoint.next;
                    newPoint.type = type;
                    newPoint.speed = speed;
                    this.moved = true;
                    newPoint.moved = true;
                    this.type = 0;
                    return;
                }
            }
            if (this.left != null && this.left.type == 0) {  // manewr wyprzedzania
                if (speed < this.getMaxSpeed() && d_prev >= 7 && d_other_prev >= 7 && d_other_next >= speed) {
                    Point newPoint = left;
                    for (int i=0; i<speed-1; ++i)
                        newPoint = newPoint.next;
                    newPoint.type = type;
                    newPoint.speed = speed+1;
                    this.moved = true;
                    newPoint.moved = true;
                    this.type = 0;
                    return;
                }
            }
            // acceleration
            speed = (speed < this.getMaxSpeed()) ? speed+1 : speed;
            Point newPoint = this;
            for (int i = 0; i <= speed; ++i) {
                if (newPoint.next.type != 0 || i == speed) {
                    speed = i;
                    break;
                }
                newPoint = newPoint.next;
            }
        
            // actual moving
            newPoint.type = type;
            type = 0;
            newPoint.speed = speed;
            moved = true;
            newPoint.moved = true;
        }
    }

    public int getMaxSpeed() {
        if (type != 0 && type != 5)
            return type*2 + 1;
        else return 0;
    }

    public void clicked() {
        type = 1;
    }

    public void clear() {
        type = 0;
    }
}