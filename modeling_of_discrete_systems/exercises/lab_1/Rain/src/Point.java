import java.util.ArrayList;
import java.util.Random;

public class Point {
	private ArrayList<Point> neighbors;
	private int currentState;
	private int nextState;
	private int numStates = 7;  // if the max state is 6, then I belive this should be 7 instead of the default 6
	
	public Point() {
		currentState = 0;
		nextState = 0;
		neighbors = new ArrayList<Point>();
	}

	public void clicked() {
		currentState=(++currentState)%numStates;	
	}
	
	public int getState() {
		return currentState;
	}

	public void setState(int s) {
		currentState = s;
	}

	// method caculating point's new state
	public void calculateNewState() {
		if (this.currentState > 0)
			this.nextState = this.currentState - 1;
		else
			if (this.countNeighbor() > 0)
				this.nextState = 6;
			else
				this.nextState = 0;
	}

	public void changeState() {
		currentState = nextState;
	}
	
	public void addNeighbor(Point nei) {
		neighbors.add(nei);
	}
	
	// method counting all active neighbors of THIS point
	public int countNeighbor() {
		int count = 0;
		for (Point point : this.neighbors)
			count += point.getState();
		return count;
	}

	public void drop() {
		Random rand = new Random();

		if (rand.nextInt(100) < 3)
			this.currentState = 6;
	}
}
