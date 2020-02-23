package repogenerator;

import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;

public class ApplicationMain extends Application {
	public static final int APP_WIDTH = 1000;
	public static final int APP_HEIGHT = 500;
	public static final double LEFTPANE_PCAGE = 0.6;
	public static final double BROWSE_TFIELD_PCAGE = 0.7;
	ObservableList<String> features = FXCollections.observableList(new ArrayList<String>());
	ListView<String> featuresListView; 
	File repoDirectory;
	TextField headerBox;
	TextArea bodyBox;
	@Override
	public void start(Stage stage) throws Exception {
		VBox root = new VBox();
		HBox topBox = new HBox();
		root.getChildren().add(topBox);
		TextField directoryField = new TextField();
		Label directoryFieldLabel = new Label();
		directoryFieldLabel.setText("Directory: ");
		directoryField.setPrefWidth(BROWSE_TFIELD_PCAGE * APP_WIDTH - directoryFieldLabel.getWidth());
		topBox.getChildren().add(directoryFieldLabel);
		topBox.getChildren().add(directoryField);
		Button directoryBrowseButton = new Button();
		directoryBrowseButton.setText("Browse");
		directoryBrowseButton.addEventHandler(ActionEvent.ANY, e -> {
			DirectoryChooser directoryChooser = new DirectoryChooser();
			directoryChooser.setTitle("Select your repository directory");
			repoDirectory = directoryChooser.showDialog(stage);
			directoryFieldLabel.setText(repoDirectory.getAbsolutePath());
			features.clear();
			try{
				String[] files = repoDirectory.list();

				for(String currentFile : files) {
					features.add(currentFile);
				}
				featuresListView.setItems(features);	
			}catch(Exception ex) {
			}
		});
		directoryBrowseButton.setPrefWidth(APP_WIDTH - BROWSE_TFIELD_PCAGE * APP_WIDTH - directoryFieldLabel.getWidth());
		topBox.getChildren().add(directoryBrowseButton);

		HBox mainBox = new HBox();
		root.getChildren().add(mainBox);
		VBox leftPane = new VBox();
		mainBox.getChildren().add(leftPane);
		VBox rightPane = new VBox();
		mainBox.getChildren().add(rightPane);

		Label featuresBoxLabel = new Label();
		featuresBoxLabel.setText("Features: ");
		leftPane.getChildren().add(featuresBoxLabel);
		ListView<String> featuresBox = new ListView<String>();
		featuresListView = featuresBox;
		featuresListView.getSelectionModel().selectedItemProperty().addListener(e -> {
			
			File currentFeature = new File(repoDirectory.getAbsolutePath() + "/" + featuresListView.getSelectionModel().getSelectedItem());
			try {
				Path currentHeader = Paths.get(currentFeature.getAbsolutePath() + "/header.txt"); 
				List<String> headerLines = Files.readAllLines(currentHeader);
				headerBox.setText(headerLines.get(0));
			}catch(Exception exception) {
				headerBox.setText("");
			}
			try {
				
				Path currentBody = Paths.get(currentFeature.getAbsolutePath() + "/body.txt");
				List<String> bodyLines = Files.readAllLines(currentBody);
				if(bodyLines.size() >= 1) {	
					String body = bodyLines.get(0);
					if(bodyLines.size() >1) {
						body+= "\n";
					}
					for(int i = 1; i<bodyLines.size(); i++) {
						body += bodyLines.get(i) + "\n";
					}
					bodyBox.setText(body);
				} else {
					bodyBox.setText("");
				}
			}catch(Exception exception) {
				bodyBox.setText("");
			}
		});
		featuresBox.setPrefWidth(LEFTPANE_PCAGE*APP_WIDTH);
		featuresBox.setPrefHeight(APP_HEIGHT - 2*directoryField.getPrefHeight());
		leftPane.getChildren().add(featuresBox);
		HBox newFeatureHBox = new HBox();
		leftPane.getChildren().add(newFeatureHBox);
		TextField newFeatureNameBox = new TextField();
		newFeatureHBox.getChildren().add(newFeatureNameBox);
		newFeatureNameBox.setPrefWidth(0.5*LEFTPANE_PCAGE*APP_WIDTH);
		Button addFeatureButton = new Button();
		addFeatureButton.setText("Add Feature");
		addFeatureButton.setPrefWidth(LEFTPANE_PCAGE * APP_WIDTH*0.5);
		addFeatureButton.addEventHandler(ActionEvent.ANY, e -> {
			File newFeatureDirectory = new File(repoDirectory.getAbsolutePath() + "/" + newFeatureNameBox.getText());
			newFeatureDirectory.mkdirs();
			newFeatureNameBox.setText("");
			try{
				new File(newFeatureDirectory.getAbsolutePath() + "/header.txt").createNewFile();
				new File(newFeatureDirectory.getAbsolutePath() + "/body.txt").createNewFile();
			}catch(Exception exception) {
			}
			
			features.clear();
			try{
				String[] files = repoDirectory.list();

				for(String currentFile : files) {
					features.add(currentFile);
				}
				featuresListView.setItems(features);	
			}catch(Exception ex) {
			}
		});
		newFeatureHBox.getChildren().add(addFeatureButton);

		headerBox = new TextField();
		headerBox.textProperty().addListener((obs, oldText, newText) -> {
			File headerFile = new File(repoDirectory.getAbsolutePath() + "/" + featuresListView.getSelectionModel().getSelectedItem() + "/header.txt");
			try {
				FileWriter writer = new FileWriter(headerFile, false);
				writer.write(headerBox.getText());
				writer.close();
			}catch(Exception exception) {
			}
		});
		rightPane.getChildren().add(headerBox);
		bodyBox = new TextArea();
		bodyBox.textProperty().addListener((obs,oldText,newText) -> {
			File bodyFile = new File(repoDirectory.getAbsolutePath() + "/" + featuresListView.getSelectionModel().getSelectedItem() + "/body.txt");
			try {
				FileWriter writer = new FileWriter(bodyFile, false);
				writer.write(bodyBox.getText());
				writer.close();
			}catch(Exception exception) {
			
			}
		});
		bodyBox.setPrefWidth(APP_WIDTH - LEFTPANE_PCAGE * APP_WIDTH);
		bodyBox.setPrefHeight(APP_HEIGHT - 4 * headerBox.getHeight());
		bodyBox.setWrapText(true);
		rightPane.getChildren().add(bodyBox);
		HBox imageBrowse = new HBox();
		rightPane.getChildren().add(imageBrowse);
		TextField imageField = new TextField();
		imageField.setPrefWidth(BROWSE_TFIELD_PCAGE * (APP_WIDTH - LEFTPANE_PCAGE * APP_WIDTH));
		imageBrowse.getChildren().add(imageField);
		Button imageBrowseButton = new Button();
		imageBrowseButton.setText("Browse");
		imageBrowseButton.setPrefWidth((APP_WIDTH - LEFTPANE_PCAGE * APP_WIDTH) - (BROWSE_TFIELD_PCAGE * (APP_WIDTH - LEFTPANE_PCAGE * APP_WIDTH)));
		imageBrowse.getChildren().add(imageBrowseButton);



		Scene scene = new Scene(root);
		stage.setScene(scene);
		stage.show();

	}

	public static void main(String[] args) {
		launch(args);

	}

}

