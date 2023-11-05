package agh.ics.oop;

public class RectangularMap extends AbstractWorldMap{
    private final int width;
    private final int height;

    public RectangularMap(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public boolean canMoveTo(Vector2d position) {
        if (this.isOccupied(position)) return false;
        return position.precedes(new Vector2d(width-1, height-1)) && position.follows(new Vector2d(0, 0));
    }

    @Override
    public Vector2d[] getEdges() {
        return new Vector2d[]{new Vector2d(0, 0), new Vector2d(width-1, height-1)};
    }
}
