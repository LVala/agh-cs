import java.awt.Color;
import java.awt.Graphics;
import java.awt.Insets;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.MouseEvent;
import java.util.ArrayList;

import javax.swing.JComponent;
import javax.swing.event.MouseInputListener;

public class Board extends JComponent implements MouseInputListener, ComponentListener {
	private static final long serialVersionUID = 1L;
    public static final String[] neigh_types = {"Moore", "von Neumann", "Moore improved"};
	private Point[][] points;
	private int size = 10;
	public int editType=0;
    public int neigh_type = 1;
    public int cur_neigh_type = 1;

	public Board(int length, int height) {
		addMouseListener(this);
		addComponentListener(this);
		addMouseMotionListener(this);
		setBackground(Color.WHITE);
		setOpaque(true);
	}

	public void iteration() {
        for (int x = 1; x < points.length - 1; ++x)
			for (int y = 1; y < points[x].length - 1; ++y)
				points[x][y].blocked = false;

		for (int x = 1; x < points.length - 1; ++x)
			for (int y = 1; y < points[x].length - 1; ++y)
				points[x][y].move();
		this.repaint();
	}

	public void clear() {
		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y) {
				points[x][y].clear();
			}

        if (neigh_type != cur_neigh_type) {
            initNeighbours();
            cur_neigh_type = neigh_type;
        }
		calculateField();
		this.repaint();
	}

	private void initialize(int length, int height) {
		points = new Point[length][height];

		for (int x = 0; x < points.length; ++x)
			for (int y = 0; y < points[x].length; ++y)
				points[x][y] = new Point();

		initNeighbours();
	}

    private void initNeighbours() {
        for (int x = 1; x < points.length-1; ++x) {
			for (int y = 1; y < points[x].length-1; ++y) {	
                points[x][y].neighbors.clear();;
                // Moore neighborhood
                if (neigh_type == 1) {
                    for (int i=-1; i<2; ++i)
                        for (int j=-1; j<2; ++j)
                            if (!(i == 0 && j == 0))
                                points[x][y].addNeighbor(points[x+i][y+j], 1);
                }
                else if (neigh_type == 2) {
                    // von Neumann neighborhood
                    points[x][y].addNeighbor(points[x+1][y], 1);
                    points[x][y].addNeighbor(points[x-1][y], 1);
                    points[x][y].addNeighbor(points[x][y+1], 1);
                    points[x][y].addNeighbor(points[x][y-1], 1);
                }
                else if (neigh_type == 3) {
                    // Moore improved neighbourhood
                    points[x][y].addNeighbor(points[x+1][y], 1);
                    points[x][y].addNeighbor(points[x-1][y], 1);
                    points[x][y].addNeighbor(points[x][y+1], 1);
                    points[x][y].addNeighbor(points[x][y-1], 1);

                    points[x][y].addNeighbor(points[x+1][y+1], 2);
                    points[x][y].addNeighbor(points[x+1][y-1], 2);
                    points[x][y].addNeighbor(points[x-1][y+1], 2);
                    points[x][y].addNeighbor(points[x-1][y-1], 2);
                }
            }
		}	
    }
	
	private void calculateField(){
        for (int x = 1; x < points.length-1; ++x)
            for (int y = 1; y < points[x].length-1; ++y)
                points[x][y].toWall = 0;


        ArrayList<Point> toCheck = new ArrayList<Point>();
        // walls repulsion force
        for (int x = 1; x < points.length-1; ++x) {
            for (int y = 1; y < points[x].length-1; ++y) {
                if (points[x][y].type == 1) {
                    points[x][y].toWall = 0;  // WALL REPULTION
                    points[x][y].neighbors.forEach((neigh) -> {
                        if (neigh.type != 2 && neigh.type != 1)
                            toCheck.add(neigh);
                    });
                    points[x][y].diagneighbors.forEach((neigh) -> {
                        if (neigh.type != 2 && neigh.type != 1)
                            toCheck.add(neigh);
                    });
                }
            }
        }

        while (!toCheck.isEmpty()) {
            if (toCheck.get(0).calcWallRepulsion()) {
                toCheck.get(0).neighbors.forEach((neigh) -> {toCheck.add(neigh);});
                toCheck.get(0).diagneighbors.forEach((neigh) -> {toCheck.add(neigh);});
            }
            toCheck.remove(0);
        }

        for (int x = 1; x < points.length-1; ++x) {
			for (int y = 1; y < points[x].length-1; ++y) {
                if (points[x][y].type == 2) {
                    points[x][y].staticField = 0;
                    points[x][y].neighbors.forEach((neigh) -> {
                        if (neigh.type != 2)
                            toCheck.add(neigh);
                    });
                    points[x][y].diagneighbors.forEach((neigh) -> {
                        if (neigh.type != 2)
                            toCheck.add(neigh);
                    });
                }
            }
        }

        while (!toCheck.isEmpty()) {
            if (toCheck.get(0).calcStaticField()) {
                toCheck.get(0).neighbors.forEach((neigh) -> {toCheck.add(neigh);});
                toCheck.get(0).diagneighbors.forEach((neigh) -> {toCheck.add(neigh);});
            }
            toCheck.remove(0);
        }

        for (int x = 1; x < points.length-1; ++x)
            for (int y = 1; y < points[x].length-1; ++y)
                points[x][y].staticField += points[x][y].toWall;
    }

	protected void paintComponent(Graphics g) {
		if (isOpaque()) {
			g.setColor(getBackground());
			g.fillRect(0, 0, this.getWidth(), this.getHeight());
		}
		g.setColor(Color.GRAY);
		drawNetting(g, size);
	}

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

		for (x = 1; x < points.length-1; ++x) {
			for (y = 1; y < points[x].length-1; ++y) {
				if(points[x][y].type==0){
					float staticField = points[x][y].staticField;
					float intensity = staticField/100;
					if (intensity > 1.0) {
						intensity = 1.0f;
					}
					g.setColor(new Color(intensity, intensity,intensity ));
				}
				else if (points[x][y].type==1){
					g.setColor(new Color(1.0f, 0.0f, 0.0f, 0.7f));
				}
				else if (points[x][y].type==2){
					g.setColor(new Color(0.0f, 1.0f, 0.0f, 0.7f));
				}
				if (points[x][y].isPedestrian){
					g.setColor(new Color(0.0f, 0.0f, 1.0f, 0.7f));
				}
				g.fillRect((x * size) + 1, (y * size) + 1, (size - 1), (size - 1));
			}
		}

	}

	public void mouseClicked(MouseEvent e) {
		int x = e.getX() / size;
		int y = e.getY() / size;
		if ((x < points.length) && (x > 0) && (y < points[x].length) && (y > 0)) {
			if(editType==3){
				points[x][y].isPedestrian=true;
			}
			else{
				points[x][y].type= editType;
			}
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
			if(editType==3){
				points[x][y].isPedestrian=true;
			}
			else{
				points[x][y].type= editType;
			}
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
