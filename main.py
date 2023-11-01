
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import javax.swing.Timer;
import java.util.HashMap;
import java.util.Map;
import java.awt.geom.Point2D;
import java.util.Stack;

public class Main {
    public static void main(String[] args) {
        LSystemGenerator generator = new LSystemGenerator("alphabet", "axiom", new HashMap<>(), 4);

        // Get the turnAngle and segmentLength from generator
        double turnAngle = generator.getTurnAngle();
        double segmentLength = generator.getSegmentLength();

        // Pass them along when creating an AnimatedLSystem
        AnimatedLSystem animatedSystem = new AnimatedLSystem(generator.getGeneratedAxiom(), turnAngle, segmentLength);

        Threading threading = new Threading();
        new UI(generator, animatedSystem, threading).initializeUI();
    }
}
class LSystemGenerator {
    private String alphabet;
    private String axiom;
    private Map<Character, String> rules;
    private int iterations;
    private String generatedAxiom;
    private double turnAngle;  // New variable
    private double segmentLength;  // New variable

    public double getTurnAngle() {
        return turnAngle;
    }

    public double getSegmentLength() {
        return segmentLength;
    }
    public LSystemGenerator(String alphabet, String axiom, Map<Character, String> rules, int iterations) {
        this.alphabet = alphabet;
        this.axiom = axiom;
        this.rules = rules;
        this.iterations = iterations;
        this.generatedAxiom = axiom;
        // Initialize turnAngle and segmentLength with default values
        this.turnAngle = 90;
        this.segmentLength = 10.0;
    }

    public void updateGenerator(String newAxiom, Map<Character, String> newRules, int newIterations, double newTurnAngle, double newSegmentLength) {
        this.axiom = newAxiom;
        this.rules = newRules;
        this.iterations = newIterations;
        this.turnAngle = newTurnAngle;
        this.segmentLength = newSegmentLength;

        // Automatically derive the alphabet from the axiom and rules
        StringBuilder alphabetBuilder = new StringBuilder();
        for (char c : newAxiom.toCharArray()) {
            if (alphabetBuilder.indexOf(String.valueOf(c)) == -1) {
                alphabetBuilder.append(c);
            }
        }
        for (char c : newRules.keySet()) {
            if (alphabetBuilder.indexOf(String.valueOf(c)) == -1) {
                alphabetBuilder.append(c);
            }
        }
        for (String s : newRules.values()) {
            for (char c : s.toCharArray()) {
                if (alphabetBuilder.indexOf(String.valueOf(c)) == -1) {
                    alphabetBuilder.append(c);
                }
            }
        }
        this.alphabet = alphabetBuilder.toString();
    }



    public void generateAxiom() {
        generatedAxiom = axiom;  // Reset to initial axiom
        String tempAxiom;
        for (int i = 1; i < iterations; i++) {
            System.out.println("Generated Axiom: " + generatedAxiom);
            StringBuilder newAxiom = new StringBuilder();
            for (char ch : generatedAxiom.toCharArray()) {
                if (rules.containsKey(ch)) {
                    newAxiom.append(rules.get(ch));
                } else {
                    newAxiom.append(ch);
                }
            }
            tempAxiom = newAxiom.toString();
            generatedAxiom = tempAxiom;
        }
    }



    public String getGeneratedAxiom() {
        System.out.println("Generated Axiom: " + generatedAxiom);
        return generatedAxiom;
    }
}

// AnimatedLSystem Class
class AnimatedLSystem {
    private Graphics2D g2d;
    private BufferedImage bufferedImage;
    private Timer timer;
    private String axiom;
    private int currentStep = 0;
    private double x, y;
    private double angle;
    private Stack<double[]> stack;
    // Constructor

    private double turnAngle;  // Add this variable
    private double segmentLength;  // Add this variable

