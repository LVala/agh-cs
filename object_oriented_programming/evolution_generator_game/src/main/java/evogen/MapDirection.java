package evogen;

import java.util.Random;

public enum MapDirection {
    NORTH,
    NORTH_EAST,
    EAST,
    SOUTH_EAST,
    SOUTH,
    SOUTH_WEST,
    WEST,
    NORTH_WEST;

    // static method
    public static MapDirection getRandomDirection() {
        MapDirection[] directionList = MapDirection.values();
        int rnd = new Random().nextInt(directionList.length);
        return directionList[rnd];
    }

    public MapDirection next(int turns) {
        // returns MapDirection after turning "turns" times clockwise

        MapDirection[] directionList = MapDirection.values();

        for (int i = 0; i< directionList.length; i++) {
            if (directionList[i] == this) return directionList[(i+turns)%directionList.length];
        }
        // loop above will always return, but IntelliJ asks for this return
        return null;
    }

    public MapDirection opposite() {
        return this.next(4);
    }

    public Vector2d getDirectionVector() {
        return switch(this) {
            case NORTH -> new Vector2d(0, 1);
            case NORTH_EAST -> new Vector2d(1, 1);
            case EAST -> new Vector2d(1, 0);
            case SOUTH_EAST -> new Vector2d(1, -1);
            case SOUTH -> new Vector2d(0, -1);
            case SOUTH_WEST -> new Vector2d(-1, -1);
            case WEST -> new Vector2d(-1, 0);
            case NORTH_WEST -> new Vector2d(-1, 1);
        };
    }
}
