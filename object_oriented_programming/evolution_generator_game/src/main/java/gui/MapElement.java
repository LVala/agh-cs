package gui;

import evogen.Animal;
import evogen.IMapObject;
import evogen.Plant;
import javafx.geometry.Pos;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.scene.control.Label;

public class MapElement {
    private final int width;
    private final int height;
    private final int maxEnergy;

    private final AnimalInfoGrid animalInfoGrid;

    public MapElement(int width, int height, int maxEnergy, AnimalInfoGrid animalInfoGrid) {
        this.width = width;
        this.height  = height;
        this.maxEnergy = maxEnergy;

        this.animalInfoGrid = animalInfoGrid;
    }

    public StackPane getImage(IMapObject object, boolean isJungle) {
        StackPane stack = new StackPane();
        stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));

        Rectangle rec = new Rectangle();
        rec.setHeight(this.height);
        rec.setWidth(this.width);


        if (object instanceof Plant) {
            rec.setFill(Color.web("0x306e26"));
            stack.getChildren().add(rec);
            return stack;
        }

        if (isJungle) rec.setFill(Color.web("0x88a464"));
        else rec.setFill(Color.web("0xd8bca4"));
        stack.getChildren().add(rec);

        if (object == null) return stack;

        Animal animal = (Animal) object;
        double energyRatio = (double) animal.getEnergy()/maxEnergy;
        String color;

        if (energyRatio < 0.2) color = "0xffe6e6";
        else if (energyRatio < 0.4) color = "0xf57878";
        else if (energyRatio < 0.6) color = "0xff4242";
        else if (energyRatio < 0.8) color = "0xb50000";
        else color = "0x570000";

        Circle circle = new Circle();
        circle.setRadius(Math.min(height, width) * 0.3);
        circle.setFill(Color.web(color));
        circle.setStroke(Color.web(color));
        stack.getChildren().add(circle);

        // to display animal info once clicked
        stack.setOnMouseClicked(event -> {
            if (animalInfoGrid.getAnimal() != null) animalInfoGrid.getAnimal().setIfTracked(false);
            animal.setIfTracked(true);
            animalInfoGrid.setAnimal(animal);
            animalInfoGrid.updateAnimalInfo();
        });

        return stack;
    }

    public StackPane getHighlightedAnimal(Animal animal, boolean isJungle) {
        // used for animals with most common genotypes
        StackPane stack = new StackPane();
        stack.setBorder(new Border(new BorderStroke(Color.web("0x000000"),
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, new BorderWidths(0.4))));

        Rectangle rec = new Rectangle();
        rec.setHeight(this.height);
        rec.setWidth(this.width);

        if (isJungle) rec.setFill(Color.web("0x88a464"));
        else rec.setFill(Color.web("0xd8bca4"));
        stack.getChildren().add(rec);

        Circle circle = new Circle();
        circle.setRadius(Math.min(height, width) * 0.3);
        circle.setFill(Color.web("0x03fce8"));
        circle.setStroke(Color.web("0x03fce8"));
        stack.getChildren().add(circle);

        stack.setOnMouseClicked(event -> {
            // tracking starts from the moment animal is being clicked
            // so information about its children from before is not shown
            if (animalInfoGrid.getAnimal() != null) animalInfoGrid.getAnimal().setIfTracked(false);
            animal.setIfTracked(true);
            animalInfoGrid.setAnimal(animal);
            animalInfoGrid.updateAnimalInfo();
        });

        return stack;
    }

    // static method
    public static GridPane createMapLegend() {
        GridPane legendGrid = new GridPane();
        legendGrid.setHgap(10);
        legendGrid.setAlignment(Pos.CENTER);

        Rectangle plantRec = new Rectangle();
        plantRec.setHeight(10);
        plantRec.setWidth(12);
        plantRec.setFill(Color.web("0x306e26"));
        Label plantLabel = new Label("-  plant");
        legendGrid.add(plantRec, 0, 0);
        legendGrid.add(plantLabel, 1, 0);

        Rectangle jungleRec = new Rectangle();
        jungleRec.setHeight(10);
        jungleRec.setWidth(10);
        jungleRec.setFill(Color.web("0x88a464"));
        Label jungleLabel = new Label("-  jungle");
        legendGrid.add(jungleRec, 2, 0);
        legendGrid.add(jungleLabel, 3, 0);

        Rectangle steppeRec = new Rectangle();
        steppeRec.setHeight(10);
        steppeRec.setWidth(10);
        steppeRec.setFill(Color.web("0xd8bca4"));
        Label steppeLabel = new Label("-  steppe");
        legendGrid.add(steppeRec, 4, 0);
        legendGrid.add(steppeLabel, 5, 0);

        Circle animalCircle = new Circle();
        animalCircle.setRadius(5);
        animalCircle.setFill(Color.web("0xE6050A"));
        animalCircle.setStroke(Color.web("0xE6050A"));
        Label animalLabel = new Label("-  animal (darker = more energy)");
        legendGrid.add(animalCircle, 0, 1);
        legendGrid.add(animalLabel, 1, 1, 5, 1);

        return legendGrid;
    }
}
