"""Benchly Admin GUI: visualize benchmark results."""

import argparse
import logging

from PyQt6 import QtCore, QtGui, QtWidgets

from shared.utils import configure_basic_logging
from shared.constants import DEFAULT_SERVER_URL
from .api import BenchlyAPI


class LeaderboardTableModel(QtCore.QAbstractTableModel):
    HEADERS = ["Rank", "Machine", "Score", "Submitted", "CPU (s)", "RAM (s)", "Disk Write (s)", "Disk Read (s)"]

    def __init__(self, rows=None):
        super().__init__()
        self._rows = rows or []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        row = self._rows[index.row()]
        col = index.column()

        if col == 0:
            return str(index.row() + 1)
        if col == 1:
            return row.get("machine_id")
        if col == 2:
            return f"{row.get('score', 0):.2f}"
        if col == 3:
            return row.get("created_at")

        payload = row.get("payload", {})
        results = payload.get("results", {})

        if col == 4:
            return f"{results.get('cpu', {}).get('duration_s', 0):.3f}"
        if col == 5:
            return f"{results.get('ram', {}).get('duration_s', 0):.3f}"
        if col == 6:
            return f"{results.get('disk', {}).get('write_seconds', 0):.3f}"
        if col == 7:
            return f"{results.get('disk', {}).get('read_seconds', 0):.3f}"

        return None

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def update_rows(self, rows):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()


class BenchlyAdminWindow(QtWidgets.QMainWindow):
    def __init__(self, server_url: str):
        super().__init__()
        self.setWindowTitle("Benchly Admin")
        self.resize(900, 600)

        self.api = BenchlyAPI(server_url)
        self._build_ui()
        self._refresh_data()

    def _build_ui(self):
        main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(main)

        toolbar = QtWidgets.QHBoxLayout()
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._refresh_data)
        self.server_label = QtWidgets.QLabel(f"Server: {self.api.server_url}")
        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch(1)
        toolbar.addWidget(self.server_label)

        self.table = QtWidgets.QTableView()
        self.table_model = LeaderboardTableModel([])
        self.table.setModel(self.table_model)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.setCentralWidget(main)

    def _refresh_data(self):
        try:
            response = self.api.get_leaderboard(limit=200)
            rows = response.get("results", [])
            self.table_model.update_rows(rows)
        except Exception as ex:
            logging.getLogger("benchly.admin").exception("Failed to refresh leaderboard: %s", ex)
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to fetch leaderboard:\n{ex}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchly admin GUI")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, help="Benchly server URL")
    args = parser.parse_args()

    configure_basic_logging()

    app = QtWidgets.QApplication([])
    window = BenchlyAdminWindow(args.server)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
