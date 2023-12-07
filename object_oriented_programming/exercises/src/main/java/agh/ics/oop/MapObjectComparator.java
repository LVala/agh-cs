package agh.ics.oop;

import java.util.Comparator;

public class MapObjectComparator implements Comparator<IMapObject> {
    private final String axis;

    public MapObjectComparator(String axis) {
        this.axis = axis;
    }

    @Override
    public int compare(IMapObject first, IMapObject second) {
        if (axis.equals("x")) {
            if (first.getPosition().x == second.getPosition().x) {
                return Integer.compare(first.getPosition().y, second.getPosition().y);
            } else {
                return Integer.compare(first.getPosition().x, second.getPosition().x);
            }
        } else {
            if (first.getPosition().y == second.getPosition().y) {
                return Integer.compare(first.getPosition().x, second.getPosition().x);
            } else {
                return Integer.compare(first.getPosition().y, second.getPosition().y);
            }
        }
    }
}
