import java.util.ArrayList;
import java.util.Random;

public class Point {

	public ArrayList<Point> neighbors;
    public ArrayList<Point> diagneighbors;
	public static Integer []types ={0,1,2,3};
	public int type;
	public float staticField;
    public float annoyance;
	public boolean isPedestrian;
    public boolean blocked = false;
    public float toWall = 0;

	public Point() {
		type=0;
		staticField = 100000;
        annoyance = 0;
		neighbors= new ArrayList<Point>();
        diagneighbors = new ArrayList<Point>();
	}
	
	public void clear() {
		staticField = 100000;
	}

	public boolean calcStaticField() {
        float smallestNorm = 100000;
        float smallestDiag = 100000;
        if (this.type == 1) return false;
        for (Point point : neighbors)
            smallestNorm = Math.min(point.staticField, smallestNorm);
        
        for (Point point: diagneighbors)
            smallestDiag = Math.min(point.staticField, smallestDiag);

        float newVal = (float) Math.min(smallestNorm+1, smallestDiag+1.4);

        if (staticField > newVal) {
            staticField = newVal;
            return true;
        }

		return false;
	}

    public boolean calcWallRepulsion() {
        float toWallNorm = 0;
        float toWallDiag = 0;
        if (this.type == 2 || this.type == 1) return false;
        for (Point point : neighbors)
            toWallNorm = Math.max(point.toWall, toWallNorm);

        for (Point point : neighbors)
            toWallDiag = Math.max(point.toWall, toWallDiag);

        float newVal = (float) Math.max(toWallNorm-1, toWallDiag-1.4);
        if (newVal <= 0) return false;

        if (toWall < newVal) {
            toWall = newVal;
            return true;
        }
        return false;
    }
	
	public void move(){
        if (isPedestrian && !blocked && type != 1) { 
            Point smallest = neighbors.get(0);
            for (Point point : neighbors)
                if (!point.isPedestrian)
                    smallest = point.staticField <= smallest.staticField ? point : smallest;
            
            for (Point point : diagneighbors)
                if (!point.isPedestrian)
                    smallest = point.staticField <= smallest.staticField ? point : smallest;
            
            if (!smallest.isPedestrian && smallest.staticField <= this.staticField) {
                annoyance = 0;
                if (smallest.type != 2)
                    smallest.isPedestrian = true;
                smallest.blocked = true;
                this.isPedestrian = false;
            }
            else if (!smallest.isPedestrian) {
                Random rnd = new Random();
                int randval = rnd.nextInt(10);
                if (randval <= annoyance) {
                    smallest.isPedestrian = true;
                    smallest.annoyance = annoyance;
                    smallest.blocked = true;
                    this.isPedestrian = false;
                    this.annoyance = 0;
                }
                else {
                    ++annoyance;
                }
            }
        }
	}

	public void addNeighbor(Point nei, int where) {
        if (where == 1) {
            neighbors.add(nei);
        }
        else if (where == 2) {
            diagneighbors.add(nei);
        }
	}
}