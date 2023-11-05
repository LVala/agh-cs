import java.awt.Color;
import java.awt.Graphics;
import java.awt.Insets;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.MouseEvent;

import javax.swing.JComponent;
import javax.swing.event.MouseInputListener;

/**
 * Board with Points that may be expanded (with automatic change of cell
 * number) with mouse event listener
 */

public class Board extends JComponent implements MouseInputListener, ComponentListener {
	private static final long serialVersionUID = 1L;
	private Point[][] points;
	private int size = 14;
    private SimType simType = SimType.GAME_OF_LIFE;

	public Board(int length, int height) {
		addMouseListener(this);
		addComponentListener(this);
		addMouseMotionListener(this);
		setBackground(Color.WHITE);
		setOpaque(true);
	}

    public void setSimType(SimType type) {
        simType = type;
    }

	// single iteration
	public void iteration() {
        if (simType.equals(SimType.RAIN)) {
            // generate top row raindrops with some probability
		    for (int x = 0; x < points.length; ++x)
            ((PointRain) points[x][0]).drop();
        }

		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y)
				points[x][y].calculateNewState();

		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y)
				points[x][y].changeState();
		this.repaint();
	}

	// clearing board
	public void clear() {
		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y) {
				points[x][y].setState(0);
			}
		this.repaint();
	}

	public void initialize(int length, int height) {
		points = new Point[length][height];

		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y)
				if (simType.equals(SimType.GAME_OF_LIFE)) {
                    points[x][y] = new PointGoL();
                }
                else if (simType.equals(SimType.RAIN)) {
                    points[x][y] = new PointRain();
                }

        if (simType.equals(SimType.GAME_OF_LIFE)) {
            for (int x = 0; x < points.length; ++x) {
                for (int y = 0; y < points[x].length; ++y) {
                    // initialization of neighbors implementing periodic boundaries
                    for (int i = -1; i <= 1; i++) {
                        for (int j = -1; j <= 1; j++) {
                            if (!(i == 0 & j == 0))
                                points[x][y].addNeighbor(points[(points.length + x + i) % points.length][(points[x].length + y + j) % points[x].length]);
                        }
                    }
                }
            }
        }
        else if (simType.equals(SimType.RAIN)) {
            for (int x = 0; x < points.length; ++x) {
                for (int y = 1; y < points[x].length; ++y) {
                    // initialization of neighbors (only the one above)
                    points[x][y].addNeighbor(points[x][y-1]);
                }
            }
        }
	}

    public void reinitialize() {
        int length = points.length;
        int height = points[0].length;
        initialize(length, height);
    }

	//paint background and separators between cells
	protected void paintComponent(Graphics g) {
		if (isOpaque()) {
			g.setColor(getBackground());
			g.fillRect(0, 0, this.getWidth(), this.getHeight());
		}
		g.setColor(Color.GRAY);
		drawNetting(g, size);
	}

	// draws the background netting
	private void drawNetting(Graphics g, int gridSpace) {
		Insets insets = getInsets();
		int firstX = insets.left;
		int firstY = insets.top;
		int lastX = this.getWidth() - insets.right;
		int lastY = this.getHeight() - insets.bottom;

		int x = firstX;
		while (x < lastX) {
			g.drawLine(x, firstY, x, lastY);
			x += gridSpace;
		}

		int y = firstY;
		while (y < lastY) {
			g.drawLine(firstX, y, lastX, y);
			y += gridSpace;
		}

        if (simType.equals(SimType.GAME_OF_LIFE)) {
            for (x = 0; x < points.length; ++x) {
                for (y = 0; y < points[x].length; ++y) {
                    if (points[x][y].getState() != 0) {	
                        g.setColor(new Color(0x000000));
                        g.fillRect((x * size) + 1, (y * size) + 1, (size - 1), (size - 1));
                    }
                }
            }
        }
        else if (simType.equals(SimType.RAIN)) {
            for (x = 0; x < points.length; ++x) {
                for (y = 0; y < points[x].length; ++y) {
                    if (points[x][y].getState() != 0) {
                        switch (points[x][y].getState()) {
                        case 1:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.16f));
                            break;
                        case 2:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.33f));
                            break;
                        case 3:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.5f));
                            break;						
                        case 4:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.66f));
                            break;						
                        case 5:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.83f));
                            break;						
                        case 6:
                            g.setColor(new Color(0.0f, 0.0f, 1.0f, 1.0f));
                            break;						
                        }
                        g.fillRect((x * size) + 1, (y * size) + 1, (size - 1), (size - 1));
                    }
                }
            }
        }
	}

	public void mouseClicked(MouseEvent e) {
		int x = e.getX() / size;
		int y = e.getY() / size;
		if ((x < points.length) && (x > 0) && (y < points[x].length) && (y > 0)) {
			points[x][y].clicked();
			this.repaint();
		}
	}

	public void componentResized(ComponentEvent e) {
		int dlugosc = (this.getWidth() / size) + 1;
		int wysokosc = (this.getHeight() / size) + 1;
		initialize(dlugosc, wysokosc);
	}

	public void mouseDragged(MouseEvent e) {
		int x = e.getX() / size;
		int y = e.getY() / size;
		if ((x < points.length) && (x > 0) && (y < points[x].length) && (y > 0)) {
			points[x][y].setState(1);
			this.repaint();
		}
	}

	public void mouseExited(MouseEvent e) {
	}

	public void mouseEntered(MouseEvent e) {
	}

	public void componentShown(ComponentEvent e) {
	}

	public void componentMoved(ComponentEvent e) {
	}

	public void mouseReleased(MouseEvent e) {
	}

	public void mouseMoved(MouseEvent e) {
	}

	public void componentHidden(ComponentEvent e) {
	}

	public void mousePressed(MouseEvent e) {
	}

}
