package agh.ics.oop;

public enum MapDirection {
    NORTH,
    SOUTH,
    WEST,
    EAST;

    public String toString() {
        String message = switch(this) {
            case EAST -> "Wschód";
            case WEST -> "Zachód";
            case NORTH -> "Północ";
            case SOUTH -> "Południe";
            default -> "Invalid";
        };
        return message;
    }

    public MapDirection next() {
        MapDirection new_direction = switch(this) {
            case EAST -> SOUTH;
            case SOUTH -> WEST;
            case WEST -> NORTH;
            case NORTH -> EAST;
        };
        return new_direction;
    }

    public MapDirection previous() {
        MapDirection new_direction = switch(this) {
            case EAST -> NORTH;
            case SOUTH -> EAST;
            case WEST -> SOUTH;
            case NORTH -> WEST;
        };
        return new_direction;
    }

    public Vector2d toUnitVector() {
        Vector2d vector = switch(this) {
            case EAST -> new Vector2d(1, 0);
            case SOUTH -> new Vector2d(0, -1);
            case WEST -> new Vector2d(-1, 0);
            case NORTH -> new Vector2d(0, 1);
        };
        return vector;
    }
}
