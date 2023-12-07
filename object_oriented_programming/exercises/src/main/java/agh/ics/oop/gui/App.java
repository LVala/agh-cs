package agh.ics.oop.gui;

import agh.ics.oop.*;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.HPos;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.*;
import javafx.stage.Stage;

import java.util.List;
import java.util.Map;

public class App extends Application implements IPositionChangeObserver {
    private IWorldMap map;
    private Thread engineThread;
    private MoveDirection[] directions;
    private GridPane grid = new GridPane();
    private SimulationEngine engine;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void init() {
        List<String> args = getParameters().getRaw();
        this.directions = new OptionsParser().parse(args.toArray(new String[0]));
        this.map = new GrassField(10);
        Vector2d[] positions = {new Vector2d(2, 2), new Vector2d(2, 3), new Vector2d(5, 7)};
        this.engine = new SimulationEngine(directions, map, positions, this);
        this.engineThread = new Thread(engine::run);
    }

    public void createGrid() {
        Vector2d[] edges = this.map.getEdges();
        int left = edges[0].x;
        int down = edges[0].y;
        int right = edges[1].x;
        int up = edges[1].y;

        Label label = new Label("y\\x");
        grid.add(label, 0,0,1,1);
        grid.getColumnConstraints().add(new ColumnConstraints(40));
        grid.getRowConstraints().add(new RowConstraints(40));
        GridPane.setHalignment(label, HPos.CENTER);

        for (int i=1; i<= right-left+1; i++) {
            grid.getColumnConstraints().add(new ColumnConstraints(40));

            label = new Label(String.format("%d", left+i-1));
            GridPane.setHalignment(label, HPos.CENTER);

            grid.add(label, i, 0,1,1);
        }

        for (int i=1; i<= up-down+1; i++) {
            grid.getRowConstraints().add(new RowConstraints(40));

            label = new Label(String.format("%d", up-i+1));
            GridPane.setHalignment(label, HPos.CENTER);

            grid.add(label, 0, i,1,1);
        }

        for (int i=1; i<= up-down+1; i++) {
            for (int j=1; j<= right-left+1; j++) {
                if (map.isOccupied(new Vector2d(left+j-1, up-i+1))) {
                    VBox newVbox = new GuiElementBox(map.objectAt(new Vector2d(left+j-1, up-i+1))).getVbox();
                    GridPane.setHalignment(newVbox, HPos.CENTER);
                    grid.add(newVbox, j, i,1,1);
                }
            }
        }
    }

    public void positionChanged(IMapObject map_object, Vector2d oldPosition, Vector2d newPosition) {
        grid.setGridLinesVisible(false);
        grid.getColumnConstraints().clear();
        grid.getRowConstraints().clear();
        grid.getChildren().clear();
        grid.setGridLinesVisible(true);
        createGrid();
    }

    public VBox createInterfaceVBox() {
        TextField text = new TextField();
        Button btn = new Button("Start");
        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(text, btn);
        vbox.setAlignment(Pos.CENTER);

        btn.setOnAction(new EventHandler<ActionEvent>() {
            @Override public void handle(ActionEvent e) {
                String[] txt = text.getText().split(" ");
                MoveDirection[] newDirections = new OptionsParser().parse(txt);
                engine.setDirections(newDirections);
                Thread newEngineThread = new Thread(engine::run);
                newEngineThread.start();
            }
        });
        return vbox;
    }

    public void start(Stage primaryStage) {
        this.grid.setGridLinesVisible(true);
        createGrid();
        HBox hbox = new HBox(15);
        hbox.getChildren().add(grid);
        VBox vboxInterface = createInterfaceVBox();
        hbox.getChildren().add(vboxInterface);

        hbox.setAlignment(Pos.CENTER);

        Scene scene = new Scene(hbox, 600, 600);
        primaryStage.setScene(scene);
        primaryStage.show();
        engineThread.start();
    }
}