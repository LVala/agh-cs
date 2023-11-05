package agh.ics.oop;

public class Grass implements IMapObject {
    private final Vector2d position;

    public Grass(Vector2d position) {
        this.position = position;
    }

    public Vector2d getPosition() {
        return position;
    }

    public String getImageFilePath() {
        return "src/main/resources/grass.png";
    }

    public String toString() {
        return "*";
    }
}
