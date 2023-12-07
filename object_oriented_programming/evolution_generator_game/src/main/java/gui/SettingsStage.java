package gui;

import evogen.AbstractWorldMap;
import evogen.BoundedMap;
import evogen.FoldedMap;
import evogen.SimulationEngine;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class SettingsStage extends Application {

    public GridPane createInputGrid() {
        GridPane grid = new GridPane();
        grid.setAlignment(Pos.CENTER);
        grid.setHgap(20);
        grid.setVgap(20);
        grid.setPadding(new Insets(25, 25, 25, 25));

        String fontName = "Tahoma";
        int fontSize = 16;

        // SCENE TITLE

        Text sceneTitle = new Text("Welcome to the Evolution Generator!\nEnter simulation parameters:");
        sceneTitle.setFont(Font.font(fontName, FontWeight.NORMAL, 20));
        grid.add(sceneTitle, 0, 0, 2, 1);

        // INPUT FIELDS

        Label widthLabel = new Label("Map width [10-100]:");
        TextField widthTextField = new TextField("30");

        Label heightLabel = new Label("Map height [10-100]:");
        TextField heightTextField = new TextField("30");

        Label startEnergyLabel = new Label("Animal start energy [1-10^6]:");
        TextField startEnergyTextField = new TextField("1000");

        Label moveEnergyLabel = new Label("Animal move energy [1-10^6]:");
        TextField moveEnergyTextField = new TextField("10");

        Label plantEnergyLabel = new Label("Plant energy [1-10^6]:");
        TextField plantEnergyTextField = new TextField("200");

        Label jungleRatioLabel = new Label("Jungle-steppe ratio (double) (0-100]:");
        TextField jungleRatioTextField = new TextField("0.2");

        Label initialAnimalsLabel = new Label("Initial number of animals [10-area]:");
        TextField initialAnimalsTextField = new TextField("100");

        Label eraLengthLabel = new Label("Era real time length (ms) [100-10^4]:");
        TextField eraLengthTextField = new TextField("500");

        Label[] labels = {widthLabel, heightLabel, startEnergyLabel, moveEnergyLabel, plantEnergyLabel,
                jungleRatioLabel, initialAnimalsLabel, eraLengthLabel};
        TextField[] textFields = {widthTextField, heightTextField, startEnergyTextField, moveEnergyTextField,
                plantEnergyTextField, jungleRatioTextField, initialAnimalsTextField, eraLengthTextField};

        for (int i = 0; i < 8; i++) {
            labels[i].setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
            grid.add(labels[i], 0, i+1);
            grid.add(textFields[i], 1, i+1);
        }

        // CHECKBOXES

        Label isMagicLabel = new Label("If simulation uses \"magic\" rule:");
        isMagicLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        grid.add(isMagicLabel, 0, 9, 2, 1);
        GridPane.setHalignment(isMagicLabel, HPos.CENTER);

        Label foldedLabel = new Label("Folded map");
        isMagicLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));
        Label boundedLabel = new Label("Bounded map");
        isMagicLabel.setFont(Font.font(fontName, FontWeight.NORMAL, fontSize));

        CheckBox foldedCheckBox = new CheckBox();
        CheckBox boundedCheckBox = new CheckBox();

        HBox foldedHBox = new HBox(10);
        HBox boundedHBox = new HBox(10);

        foldedHBox.getChildren().addAll(foldedLabel, foldedCheckBox);
        boundedHBox.getChildren().addAll(boundedLabel, boundedCheckBox);

        grid.add(foldedHBox, 0, 10);
        grid.add(boundedHBox, 1, 10);

        // BUTTON

        Button btn = new Button("Start the simulation");
        btn.setFont(Font.font(fontName, FontWeight.NORMAL, 22));
        btn.setPrefSize(250,60);

        // BUTTON ON ACTION AND VALIDATION

        btn.setOnAction(event -> {
            if (checkIfValid(widthTextField, "[0-9]+", 10, 100)) return;
            int width = Integer.parseInt(widthTextField.getText());
            if (checkIfValid(heightTextField, "[0-9]+", 10, 100)) return;
            int height = Integer.parseInt(heightTextField.getText());
            if (checkIfValid(startEnergyTextField, "[0-9]+", 1, 1000000)) return;
            int startEnergy = Integer.parseInt(startEnergyTextField.getText());
            if (checkIfValid(moveEnergyTextField, "[0-9]+", 1, 1000000)) return;
            int moveEnergy = Integer.parseInt(moveEnergyTextField.getText());
            if (checkIfValid(plantEnergyTextField, "[0-9]+", 1, 1000000)) return;
            int plantEnergy = Integer.parseInt(plantEnergyTextField.getText());
            if (checkIfValid(initialAnimalsTextField, "[0-9]+", 10, width * height)) return;
            int initialAnimals = Integer.parseInt(initialAnimalsTextField.getText());
            if (checkIfValid(eraLengthTextField, "[0-9]+", 100, 10000)) return;
            int eraLength = Integer.parseInt(eraLengthTextField.getText());

            // custom validation for jungleRatio as it's double
            if (!jungleRatioTextField.getText().matches("([0-9]+\\.[0-9]+)|[0-9]+")){
                jungleRatioTextField.setStyle("-fx-text-box-border: #B22222; -fx-focus-color: #B22222;");
                jungleRatioTextField.setText("invalid input");
                return;
            }
            double jungleRatio = Double.parseDouble(jungleRatioTextField.getText());
            if (jungleRatio <= 0  || jungleRatio > 100) {
                jungleRatioTextField.setStyle("-fx-text-box-border: #B22222; -fx-focus-color: #B22222;");
                jungleRatioTextField.setText("invalid value");
                return;
            }
            else {
                jungleRatioTextField.setStyle(null);
            }

            boolean isMagicFolded = foldedCheckBox.isSelected();
            boolean isMagicBounded = boundedCheckBox.isSelected();

            AbstractWorldMap foldedMap = new FoldedMap(width, height, startEnergy, moveEnergy, plantEnergy, jungleRatio, initialAnimals);
            AbstractWorldMap boundedMap = new BoundedMap(width, height, startEnergy, moveEnergy, plantEnergy, jungleRatio, initialAnimals);

            SimulationEngine foldedEngine = new SimulationEngine(foldedMap, isMagicFolded, eraLength);
            SimulationEngine boundedEngine = new SimulationEngine(boundedMap, isMagicBounded, eraLength);

            SimulationStage simulationStage = new SimulationStage(foldedEngine, boundedEngine);

            simulationStage.showMainStage();
        });

        HBox hbBtn = new HBox(20);
        hbBtn.setAlignment(Pos.CENTER);
        hbBtn.getChildren().add(btn);
        grid.add(hbBtn, 0, 12, 2, 1);

        return grid;
    }

    public boolean checkIfValid(TextField textField, String regex, int minValue, int maxValue) {
        if (!textField.getText().matches(regex)){
            textField.setStyle("-fx-text-box-border: #B22222; -fx-focus-color: #B22222;");
            textField.setText("invalid input");
            return true;
        }
        int value =Integer.parseInt(textField.getText());
        if (value < minValue || value > maxValue) {
            textField.setStyle("-fx-text-box-border: #B22222; -fx-focus-color: #B22222;");
            textField.setText("invalid value");
            return true;
        }
        else {
            textField.setStyle(null);
            return false;
        }
    }

    // STARTUP METHODS

    public  void start(Stage primaryStage) {
        primaryStage.setTitle("Evolution Generator - Initial Settings");

        GridPane grid = createInputGrid();
        Scene scene = new Scene(grid, 500, 650);
        primaryStage.setScene(scene);

        // exception handling on GUI thread
        Thread.currentThread().setUncaughtExceptionHandler((thread, throwable) -> {
            System.out.println("Exception caught in GUI thread. GUI shut down\nException: "+throwable.getMessage());
            Platform.exit();
        });

        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
