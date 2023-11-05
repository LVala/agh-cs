package distributed.zookeeper;

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;

public class MainWindow extends Application {
    private Label descendantsCountLabel;
    private Label descendantsTreeLabel;
    private Executor executor;

    public MainWindow(Executor executor) {
        this.executor = executor;
    }

    public void updateDescendantsCountLabel(int count) {
        if (count == -1) {
            this.descendantsCountLabel.setText("Descendants count: znode 'z' does not exist");
        } else {
            this.descendantsCountLabel.setText("Descendants count: " + count);
        }
    }

    @Override
    public void start(Stage stage) {
        this.descendantsCountLabel = new Label("Descendants count: ");
        this.descendantsTreeLabel = new Label("");

        Button button = new Button("Refresh descendants tree");
        button.setOnAction(e -> {
          // is this even thread safe?
          this.descendantsTreeLabel.setText(this.executor.getDescendantsTreeString());  
        });

        VBox root = new VBox();
        root.getChildren().add(this.descendantsCountLabel);
        root.getChildren().add(button);
        root.getChildren().add(this.descendantsTreeLabel);
        Scene scene = new Scene(root, 640, 480);
        stage.setScene(scene);
        stage.show();
    }
}