    // Modify the constructor to accept turnAngle and segmentLength
    public AnimatedLSystem(String axiom, double turnAngle, double segmentLength) {
        this.axiom = axiom;
        this.turnAngle = turnAngle;  // Initialize the variable
        this.segmentLength = segmentLength;  // Initialize the variable
        this.stack = new Stack<>();
    }
    public void updateTurnAngleAndSegmentLength(double newTurnAngle, double newSegmentLength, String newAxiom) {
        this.turnAngle = newTurnAngle;
        this.segmentLength = newSegmentLength;
        this.axiom = newAxiom;
    }
    public void resetGraphics(int width, int height) {
        bufferedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        g2d = bufferedImage.createGraphics();
        g2d.setColor(Color.BLACK);  // Set background color
        g2d.fillRect(0, 0, width, height);  // Fill background
        g2d.setColor(Color.GREEN);  // Set drawing color
        x = 0;  // Reset x-coordinate
        y = 0;  // Reset y-coordinate
        angle = 90;  // Reset angle
    }
    private int lastStep = -1;  // Add this to your class fields

    public void drawSystem() {

        g2d.translate(bufferedImage.getWidth() / 2, bufferedImage.getHeight() / 2); // Move to center

        if (lastStep == -1 || lastStep > currentStep) { 
            x = 0;  // Initialize your starting x
            y = 0;  // Initialize your starting y
            angle = 90.0;  // Initialize your starting angle
        }

        if (currentStep < axiom.length()) {
            char command = axiom.charAt(currentStep);
            if (currentStep != lastStep) {
                System.out.println("Current Command: " + command + ", Current Angle: " + angle);  // Debug statement
            }
            switch (command) {
                case 'F': case 'G': case '0': case '1': case'x': // Move forward
                    g2d.setColor(Color.GREEN);  // Green path
                    double newX = x + segmentLength * Math.cos(Math.toRadians(angle));
                    double newY = y - segmentLength * Math.sin(Math.toRadians(angle));

                    int roundedX = (int) Math.round(newX);
                    int roundedY = (int) Math.round(newY);

                    g2d.drawLine((int) x, (int) y, roundedX, roundedY);

                    x = roundedX;
                    y = roundedY;
                    break;
                case '-':  // Turn right
                    angle -= turnAngle;
                    break;
                case '+':  // Turn left
                    angle += turnAngle;
                    break;
                case '[':  // Save state
                    stack.push(new double[]{x, y, angle});
                    break;
                case ']':  // Restore state
                    double[] state = stack.pop();
                    x = state[0];
                    y = state[1];
                    angle = state[2];
                    break;
                case '*':  // Draw a red circle
                    g2d.setColor(Color.RED);  // Red circle
                    g2d.fillOval((int) x - (int)(segmentLength / 4), (int) y - (int)(segmentLength / 4), (int)(segmentLength / 2), (int)(segmentLength / 2));
                    break;

            }
            lastStep = currentStep;
        }g2d.translate(-bufferedImage.getWidth() / 2, -bufferedImage.getHeight() / 2); // Reset translation
    }
    // Start the timer to incrementally draw the system
    public void startTimer(final UI ui, final JPanel panel) {
        if (timer != null) {
            timer.stop();  // Stop the existing timer if it's already running
        }
        currentStep = 0;  // Reset the current step
        lastStep = -1;  // Reset the last step
        timer = new Timer(100, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (currentStep < axiom.length()) {
                    drawSystem();
                    ui.updateDrawingComponent(getBufferedImage());
                    System.out.println("Current Step: " + currentStep + ", Axiom Length: " + axiom.length());
                    currentStep++;
                } else {
                    timer.stop();
                }
            }
        });
        timer.start();
    }
    // Getter for the buffered image to display it in the UI
    public BufferedImage getBufferedImage() {
        return bufferedImage;
    }
}
class UI {
    private JFrame frame;
    private JPanel panel;
    private JMenuBar menuBar;
    private JMenu presetMenu;
    private LSystemGenerator generator;
    private AnimatedLSystem animatedSystem;
    private Threading threading;
    private JTextField iterationsField;
    private JTextField turnAngleField;
    private JTextField segmentLengthField;
    private JButton generateButton;
    private JLabel imageLabel;
    private JTextField rule1PredecessorField;
    private JTextField rule1SuccessorField;
    private JTextField rule2PredecessorField;
    private JTextField rule2SuccessorField;
    private JTextField starter;

    // Add zoom variables
    private double zoomFactor = 1.0;

    public UI(LSystemGenerator generator, AnimatedLSystem animatedSystem, Threading threading) {
        this.generator = generator;
        this.animatedSystem = animatedSystem;
        this.threading = threading;
        this.starter = new JTextField(10);
    }

    public void initializeUI() {
        frame = new JFrame("Animated L-system");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);

        panel = new JPanel();
        frame.add(panel);

