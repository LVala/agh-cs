package agh.ics.oop;

import javafx.application.Platform;

import java.util.LinkedHashMap;
import java.util.Map;

abstract public class AbstractWorldMap implements IWorldMap, IPositionChangeObserver {
    protected final Map<Vector2d, Animal> animals = new LinkedHashMap<>();

    public abstract Vector2d[] getEdges();

    public abstract boolean canMoveTo(Vector2d position);

    @Override
    public void positionChanged(IMapObject map_object, Vector2d oldPosition, Vector2d newPosition) {
        this.animals.remove(oldPosition);
        this.animals.put(newPosition, (Animal) map_object);
    }

    public boolean isOccupied(Vector2d position) {
        return animals.get(position) != null;
    }

    public IMapObject objectAt(Vector2d position) {
        return animals.get(position);
    }

    @Override
    public Map<Vector2d, Animal> getAnimals() {
        return this.animals;
    }

    @Override
    public boolean place(Animal animal) {
        if (!this.canMoveTo(animal.getPosition())) throw new IllegalArgumentException("It is not legal to place animal on " + animal.getPosition());
        this.animals.put(animal.getPosition(), animal);
        return true;
    }

    public String toString() {
        Vector2d[] edges = getEdges();
        MapVisualizer map_visualizer = new MapVisualizer(this);
        return map_visualizer.draw(edges[0], edges[1]);
    }
}
