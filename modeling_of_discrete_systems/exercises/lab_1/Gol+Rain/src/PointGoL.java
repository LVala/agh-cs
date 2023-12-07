import java.util.ArrayList;

public class PointGoL implements Point{
	private ArrayList<Point> neighbors;
	private int currentState;
	private int nextState;
	private int numStates = 2;
	
	public PointGoL() {
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
	// using 23/3 rule
	public void calculateNewState() {
		if (this.currentState == 0) {
			if (this.countNeighbor() == 3)
				this.nextState = 1;
			else
				this.nextState = 0;
		} else {
			if (this.countNeighbor() >= 2 && this.countNeighbor() <= 3)
				this.nextState = 1;
			else
				this.nextState = 0;
		}
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
}
