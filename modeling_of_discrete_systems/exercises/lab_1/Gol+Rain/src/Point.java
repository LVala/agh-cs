interface Point {
    public void clicked();
    public int getState();
    public void setState(int s);
    public void calculateNewState();
    public void changeState();
    public void addNeighbor(Point nei);
    public int countNeighbor();
}