        menuBar = new JMenuBar();
        presetMenu = new JMenu("Presets");
        menuBar.add(presetMenu);
        String newStarter = starter.getText();
        JMenuItem binaryTreeItem = new JMenuItem("Binary Tree");
        JMenuItem sierpinskiTriangleItem = new JMenuItem("Sierpinski Triangle");
        JMenuItem dragonCurveItem = new JMenuItem("Dragon Curve");
        JMenuItem barnsleyFernItem = new JMenuItem("Barnsley Fern");
        panel.addMouseWheelListener(new MouseWheelListener() {
            @Override
            public void mouseWheelMoved(MouseWheelEvent e) {
                int notches = e.getWheelRotation();
                if (notches < 0) {
                    // Zoom in when scrolling up
                    zoomFactor *= 1.2; // Increase zoom by 20%
                } else {
                    // Zoom out when scrolling down
                    zoomFactor /= 1.2; // Decrease zoom by 20%
                }
                redrawImage(); // Redraw the image with the updated zoom factor
            }
        });
        binaryTreeItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loadConfiguration("Binary Tree");
            }
        });

        sierpinskiTriangleItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loadConfiguration("Sierpinski Triangle");
            }
        });

        dragonCurveItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loadConfiguration("Dragon Curve");
            }
        });

        barnsleyFernItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loadConfiguration("Barnsley Fern");
            }
        });

        iterationsField = new JTextField(10);
        turnAngleField = new JTextField(10);
        segmentLengthField = new JTextField(10);
        generateButton = new JButton("Generate");

        panel.add(new JLabel("Iterations:"));
        panel.add(iterationsField);
        panel.add(new JLabel("Turn Angle:"));
        panel.add(turnAngleField);
        panel.add(new JLabel("Segment Length:"));
        panel.add(segmentLengthField);

        panel.add(generateButton);
