package gui;

import evogen.*;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.StackPane;

import java.util.List;

public class MapGrid {
    public final GridPane mapGrid = new GridPane();

    private final AbstractWorldMap map;
    private final MapElement mapElement;

    public MapGrid(AbstractWorldMap map, AnimalInfoGrid animalInfoGrid) {
        this.mapGrid.setAlignment(Pos.TOP_CENTER);
        this.mapGrid.setPadding(new Insets(25, 25, 10, 10));

        int gridElemHeight = 300 / map.height;
        int gridElemWidth = 300 / map.width;

        this.map = map;
        this.mapElement = new MapElement(gridElemWidth, gridElemHeight, this.map.startEnergy, animalInfoGrid);
    }

    // UPDATE METHODS

    // map is de facto drawn upside-down, but IMO it does not make a difference
    // when it comes to visualization and simplifies the code a lot
    public void updateMapGrid() {
        for (int i = 0; i < this.map.height; i++) {
            for (int j = 0; j < this.map.width; j++) {
                Vector2d position = new Vector2d(j, i);
                StackPane stack;
                int finalI = i;
                int finalJ = j;
                this.mapGrid.getChildren().removeIf(node -> GridPane.getRowIndex(node) == finalI && GridPane.getColumnIndex(node) == finalJ);

                if (this.map.isOccupiedByAnimal(position, 1)) {
                    Animal animal = this.map.getStrongestAnimalAt(position);
                    stack = mapElement.getImage(animal, this.map.isInJungle(position));
                }
                else if (this.map.isOccupiedByPlant(position)) {
                    Plant plant = this.map.getPlantAt(position);
                    stack = mapElement.getImage(plant, this.map.isInJungle(position));
                }
                else {
                    stack = mapElement.getImage(null, this.map.isInJungle(position));
                }
                this.mapGrid.add(stack, j, i);
            }
        }
    }

    // highlights only, when the animal is the strongest one on the field
    // because otherwise it's theoretically not visible, covered by stronger one
    public void highlightMostCommonGenotype(List<Genotype> mostCommonGenotypes) {
        for (int i = 0; i < this.map.height; i++) {
            for (int j = 0; j < this.map.width; j++) {
                Vector2d position = new Vector2d(j, i);
                int finalI = i;
                int finalJ = j;
                if (this.map.isOccupiedByAnimal(position, 1)) {
                    Animal animal = this.map.getStrongestAnimalAt(position);
                    if (mostCommonGenotypes.contains(animal.getGenotype())) {
                        this.mapGrid.getChildren().removeIf(node -> GridPane.getRowIndex(node) == finalI && GridPane.getColumnIndex(node) == finalJ);
                        StackPane stack = mapElement.getHighlightedAnimal(animal, this.map.isInJungle(position));
                        this.mapGrid.add(stack, j, i);
                    }
                }
            }
        }
    }
}
