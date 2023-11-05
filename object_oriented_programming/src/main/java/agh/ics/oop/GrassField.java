package agh.ics.oop;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import java.lang.Math;

public class GrassField extends AbstractWorldMap {
    private final int grass_quantity;
    protected final Map<Vector2d, Grass> grasses = new LinkedHashMap<>();
    protected final MapBoundary map_boundary = new MapBoundary();

    public GrassField(int grass_quantity) {
        this.grass_quantity = grass_quantity;
        fill_with_grass();
    }

    private void fill_with_grass() {
        while (this.grasses.size() < this.grass_quantity) {
            int new_x = ThreadLocalRandom.current().nextInt(0,  (int) Math.sqrt(this.grass_quantity*10));
            int new_y = ThreadLocalRandom.current().nextInt(0,  (int) Math.sqrt(this.grass_quantity*10));
            Vector2d new_position = new Vector2d(new_x, new_y);

            if (this.grasses.get(new_position) == null) {
                Grass new_grass = new Grass(new_position);
                this.grasses.put(new_position, new_grass);
                map_boundary.addObject(new_grass);
            }
        }
    }

    @Override
    public boolean place(Animal animal) {
        super.place(animal);
        map_boundary.addObject(animal);
        return true;
    }

    @Override
    public boolean canMoveTo(Vector2d position) {
        if (this.isOccupied(position)) {
            return (objectAt(position) instanceof Grass);
        }
        return true;
    }

    @Override
    public boolean isOccupied(Vector2d position) {
        if (super.isOccupied(position)) return true;
        return this.grasses.get(position) != null;
    }

    @Override
    public IMapObject objectAt(Vector2d position) {
        if (super.objectAt(position) != null ) return super.objectAt(position);
        return this.grasses.get(position);
    }

    @Override
    public void positionChanged(IMapObject map_object, Vector2d oldPosition, Vector2d newPosition) {
        super.positionChanged(map_object, oldPosition, newPosition);
        map_boundary.positionChanged(map_object, oldPosition, newPosition);
    }

    @Override
    public Vector2d[] getEdges() {
        return map_boundary.getEdges();
    }
}