// Add them to the panel
        starter = new JTextField(10);
        panel.add(new JLabel("starter"));
        panel.add(starter);
        rule1PredecessorField = new JTextField(10);
        rule1SuccessorField = new JTextField(10);
        rule2PredecessorField = new JTextField(10);
        rule2SuccessorField = new JTextField(10);
        panel.add(new JLabel("Rule 1 Predecessor:"));
        panel.add(rule1PredecessorField);
        panel.add(new JLabel("Rule 1 Successor:"));
        panel.add(rule1SuccessorField);
        panel.add(new JLabel("Rule 2 Predecessor:"));
        panel.add(rule2PredecessorField);
        panel.add(new JLabel("Rule 2 Successor:"));
        panel.add(rule2SuccessorField);


        imageLabel = new JLabel();  // Initialize JLabel for image display
        panel.add(imageLabel);  // Add to panel
        // Create new text fields for the predecessor and successor of each rule


        // Add zoom buttons to a separate panel
        JPanel zoomPanel = new JPanel();
        JButton zoomInButton = new JButton("Zoom In");
        JButton zoomOutButton = new JButton("Zoom Out");

        zoomInButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                zoomFactor *= 1.2; // Increase zoom by 20%
                redrawImage();
            }
        });

        zoomOutButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                zoomFactor /= 1.2; // Decrease zoom by 20%
                redrawImage();
            }
        });

        zoomPanel.add(zoomInButton);
        zoomPanel.add(zoomOutButton);
        frame.add(zoomPanel, BorderLayout.SOUTH); // Add zoom buttons panel to the bottom of the frame

        frame.setJMenuBar(menuBar);
        frame.setVisible(true);


        generateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println("generateAxiom() called");
                int newIterations = Integer.parseInt(iterationsField.getText());
                double newTurnAngle = Double.parseDouble(turnAngleField.getText());
                double newSegmentLength = Double.parseDouble(segmentLengthField.getText());
                char newRule1pred = rule1PredecessorField.getText().charAt(0);
                char newRule2pred = rule2PredecessorField.getText().charAt(0);
                String newRule1succ = rule1SuccessorField.getText();
                String newRule2succ = rule2SuccessorField.getText();

                String newStarter = starter.getText(); // Read the new starter value


                Map<Character, String> newRules = new HashMap<>();
                newRules.put(newRule1pred, newRule1succ);
                newRules.put(newRule2pred, newRule2succ);
                System.out.println(newRules);
                System.out.println("New Starter: " + newStarter);
                System.out.println("New Rules: " + newRules.toString());
                System.out.println("New Iterations: " + newIterations);
                System.out.println("New Turn Angle: " + newTurnAngle);
                System.out.println("New Segment Length: " + newSegmentLength);
                generator.updateGenerator(newStarter, newRules, newIterations, newTurnAngle, newSegmentLength); // Pass the new starter value
                generator.generateAxiom();
                System.out.println("Generated Axiom: " + generator.getGeneratedAxiom());

                // Reset graphics (if you decide this should be here and not in the separate thread)
                animatedSystem.resetGraphics(800, 600);
                // Execute calculations in a separate thread
                threading.runCalculations(animatedSystem, generator, panel, UI.this);


            }
        });

        presetMenu.add(binaryTreeItem);
        presetMenu.add(sierpinskiTriangleItem);
        presetMenu.add(dragonCurveItem);
        presetMenu.add(barnsleyFernItem);

        frame.setJMenuBar(menuBar);
        frame.setVisible(true);
    }
    // Redraw the image with the updated zoom factor
    private void redrawImage() {
        BufferedImage zoomedBufferedImage = new BufferedImage(
                (int) (animatedSystem.getBufferedImage().getWidth() * zoomFactor),
                (int) (animatedSystem.getBufferedImage().getHeight() * zoomFactor),
                BufferedImage.TYPE_INT_ARGB);

        Graphics2D g2dZoomed = zoomedBufferedImage.createGraphics();
        g2dZoomed.scale(zoomFactor, zoomFactor); // Apply zoom factor
        g2dZoomed.drawImage(animatedSystem.getBufferedImage(), 0, 0, null);
        g2dZoomed.dispose();

        updateDrawingComponent(zoomedBufferedImage);
    }
    public void updateDrawingComponent(BufferedImage image) {
        ImageIcon icon = new ImageIcon(image);
        imageLabel.setIcon(icon);
        System.out.println("Updating drawing component");
    }

    public void loadConfiguration(String presetName) {
        Map<Character, String> newRules = new HashMap<>();
        int newIterations = 4;
        String newStarter = starter.getText();  // Read the starter value from the UI
        double newTurnAngle = 0.0;
        double newSegmentLength = 10.0;

        switch (presetName) {
            case "Binary Tree":
                newStarter = "0";
                newTurnAngle = 45;
                newSegmentLength = 10;
                newRules.put('0', "1[*+0]-0");
                newRules.put('1', "11");
                break;
            case "Sierpinski Triangle":
                newStarter = "F-F-F";
                newTurnAngle = 120;
                newRules.put('F', "F-G+F+G-F");
                newRules.put('G', "GG");
                break;
            case "Dragon Curve":

                newStarter = "F";
                newTurnAngle = 90;
                newRules.put('F', "F+G");
                newRules.put('G', "F-G");
                break;
            case "Barnsley Fern":

                newStarter = "X";
                newTurnAngle = 25;
                newRules.put('X', "F+[[*X]-X]-F[-FX]+X");
                newRules.put('F', "FF");
                break;
            default:
                return;
        }


        iterationsField.setText(String.valueOf(newIterations));
        turnAngleField.setText(Double.toString(newTurnAngle));
        starter.setText(newStarter);
        segmentLengthField.setText(Double.toString(newSegmentLength));

        rule1PredecessorField.setText(newRules.keySet().toArray(new Character[0])[0].toString());
        rule1SuccessorField.setText(newRules.get(newRules.keySet().toArray(new Character[0])[0]));
        rule2PredecessorField.setText(newRules.keySet().toArray(new Character[0])[1].toString());
        rule2SuccessorField.setText(newRules.get(newRules.keySet().toArray(new Character[0])[1]));



    }

}


class Threading {
    public void runCalculations(final AnimatedLSystem animatedSystem, final LSystemGenerator generator, final JPanel panel, final UI ui) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                //animatedSystem.resetGraphics(800, 600);  // Reset graphics and coordinates


                System.out.println("After Generation: " + generator.getGeneratedAxiom());
                animatedSystem.updateTurnAngleAndSegmentLength(generator.getTurnAngle(), generator.getSegmentLength(), generator.getGeneratedAxiom());
                animatedSystem.startTimer(ui, panel);
            }
        }).start();
    }
}
