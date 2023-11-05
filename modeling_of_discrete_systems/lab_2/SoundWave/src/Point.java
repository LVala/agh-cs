public class Point {

    public static Integer[] types = {0,1,2};
    public int type;

    public int sinInput;

	public Point nNeighbor;
	public Point wNeighbor;
	public Point eNeighbor;
	public Point sNeighbor;
	public float nVel;
	public float eVel;
	public float wVel;
	public float sVel;
	public float pressure;

	public Point() {
        sinInput = 0;
        type = types[0];
		clear();
	}

	public void clicked() {
		pressure = 1;
	}
	
	public void clear() {
		nVel = 0;
        eVel = 0;
        wVel = 0;
        sVel = 0;
        pressure = 0;
        type = types[0];  // to be able to clear walls and sound sources
	}

	public void updateVelocity() {
        if (type == types[0]) {
            nVel = nVel - (nNeighbor.getPressure() - pressure);
            sVel = sVel - (sNeighbor.getPressure() - pressure);
            wVel = wVel - (wNeighbor.getPressure() - pressure);
            eVel = eVel - (eNeighbor.getPressure() - pressure);
        }
	}

	public void updatePresure() {
        if (type == types[0]) {
		    pressure = (float) (pressure - 0.5 * (nVel  + sVel + wVel + eVel));
        }
        else if (type == types[2]) {
            double radians = Math.toRadians(sinInput);
            pressure = (float) (Math.sin(radians));
        }
	}

	public float getPressure() {
		return pressure;
	}
}