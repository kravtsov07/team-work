import math
from enum import Enum

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
FIT_MARGIN_X = 40
FIT_MARGIN_Y = 120
MIN_ZOOM = 0.05
MAX_ZOOM = 20.0
ZOOM_FACTOR = 1.15


class NodeKind(Enum):
    LEAF = ("A", LEAF_COLOR)
    MERGE = ("M", MERGE_COLOR)
    ROOT = ("M", ROOT_COLOR)


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def fit_content(self):
        self.resetTransform()
        rect = self.scene().itemsBoundingRect()
        if rect.isNull():
            return

        rect.adjust(-FIT_MARGIN_X, -FIT_MARGIN_Y, FIT_MARGIN_X, FIT_MARGIN_Y)
        self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_content()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta == 0:
            return

        factor = ZOOM_FACTOR if delta > 0 else 1 / ZOOM_FACTOR
        current_scale = self.transform().m11()
        new_scale = current_scale * factor
        if new_scale < MIN_ZOOM or new_scale > MAX_ZOOM:
            return

        self.scale(factor, factor)


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

        self.view = ZoomableGraphicsView(self.scene)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def _set_first_row(self):
        self.scene.clear()

        x, y = 20, 60
        for i in range(len(self.order) + 1):
            node = TreeNode(x, y, i + 1, NodeKind.LEAF)
            self.scene.addItem(node)
            self.nodes.append(node)
            x += 60

    def set_snapshot(self, order: list[int]):
        self.order = order
        self.nodes = []
        self._set_first_row()

        for step, ind in enumerate(order, start=1):
            is_last = step == len(order)
            self._connect_nodes(ind, merge_number=step, is_root=is_last)

        self.view.fit_content()

    def _connect_nodes(self, ind: int, merge_number: int, is_root: bool = False):
        if not 0 <= ind < len(self.nodes) - 1:
            raise IndexError(
                f"merge index {ind} out of range for {len(self.nodes)} node(s)"
            )

        first_node = self.nodes[ind]
        second_node = self.nodes[ind + 1]

        p1 = first_node.sceneBoundingRect().center()
        p2 = second_node.sceneBoundingRect().center()

        kind = NodeKind.ROOT if is_root else NodeKind.MERGE
        new_node = self._new_node(p1, p2, merge_number, kind)
        self.scene.addItem(new_node)
        p3 = new_node.sceneBoundingRect().center()

        for node, p in ((first_node, p1), (second_node, p2)):
            start = node.get_perf_point(p3)
            end = new_node.get_perf_point(p)
            self._draw_curve(start, end)

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

    def _new_node(self, p1: QPointF, p2: QPointF, merge_number: int, kind: NodeKind):
        new_x = (p1.x() + p2.x()) / 2 - NODE_RADIUS
        new_y = max(p1.y(), p2.y()) + 80
        return TreeNode(new_x, new_y, merge_number, kind)


class TreeNode(QGraphicsEllipseItem):
    def __init__(
        self,
        x: float,
        y: float,
        index: int,
        kind: NodeKind = NodeKind.MERGE,
    ):
        letter, color = kind.value

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
