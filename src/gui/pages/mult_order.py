import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QDialog,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QVBoxLayout,
)

LEAF_COLOR = QColor("#7fb3d5")
MERGE_COLOR = QColor("#f5b041")
ROOT_COLOR = QColor("#58d68d")
BORDER_COLOR = QColor("#2c3e50")
LINE_COLOR = QColor("#5d6d7e")
NODE_RADIUS = 22


class MultOrder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.order: list[int] = []
        self.nodes: list[TreeNode] = []
        self.resize(1400, 900)

    def _setup_ui(self):
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor("#eef1f5"))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

    def _set_first_row(self):
        self.scene.clear()

        x, y = 20, 20
        for i in range(len(self.order) + 1):
            node = TreeNode(x, y, i + 1, "A", LEAF_COLOR)
            self.scene.addItem(node)
            self.nodes.append(node)
            x += 60

    def set_snapshot(self, order: list[int]):
        self.order = order
        self._set_first_row()

        for step, ind in enumerate(order, start=1):
            is_last = step == len(order)
            self._connect_nodes(ind, is_root=is_last)

    def _connect_nodes(self, ind: int, is_root: bool = False):
        first_node = self.nodes[ind]
        second_node = self.nodes[ind + 1]

        p1 = first_node.sceneBoundingRect().center()
        p2 = second_node.sceneBoundingRect().center()

        color = ROOT_COLOR if is_root else MERGE_COLOR
        new_node = self._new_node(p1, p2, ind, color)
        self.scene.addItem(new_node)
        p3 = new_node.sceneBoundingRect().center()

        b1 = first_node.get_perf_point(p3)
        b1_end = new_node.get_perf_point(p1)
        self._draw_curve(b1, b1_end)

        b2 = second_node.get_perf_point(p3)
        b2_end = new_node.get_perf_point(p2)
        self._draw_curve(b2, b2_end)

        self.nodes[ind] = new_node
        self.nodes.pop(ind + 1)

    def _draw_curve(self, start: QPointF, end: QPointF):
        path = QPainterPath(start)

        c1 = QPointF(start.x(), start.y() + (end.y() - start.y()) * 0.5)
        c2 = QPointF(end.x(), start.y() + (end.y() - start.y()) * 0.5)
        path.cubicTo(c1, c2, end)

        item = QGraphicsPathItem(path)
        pen = QPen(LINE_COLOR, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        item.setPen(pen)
        self.scene.addItem(item)

    def _new_node(self, p1: QPointF, p2: QPointF, ind: int, color: QColor):
        new_x = (p1.x() + p2.x()) / 2 - NODE_RADIUS
        new_y = max(p1.y(), p2.y()) + 60
        new_node = TreeNode(new_x, new_y, ind, "M", color)
        return new_node


class TreeNode(QGraphicsEllipseItem):
    def __init__(
        self,
        x: float,
        y: float,
        index: int,
        letter: str = "M",
        color: QColor = MERGE_COLOR,
    ):
        d = NODE_RADIUS * 2
        super().__init__(0, 0, d, d)
        self.index = index

        self.setPos(x, y)
        self.setBrush(QBrush(color))
        self.setPen(QPen(BORDER_COLOR, 1.5))
        self.setZValue(1)

        self.label = QGraphicsSimpleTextItem(f"{letter}{index}", self)
        font = QFont("Segoe UI", 9, QFont.Weight.DemiBold)
        self.label.setFont(font)
        self.label.setBrush(QBrush(QColor("#1c2833")))
        self.label.setZValue(2)

        text_rect = self.label.boundingRect()
        node_rect = self.rect()
        self.label.setPos(
            node_rect.center().x() - text_rect.width() / 2,
            node_rect.center().y() - text_rect.height() / 2,
        )

    def get_perf_point(self, other: QPointF) -> QPointF:
        """
        Функия для поиска точки окружности нода для идеального соединения

        Требуется для черчения линий не через центры нодов.
        """
        center = self.sceneBoundingRect().center()
        rx = self.rect().width() / 2
        ry = self.rect().height() / 2

        dx = other.x() - center.x()
        dy = other.y() - center.y()

        if dx == 0 and dy == 0:
            return center

        denom = math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
        t = 1 / denom

        return QPointF(center.x() + dx * t, center.y() + dy * t)

    def decrement(self):
        self.index -= 1
