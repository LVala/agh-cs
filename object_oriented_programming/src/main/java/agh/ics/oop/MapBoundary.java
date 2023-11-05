package agh.ics.oop;

import java.util.SortedSet;
import java.util.TreeSet;

public class MapBoundary implements IPositionChangeObserver {
    private final SortedSet<IMapObject> x_objects = new TreeSet<IMapObject>(new MapObjectComparator("x"));
    private final SortedSet<IMapObject> y_objects = new TreeSet<IMapObject>(new MapObjectComparator("y"));

    public void addObject(IMapObject map_object) {
        this.x_objects.add(map_object);
        this.y_objects.add(map_object);
    }

    @Override
    public void positionChanged(IMapObject map_object, Vector2d oldPosition, Vector2d newPosition) {
        this.x_objects.remove(map_object);
        this.y_objects.remove(map_object);

        this.x_objects.add(map_object);
        this.y_objects.add(map_object);
    }

    public Vector2d[] getEdges() {
        Vector2d left = x_objects.first().getPosition();
        Vector2d right = x_objects.last().getPosition();
        Vector2d down = y_objects.first().getPosition();
        Vector2d up = y_objects.last().getPosition();

        Vector2d upper_right = up.upperRight(right);
        Vector2d lower_left = down.lowerLeft(left);

        return new Vector2d[]{lower_left, upper_right};
    }
}