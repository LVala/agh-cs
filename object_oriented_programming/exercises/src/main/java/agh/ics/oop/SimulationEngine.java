package agh.ics.oop;

import agh.ics.oop.gui.App;
import javafx.application.Application;
import javafx.application.Platform;

public class SimulationEngine implements IEngine, Runnable{
    private MoveDirection[] directions;
    private final IWorldMap map;
    private final App app;

    public SimulationEngine(MoveDirection[] directions, IWorldMap map, Vector2d[] positions, Application app) {
        this.directions = directions;
        this.map = map;
        this.app = (App) app;
        placeAnimals(positions);
    }

    public void setDirections(MoveDirection[] directions) {
        this.directions = directions;
    }

    public SimulationEngine(IWorldMap map, Vector2d[] positions, Application app) {
        this.map = map;
        this.app = (App) app;
        placeAnimals(positions);
    }

    public void placeAnimals(Vector2d[] positions) {
        for (Vector2d position: positions) {
            map.place(new Animal(this.map, position));
        }
    }

    @Override
    public void run() {
        try {
            int moveDelay = 500;
            Thread.sleep(moveDelay);
        } catch (InterruptedException e) {
            System.out.println("Thread.sleep error: " + e);
        }
        Animal[] animals = this.map.getAnimals().values().toArray(new Animal[0]);
        int len = animals.length;
        int i = 0;

        for (MoveDirection direction : this.directions) {
            animals[i % len].move(direction);
            i++;
            System.out.println(this.map);
            Platform.runLater(() -> {
                app.positionChanged(new Animal(), new Vector2d(1, 1), new Vector2d(1, 1));
            });
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println("Thread.sleep error: " + e);
            }
        }
    }
}
