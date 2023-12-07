package gui;

import evogen.Animal;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class AnimalInfoGrid {
    public static final String fontName = "Tahoma";
    public static final int fontSize = 16;

    public final GridPane animalInfoGrid = new GridPane();
    private Animal animal;

    public AnimalInfoGrid() {
        this.animalInfoGrid.setAlignment(Pos.TOP_CENTER);
        this.animalInfoGrid.setHgap(20);
        this.animalInfoGrid.setVgap(20);
        this.animalInfoGrid.setPadding(new Insets(10, 25, 25, 10));

        Label mainLabel = new Label("Animal Info");
        mainLabel.setFont(Font.font(fontName, FontWeight.NORMAL, 20));
        this.animalInfoGrid.add(mainLabel, 0, 0, 2, 1);
        GridPane.setHalignment(mainLabel, HPos.CENTER);

        Label childrenLabel = new Label("Number of children:");
        childrenLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(childrenLabel, 0, 1);

        Label descendantsLabel = new Label("Number of descendants:");
        descendantsLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(descendantsLabel, 0, 2);

        Label deathEraLabel = new Label("Era of animal death:");
        deathEraLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(deathEraLabel, 0, 3);

        Label genotypeLabel = new Label("Genotype:");
        genotypeLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(genotypeLabel, 0, 4, 2, 1);
    }

    // GETTERS AND SETTERS

    public Animal getAnimal() {
        return this.animal;
    }

    public void setAnimal(Animal animal) {
        this.animal = animal;
    }

    // UPDATE METHOD

    public void updateAnimalInfo() {
        this.animalInfoGrid.getChildren().removeIf(node -> GridPane.getColumnIndex(node) == 1);
        this.animalInfoGrid.getChildren().removeIf(node -> GridPane.getRowIndex(node) == 5);

        Label childrenValue = new Label(Integer.toString(animal.getTrackedChildrenNumber()));
        childrenValue.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(childrenValue, 1,1);

        Label descendantsValue = new Label(Integer.toString(animal.getTrackedDescendantsNumber()));
        descendantsValue.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(descendantsValue, 1,2);

        Label deathEraValue;
        if (animal.getDeathEra() == -1) deathEraValue = new Label("N/A");
        else deathEraValue = new Label(Integer.toString(animal.getDeathEra()));

        deathEraValue.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(deathEraValue, 1,3);

        Label genotypeValue = new Label(animal.getGenotype().toString());
        genotypeValue.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        this.animalInfoGrid.add(genotypeValue, 0,5, 2, 1);
    }
}
