package agh.ics.oop;

import java.util.ArrayList;
import java.util.List;

public class Animal implements IMapObject {
    private MapDirection orientation;
    private Vector2d position;
    private IWorldMap map;
    private final List<IPositionChangeObserver> observers = new ArrayList<>();

    public Animal() {
        this.orientation = MapDirection.NORTH;
        this.position = new Vector2d(2, 2);
    }

    public Animal(IWorldMap map, Vector2d initialPosition) {
        this.orientation = MapDirection.NORTH;
        this.position = initialPosition;
        this.map = map;
        this.addObserver((IPositionChangeObserver) map);
    }

    public String getImageFilePath() {
        return switch(this.getOrientation()) {
            case NORTH -> "src/main/resources/up.png";
            case EAST -> "src/main/resources/right.png";
            case SOUTH -> "src/main/resources/down.png";
            case WEST -> "src/main/resources/left.png";
        };
    }

    public MapDirection getOrientation() {
        return this.orientation;
    }

    public Vector2d getPosition() {
        return this.position;
    }

    public String toString() {
        return this.orientation.name().substring(0, 1);
    }

    public boolean isAt(Vector2d position) {
        return this.position.equals(position);
    }

    void addObserver(IPositionChangeObserver observer) {
        this.observers.add(observer);
    }

    void removeObserver(IPositionChangeObserver observer) {
        this.observers.remove(observer);
    }

    void positionChanged(Vector2d oldPosition, Vector2d newPosition) {
        for (IPositionChangeObserver observer : this.observers) {
            observer.positionChanged(this, oldPosition, newPosition);
        }
    }

    public void move(MoveDirection direction) {
        Vector2d cur_vec = switch (this.orientation) {
            case NORTH -> new Vector2d(0, 1);
            case EAST -> new Vector2d(1, 0);
            case SOUTH -> new Vector2d(0, -1);
            case WEST -> new Vector2d(-1, 0);
        };

        Vector2d old_position = this.position;

        switch (direction) {
            case RIGHT -> this.orientation = this.orientation.next();
            case LEFT -> this.orientation = this.orientation.previous();
            case FORWARD -> {
                if (!this.map.canMoveTo(this.position.add(cur_vec))) break;
                this.position = this.position.add(cur_vec);
            }
            case BACKWARD -> {
                if (!this.map.canMoveTo(this.position.subtract(cur_vec))) break;
                this.position = this.position.subtract(cur_vec);
            }
        }

        Vector2d new_position = this.position;
        positionChanged(old_position, new_position);
    }
}
