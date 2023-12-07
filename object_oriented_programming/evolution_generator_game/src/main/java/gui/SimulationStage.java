package gui;

import evogen.SimulationEngine;
import javafx.scene.Scene;
import javafx.scene.layout.*;
import javafx.stage.Stage;

public class SimulationStage {
    private final SimulationEngine foldedEngine;
    private final SimulationEngine boundedEngine;

    private SimulationBox foldedSimulationBox;
    private SimulationBox boundedSimulationBox;

    private Stage mainStage;

    public SimulationStage(SimulationEngine foldedEngine, SimulationEngine boundedEngine) {
        this.foldedEngine = foldedEngine;
        this.boundedEngine = boundedEngine;
    }

    public Stage getStage() {
        return this.mainStage;
    }

    public void showMainStage() {
        // main simulation window containing two simulation "boxes"
        this.mainStage = new Stage();
        this.mainStage.setTitle("Evolution Generator");

        this.foldedSimulationBox = new SimulationBox(this.foldedEngine, this);
        this.boundedSimulationBox = new SimulationBox(this.boundedEngine, this);

        this.foldedEngine.setSimulationGuiBox(foldedSimulationBox);
        this.boundedEngine.setSimulationGuiBox(boundedSimulationBox);

        HBox mainHBox = new HBox(10);
        mainHBox.getChildren().addAll(this.foldedSimulationBox.simulationBox, this.boundedSimulationBox.simulationBox);

        Scene scene = new Scene(mainHBox, 1500, 800);
        this.mainStage.setScene(scene);
        this.mainStage.show();

        // make simulation threads shutdown when closing the window
        mainStage.setOnCloseRequest(event -> {
            foldedSimulationBox.getExecutor().shutdown();
            boundedSimulationBox.getExecutor().shutdown();
        });
    }

    // used in handing exceptions in ScheduledExecutorService threads
    public void terminateExecution() {
        this.foldedSimulationBox.getExecutor().shutdown();
        this.boundedSimulationBox.getExecutor().shutdown();
        this.mainStage.close();
    }
}